import time
from datetime import datetime, timedelta
from uuid import uuid4

import schedule
from fastapi import WebSocket, APIRouter, HTTPException
from langchain.memory import ChatMessageHistory
from langchain_community.document_loaders.pdf import PyPDFium2Loader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from setting import config
from utils.json_converter import JsonConverter
from utils.logger import logger

router = APIRouter()

# Define the global variable 'sessions' at the module level
sessions = {}

SESSION_TIMEOUT = timedelta(minutes=30)  # Set the session timeout to 30 minutes


def remove_inactive_sessions():
    """Remove sessions that have been inactive for more than SESSION_TIMEOUT."""
    global sessions
    now = datetime.now()
    inactive_sessions = [session_id for session_id, session in sessions.items() if
                         now - session['last_active'] > SESSION_TIMEOUT]
    for session_id in inactive_sessions:
        del sessions[session_id]


# Schedule the remove_inactive_sessions function to run every minute
schedule.every(1).minutes.do(remove_inactive_sessions)


@router.websocket("/chat")
async def chat_openai_prompt_templates_history_continuous_stream(websocket: WebSocket):
    MAX_TOKENS = 10000
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

    # chat = ChatOpenAI(openai_api_key=config['large-model']['openai-key'],
    #                   model_name="gpt-3.5-turbo-0125",
    #                   streaming=True,
    #                   )

    chat = ChatOpenAI(openai_api_key=config['large-model']['openai-key'],
                      openai_api_base="https://api.moonshot.cn/v1",
                      model_name="moonshot-v1-8k",
                      streaming=True,
                      )

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


@router.post("/build")
async def build_chat():
    global sessions
    session_id = str(uuid4())
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

    chat = ChatOpenAI(openai_api_key=config['large-model']['openai-key'],
                      model_name="gpt-3.5-turbo-0125",
                      # streaming=True,
                      )
    MAX_TOKENS = 10000
    sessions[session_id] = {"chat": chat, "history": demo_ephemeral_chat_history, "prompt": prompt,
                            "MAX_TOKENS": MAX_TOKENS}

    # 将会话数据序列化为JSON
    session_data = {
        "chat": chat,
        "history": demo_ephemeral_chat_history,
        "prompt": prompt,
        "MAX_TOKENS": MAX_TOKENS
    }
    session_data_json = JsonConverter.to_json(session_data)
    logger.info("session_data_json: ", session_data_json)
    return {"session_id": session_id}


from fastapi import WebSocket, WebSocketDisconnect


@router.websocket("/chat/{session_id}")
async def chat_openai_prompt_templates_history_continuous_stream(websocket: WebSocket, session_id: str):
    global sessions
    if session_id not in sessions:
        print("Invalid session ID.")
        return

    session = sessions[session_id]
    chat = session["chat"]
    demo_ephemeral_chat_history = session["history"]
    prompt = session["prompt"]
    MAX_TOKENS = session["MAX_TOKENS"]

    total_length = len("你是一个有用的助手。尽你所能回答所有问题。请用中文进行对话") + len("你好!") + len("有什么问题嘛?")
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
                total_length = len("你是一个有用的助手。尽你所能回答所有问题。请用中文进行对话") + len("你好!") + len(
                    "有什么问题嘛?")
            print(f"Current total_length: {total_length}")

            # Update the last active time of the session
            session['last_active'] = datetime.now()
        except WebSocketDisconnect:
            await websocket.close()
            break


@router.get("/sessions")
async def get_sessions():
    global sessions
    if not sessions:
        raise HTTPException(status_code=404, detail="No active sessions")
    return sessions


@router.get("/test/{question}")
async def get_sessions(question: str):
    # Load, chunk and index the contents of the blog.
    loader = PyPDFium2Loader(
        "https://hq-prd-e-zine.oss-cn-szfinance.aliyuncs.com/agent/prd/admin/hqins_model_match/product/5cabe54ee999463187f08572629b0f8d.pdf")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(
        openai_api_key=config['large-model']['openai-key']))

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()

    template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Use three sentences maximum and keep the answer as concise as possible.
        Always say "thanks for asking!" at the end of the answer.

        {context}

        Question: {question}

        Helpful Answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0,
                     openai_api_key=config['large-model']['openai-key'])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | custom_rag_prompt
            | llm
            | StrOutputParser()
    )

    # invoke = rag_chain.invoke("What is Task Decomposition?")
    invoke = rag_chain.invoke(question)
    print(invoke)
    return invoke


# Start the scheduler in a separate thread
def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


import threading

scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.start()
