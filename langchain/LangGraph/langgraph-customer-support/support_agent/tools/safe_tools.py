import json
from typing import Any, Dict

from langchain_core.messages import AIMessage
from langchain_core.tools import tool


@tool
def get_info_from_db(name: str) -> Dict[str, Any]:
    """
    :return: A dictionary with all information about a person
    """

    with open(
        "/Users/edenmarco/GithubProjects/langgraph-customer-support/db/profile.json",
        "r",
    ) as file:
        users_info = json.load(file)

        for user_info in users_info:
            if f"{user_info['first_name']} {user_info['last_name']}" == name:
                return user_info
        raise ValueError(f"Couldn't find user {name} in DB")


safe_tools = [get_info_from_db]
