import logging

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_cohere.chat_models import ChatCohere
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


def get_chat_model(model_provider: str, model_name: str) -> BaseChatModel:
    """
    Return a chat-based LLM model from the given `model_provider` with the given `model_name`.

    Args:
        model_provider (str): The provider of the chat-based LLM model.
        model_name (str): The name of the chat-based LLM model to use.

    Returns:
        ChatOllama: A chat-based LLM model.
    """
    assert model_provider in [
        'ollama',
        'cohere',
        'openai'
    ], f'Invalid model provider: {model_provider}'

    if model_provider == 'ollama':
        logger.info(f'Loading Ollama model: {model_name}')
        llm = ChatOllama(model=model_name, temperature=0.0)

    elif model_provider == 'cohere':
        logger.info(f'Loading Cohere model: {model_name}')
        llm = ChatCohere(model=model_name, temperature=0.0)

    elif model_provider == 'openai':
        logger.info(f'Loading OpenAI model: {model_name}')
        llm = ChatOpenAI(model=model_name, temperature=0.0)

    return llm

def run(model_provider: str, model_name: str, input: str):

    llm = get_chat_model(model_provider, model_name)
    output = llm.invoke(input)
    print(output.content)

if __name__ == '__main__':

    from fire import Fire
    from dotenv import load_dotenv, find_dotenv

    # Load the environment variables from my .env file
    load_dotenv(find_dotenv())

    Fire(run)