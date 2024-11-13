from typing import Optional, List

from fastapi import WebSocket, WebSocketDisconnect
from langchain.memory import ChatMessageHistory
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from constants.constants import MAX_TOKENS
from constants.large_model_enum import LargeModelName
from model.vo.application_vo import ApplicationVO
from model.vo.file_vo import FileVO
from model.vo.knowledge_vo import KnowledgeVO
from services.application.application_service import ApplicationService
from services.components.langchain.v1.chats.chat_components import get_chat_model
from services.components.langchain.v1.vectorstores.pgvector import generation_pgvector
from services.knowledge.knowledge_service import KnowledgeService
from utils.json_converter import JsonConverter
from utils.logger import logger


async def get_files(knowledgeService: KnowledgeService, knowledge_vos: List[KnowledgeVO]) -> List[FileVO]:
    files = []
    for knowledge in knowledge_vos:
        knowledge_vo = knowledgeService.get_knowledge_by_id(knowledge.id)
        if knowledge_vo is None:
            logger.info(
                "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream knowledge_vo is None")
            continue
        file_vos = knowledge_vo.file_vos
        if file_vos is None or len(file_vos) == 0:
            logger.info(
                "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream file_vos is None")
            continue
        files.extend(file_vos)
    logger.info(
        "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream files: ",
        JsonConverter.to_json(files))
    return files


async def get_application(applicationService: ApplicationService, application_id: int,
                          ) -> Optional[ApplicationVO]:
    application = applicationService.get_application_by_id(application_id)
    logger.info(
        "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream application: ",
        application)
    if application is None:
        logger.error(
            "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream application is None")
        return None
    return application


async def application_chat_history_continuous_stream(websocket: WebSocket, application_id: int,
                                                     applicationService: ApplicationService,
                                                     knowledgeService: KnowledgeService,
                                                     ):
    # 将原始函数的整个主体复制到这里
    # 将`applicationService`和`knowledgeService`的所有实例替换为`self.applicationService`和`self.knowledgeService`
    await websocket.accept()
    # 获取application信息
    application = await get_application(applicationService, application_id)
    if application is None or application.model_name is None or application.model_name_valid is False:
        await websocket.close(code=1008, reason="application or model_name is None")
        return
    # 判断属于哪一个公司
    chat: BaseChatModel = None
    # 遍历 LargeModelName 枚举
    for model in LargeModelName:
        # 检查每个模型的 vendor_name 是否与 application 中的 model_name 匹配
        if model.vendor_name == application.model_name:
            # 如果找到匹配项，将其赋值给变量 large_model
            large_model = model
            break
    else:
        # 如果在遍历整个枚举后没有找到匹配项，关闭 websocket 连接
        await websocket.close(code=1008, reason="在 LargeModelName 枚举中未找到匹配的模型")
        return

    # 如果找到匹配的模型，通过调用 get_chat_model 函数获取相应的聊天模型
    chat, rate_limiter = await get_chat_model(chat, large_model)
    knowledge_vos = application.knowledge_vos
    if knowledge_vos is None or len(knowledge_vos) == 0:
        logger.info(
            "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream knowledge_vos is None")

    if len(knowledge_vos) > 0:
        # 提取出所有的文件信息
        files = await get_files(knowledgeService, knowledge_vos)
        if len(files) > 0:
            file_ids = [file.id for file in files if file.id is not None]
            # 使用 pgVector
            vectorstore = generation_pgvector()

            # Retrieve and generate using the relevant snippets of the docs.
            retriever = vectorstore.as_retriever(search_kwargs={"k": 4, "filter": {"file_id": {"$in": file_ids}}})
            llm: BaseChatModel = None
            llm, rate_limiter = await get_chat_model(llm, large_model)

            def format_docs(docs):
                for doc in docs:
                    logger.info(
                        f"model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream doc page_content: {doc.page_content}")
                return "\n\n".join(doc.page_content for doc in docs)

            contextualize_q_system_prompt = """Given a chat history and the latest user question
                    which might reference context in the chat history, formulate a standalone question
                    which can be understood without the chat history. Do NOT answer the question,
                    just reformulate it if needed and otherwise return it as is."""
            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}"),
                ]
            )
            contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

            qa_system_prompt = """You are an assistant for question-answering tasks. 
                                Use the following pieces of retrieved context to answer the question. 
                                If you don't know the answer, just say that you don't know. 

                                {context}"""
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}"),
                ]
            )

            def contextualized_question(input: dict):
                if input.get("chat_history"):
                    return contextualize_q_chain
                else:
                    return input["question"]

            rag_chain = (
                    RunnablePassthrough.assign(
                        context=contextualized_question | retriever | format_docs
                    )
                    | qa_prompt
                    | llm
            )

            chat_history = []
            # await websocket.accept()
            while True:  # Loop until a break condition is met
                # question = input("Please enter your question: ")  # Get question from user input
                question = await websocket.receive_text()
                if question.lower() == 'exit':  # If user types 'exit', break the loop
                    break
                chunks: str = ""
                for chunk in rag_chain.stream({"question": question, "chat_history": chat_history}):
                    logger.info(
                        f"model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream chunk content: {chunk}")
                    await websocket.send_text(chunk.content)
                    chunks += chunk.content
                chat_history.extend([HumanMessage(content=question), chunks])
                logger.info(
                    f"model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream chunks: {chunks}, chat_history: {chat_history}")
    else:
        system_message_content = "你是一个有用的助手。尽你所能回答所有问题。请用中文进行对话"
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_message_content,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        demo_ephemeral_chat_history = ChatMessageHistory()
        demo_ephemeral_chat_history.add_user_message("你好!")
        demo_ephemeral_chat_history.add_ai_message("有什么问题嘛?")
        chat_history_messages = demo_ephemeral_chat_history.messages
        print("chat_history_messages:", chat_history_messages)
        total_length = len(system_message_content) + len("你好!") + len("有什么问题嘛?")
        await websocket.accept()
        while True:
            try:
                user_message = await websocket.receive_text()
                demo_ephemeral_chat_history.add_user_message(user_message)
                total_length += len(user_message)
                chain = prompt | chat
                for chunk in chain.stream({"messages": demo_ephemeral_chat_history.messages}, ):
                    await websocket.send_text(chunk.content)
                    total_length += len(chunk.content)
                print(f"Estimated total tokens used: {total_length}")
                if total_length >= MAX_TOKENS:
                    demo_ephemeral_chat_history.clear()
                    demo_ephemeral_chat_history.add_user_message("你好!")
                    demo_ephemeral_chat_history.add_ai_message("有什么问题嘛?")
                    total_length = len(system_message_content) + len("你好!") + len("有什么问题嘛?")
                print(f"Current total_length: {total_length}")
            except WebSocketDisconnect:
                await websocket.close()
                break
            finally:
                if rate_limiter is not None:
                    rate_limiter.add_request(large_model.vendor_name, total_length)
                await websocket.close()
