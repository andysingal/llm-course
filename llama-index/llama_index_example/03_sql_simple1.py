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
from llama_index.core import SQLDatabase, VectorStoreIndex, Settings
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

    # 定义你的LLM
    llm = Ollama(model="pxlksr/defog_sqlcoder-7b-2:Q8")
    llm.temperature = 0.2
    llm.base_url = "http://1.92.64.112:11434"

    from llama_index.core.indices.struct_store.sql_query import (
        SQLTableRetrieverQueryEngine,
    )
    from llama_index.core.objects import (
        SQLTableNodeMapping,
        ObjectIndex,
        SQLTableSchema,
    )

    # set Logging to DEBUG for more detailed outputs
    table_node_mapping = SQLTableNodeMapping(sql_database)
    table_schema_objs = [
        (SQLTableSchema(table_name="city_stats"))
    ]  # add a SQLTableSchema for each table

    from llama_index.core.embeddings import resolve_embed_model
    Settings.embed_model = resolve_embed_model("local:data/embed_model/bge-small-en-v1.5")
    obj_index = ObjectIndex.from_objects(
        table_schema_objs,
        table_node_mapping,
        VectorStoreIndex
    )
    print(datetime.datetime.now())
    query_engine = SQLTableRetrieverQueryEngine(
        sql_database, obj_index.as_retriever(similarity_top_k=1), llm=llm
    )
    query_str = "Which city has the highest population?"
    response = query_engine.query(query_str)
    print(response)
    display(Markdown(f"<b>{response}</b>"))
    print(datetime.datetime.now())