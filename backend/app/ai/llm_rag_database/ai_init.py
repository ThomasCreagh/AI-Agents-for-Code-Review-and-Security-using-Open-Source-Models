# import asyncio

from app.ai.llm_rag_database.create_rag_db import RagDB
from app.ai.llm_rag_database.launch import RunModel

db = RagDB()
run_model = RunModel()


def init():
    global db
    global run_model
    print("init db...")
    db = RagDB()
    print("finished init db...")
    print("start 0")
    run_model = RunModel()
    print("finished 0")
