import json
from typing import Any, Dict

from support_agent.state import AssistantGraphState, RequiredInformation


def verify_information(state: AssistantGraphState) -> Dict[str, Any]:
    EDEN_INDEX = 0
    required_information: RequiredInformation = state["required_information"]
    with open(
        "/Users/edenmarco/GithubProjects/langgraph-customer-support/db/profile.json",
        "r",
    ) as file:
        user_info = json.load(file)[EDEN_INDEX]
        if (
            user_info["secret"]["id"] == required_information.provided_id
            and user_info["secret"]["city_of_birth"]
            == required_information.provided_city_of_birth
            and user_info["secret"]["last_4_digits"]
            == required_information.provided_4_digits
            and required_information.provided_name
            == f"{user_info['first_name']} {user_info['last_name']}"
        ):
            print("Verification Success")
            return {"verified": True}

    print("Verification Failed")
    return {"verified": False}
