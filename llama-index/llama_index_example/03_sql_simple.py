#!/usr/bin/python3
# encoding=utf-8

"""
    项目名称:  llamaindex_learn
    文件名称： 03_sql_simple1.py
    功能描述： ..
    创建者：   lixinxin
    创建日期： 2024/3/14 13:47
"""
import datetime
import os
import openai
from llama_index.core import SQLDatabase
from llama_index.llms.ollama import Ollama

os.environ["OPENAI_API_KEY"] = "sk-.."
openai.api_key = os.environ["OPENAI_API_KEY"]

from IPython.display import Markdown, display

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)

if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:")
    metadata_obj = MetaData()

    # create city SQL table
    table_name = "city_stats"
    city_stats_table = Table(
        table_name,
        metadata_obj,
        Column("city_name", String(16), primary_key=True),
        Column("population", Integer),
        Column("country", String(16), nullable=False),
    )
    metadata_obj.create_all(engine)

    sql_database = SQLDatabase(engine, include_tables=["city_stats"])
    from sqlalchemy import insert

    rows = [
        {"city_name": "Toronto", "population": 2930000, "country": "Canada"},
        {"city_name": "Tokyo", "population": 13960000, "country": "Japan"},
        {"city_name": "Chicago", "population": 2679000, "country": "United States"},
        {"city_name": "Seoul", "population": 9776000, "country": "South Korea"},
    ]
    for row in rows:
        stmt = insert(city_stats_table).values(**row)
        with engine.begin() as connection:
            cursor = connection.execute(stmt)

    # view current table
    stmt = select(
        city_stats_table.c.city_name,
        city_stats_table.c.population,
        city_stats_table.c.country,
    ).select_from(city_stats_table)

    with engine.connect() as connection:
        results = connection.execute(stmt).fetchall()
        print(results)

    from sqlalchemy import text

    with engine.connect() as con:
        rows = con.execute(text("SELECT city_name from city_stats"))
        for row in rows:
            print(row)

    from llama_index.core.query_engine import NLSQLTableQueryEngine

    # 定义你的LLM
    llm = Ollama(model="pxlksr/defog_sqlcoder-7b-2:Q8")
    llm.temperature = 0.2
    llm.base_url = "http://1.92.64.112:11434"

    print(datetime.datetime.now())
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, tables=["city_stats"], llm=llm
    )
    query_str = "Which city has the highest population?"
    response = query_engine.query(query_str)
    print(response)
    display(Markdown(f"<b>{response}</b>"))
    print(datetime.datetime.now())