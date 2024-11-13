import asyncio
import json

from fastapi import WebSocket, WebSocketDisconnect
from langchain import hub
from langchain_community.document_loaders.pdf import PyPDFium2Loader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_text_splitters import RecursiveCharacterTextSplitter

from constants.large_model_enum import LargeModelName
from services.components.langchain.v1.chats.chat_components import get_chat_model
from services.components.langchain.v1.prompts.generate_prompts import generation_prompt_template
from services.components.langchain.v1.vectorstores.pgvector import generation_pgvector
from services.knowledge.knowledge_service import KnowledgeService
from setting import config
from utils.json_converter import JsonConverter
from utils.logger import logger


async def get_files(knowledgeService: KnowledgeService, knowledge_id: int):
    # ... get_files的实现 ...
    files = []
    knowledge_vo = knowledgeService.get_knowledge_by_id(knowledge_id)
    if knowledge_vo is None:
        logger.info(
            "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream knowledge_vo is None")
        return files
    file_vos = knowledge_vo.file_vos
    if file_vos is None or len(file_vos) == 0:
        logger.info(
            "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream file_vos is None")
        return files
    files.extend(file_vos)
    logger.info(
        "model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream files: ",
        JsonConverter.to_json(files))
    return files


async def prompt_model_match_templates_stream(websocket: WebSocket,
                                              model_name: str,
                                              knowledge_id: int,
                                              knowledgeService: KnowledgeService,
                                              ):
    # ... chat_openai_prompt_templates_stream的实现 ...
    await websocket.accept()

    if knowledge_id == 0:
        for model in LargeModelName:
            # 检查每个模型的 vendor_name 是否与 application 中的 model_name 匹配
            if model.vendor_name == model_name:
                # 如果找到匹配项，将其赋值给变量 large_model
                large_model = model
                break
        else:
            # 如果在遍历整个枚举后没有找到匹配项，关闭 websocket 连接
            await websocket.close(code=1008, reason="在 LargeModelName 枚举中未找到匹配的模型")
            return

        chat: BaseChatModel = None
        chat, rate_limiter = await get_chat_model(chat, large_model)

        # 从第一条WebSocket消息中获取prompt_params参数和prompt_template参数
        first_message_str = await websocket.receive_text()
        # 将字符串转换为字典
        first_message = json.loads(first_message_str)

        prompt_template = first_message['prompt_template']
        prompt_params = first_message['prompt_params']

        prompt = generation_prompt_template(prompt_template=prompt_template, prompt_params=prompt_params)

        total_length = 0
        total_content = ""
        try:

            chain = prompt | chat

            for chunk in chain.stream(prompt_params):
                await websocket.send_text(chunk.content)
                await asyncio.sleep(0.5)
                total_length += len(chunk.content)
                total_content += chunk.content
            logger.info(f"Estimated total tokens used: {total_length}, Current total_content: {total_content}")
            await websocket.close(code=1000, reason="对话结束")
        except WebSocketDisconnect:
            await websocket.close()
        finally:
            if rate_limiter is not None:
                rate_limiter.add_request(large_model.vendor_name, total_length)
    else:

        # 从第一条WebSocket消息中获取prompt_params参数和prompt_template参数
        first_message_str = await websocket.receive_text()
        
        # 提取出所有的文件信息
        files = await get_files(knowledgeService=knowledgeService, knowledge_id=knowledge_id, )
        if len(files) > 0:
            file_ids = [file.id for file in files if file.id is not None]
            # 使用 pgVector
            vectorstore = generation_pgvector()

            # Retrieve and generate using the relevant snippets of the docs.
            retriever = vectorstore.as_retriever(search_kwargs={"k": 4, "filter": {"file_id": {"$in": file_ids}}})
            prompt = hub.pull("rlm/rag-prompt")
            llm: BaseChatModel = None

            for model in LargeModelName:
                # 检查每个模型的 vendor_name 是否与 application 中的 model_name 匹配
                if model.vendor_name == model_name:
                    # 如果找到匹配项，将其赋值给变量 large_model
                    large_model = model
                    break
            llm, rate_limiter = await get_chat_model(llm, large_model, )

            def format_docs(docs):
                for doc in docs:
                    logger.info(
                        f"model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream doc page_content: {doc.page_content}")
                return "\n\n".join(doc.page_content for doc in docs)

            rag_chain_from_docs = (
                    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
                    | prompt
                    | llm
                    | StrOutputParser()
            )

            rag_chain_with_source = RunnableParallel(
                {"context": retriever, "question": RunnablePassthrough()}
            ).assign(answer=rag_chain_from_docs)


            # 将字符串转换为字典
            first_message = json.loads(first_message_str)

            prompt_template = first_message['prompt_template']
            prompt_params = first_message['prompt_params']

            template = generation_prompt_template(prompt_template=prompt_template, prompt_params=prompt_params)

            question = template.invoke(prompt_params)

            total_length = 0
            total_content = ""

            try:

                for chunk in rag_chain_with_source.stream(question.text):
                    logger.info(f"model-match api/v1/chat_api.py chat_openai_prompt_templates_history_continuous_stream chunk: {chunk}")
                    if 'answer' in chunk:
                        await websocket.send_text(chunk['answer'])
                        await asyncio.sleep(0.5)
                        total_length += len(chunk['answer'])
                        total_content += chunk['answer']
                logger.info(f"Estimated total tokens used: {total_length}, Current total_content: {total_content}")
                await websocket.close(code=1000, reason="对话结束")
            except WebSocketDisconnect:
                await websocket.close(code=1000, reason="对话结束")
            finally:
                if rate_limiter is not None:
                    rate_limiter.add_request(large_model.vendor_name, total_length)

    return


def test():
    from langchain import hub
    prompt = hub.pull("rlm/rag-prompt")
    print(prompt)


if __name__ == "__main__":
    test()
