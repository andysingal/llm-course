#!/usr/bin/python3
# encoding=utf-8

"""
    项目名称:  llamaindex_learn
    文件名称： 03_sql_simple.py
    功能描述： ..
    创建者：   lixinxin
    创建日期： 2024/3/14 13:47
"""

import os

import openai
from IPython.display import Markdown, display
from llama_index.core import SQLDatabase
from llama_index.llms.ollama import Ollama
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
)

from llama_index_service.util.excel_util import ExcelUtil

os.environ["OPENAI_API_KEY"] = "sk-.."
openai.api_key = os.environ["OPENAI_API_KEY"]

def read_excel(filename, sheet):
    res = []
    ex = ExcelUtil(filename)
    max_row = ex.get_max_row()
    head = []
    for j in range(max_row):
        i = j + 1
        if i == 1:
            head = ex.get_row_value(i)
            continue

        map = {}
        row = ex.get_row_value(i)
        for r in range(len(row)):
            map[head[r]] = row[r]
        print(i, " ", row)
        res.append(map)

    return head, res

if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:")
    metadata_obj = MetaData()

    sheet = 'Sheet1'
    filepath = './data/excel/test.xlsx'
    table_name = os.path.splitext(os.path.basename(filepath))[0]
    col_name, rows = read_excel(filepath, sheet)

    city_stats_table = Table(
        table_name,
        metadata_obj,
        Column("vin", String(16), primary_key=True),
        Column("库存类型", String(16), nullable=False),
        Column("是否上牌", String(16), nullable=False),
        Column("经销商编码", String(16), nullable=False),
        Column("经销商名称", String(16), nullable=False),
        Column("送达方", String(16)),
        Column("终端离线时长", Integer),
        Column("车联网实销状态", String(16), nullable=False),
        Column("TSP库存名称", String(16)),
        Column("DMS库存类型", String(16)),
        Column("SAP库存类型", String(16)),
        Column("车联网库存类型与（DMS库存类型是否匹配或者SAP库存类型）", String(16), nullable=False),
        Column("不一致原因", String(16)),
        Column("入中心库时间", String(16)),
        Column("库龄", String(16)),
    )
    metadata_obj.create_all(engine)

    sql_database = SQLDatabase(engine, include_tables=[table_name])
    from sqlalchemy import insert

    for row in rows:
        stmt = insert(city_stats_table).values(**row)
        with engine.begin() as connection:
            cursor = connection.execute(stmt)

    from sqlalchemy import text

    with engine.connect() as con:
        rows = con.execute(text("SELECT vin from " + table_name))
        for row in rows:
            print(row)

    from llama_index.core.query_engine import NLSQLTableQueryEngine

    # 定义你的LLM
    llm = Ollama(model="pxlksr/defog_sqlcoder-7b-2:Q8")
    llm.temperature = 0.2
    llm.base_url = "http://1.92.64.112:11434"

    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, tables=[table_name], llm=llm
    )
    query_str = "终端离线时长小于10的经销商名称分别是哪些"
    response = query_engine.query(query_str)
    print(response)
    display(Markdown(f"<b>{response}</b>"))