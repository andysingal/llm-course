import os
from typing import Dict, Optional

from IPython.display import Markdown, display
from llama_index.core import PromptTemplate, Settings
from llama_index.core.indices.query.query_transform.base import BaseQueryTransform
from llama_index.core.prompts.base import BasePromptTemplate
from llama_index.core.prompts.mixin import PromptDictType
from llama_index.core.prompts.prompt_type import PromptType
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import QueryBundle
from llama_index.core.service_context_elements.llm_predictor import LLMPredictorType
from llama_index.llms.openai import OpenAI

from util.helpers import get_weather

HYDE_TMPL = (
    "Please write a passage to answer the question\n"
    "Try to include as many key details as possible.\n"
    "-----------------------------------\n"
    "{context_str}\n"
    "-----------------------------------\n"
    'Passage:"""\n'
)

DEFAULT_HYDE_PROMPT = PromptTemplate(HYDE_TMPL, prompt_type=PromptType.SUMMARY)


class VerboseHyDEQueryTransform(BaseQueryTransform):
    """Hypothetical Document Embeddings (HyDE) query transform.

    It uses an LLM to generate hypothetical answer(s) to a given query,
    and use the resulting documents as embedding strings.

    As described in `[Precise Zero-Shot Dense Retrieval without Relevance Labels]
    (https://arxiv.org/abs/2212.10496)`
    """

    def __init__(
        self,
        llm: Optional[LLMPredictorType] = None,
        hyde_prompt: Optional[BasePromptTemplate] = None,
        include_original: bool = True,
        verbose: Optional[bool] = False,
    ) -> None:
        """Initialize HyDEQueryTransform.

        Args:
            llm_predictor (Optional[LLM]): LLM for generating
                hypothetical documents
            hyde_prompt (Optional[BasePromptTemplate]): Custom prompt for HyDE
            include_original (bool): Whether to include original query
                string as one of the embedding strings
        """
        super().__init__()

        self._llm = llm or Settings.llm
        self._hyde_prompt = hyde_prompt or DEFAULT_HYDE_PROMPT
        self._include_original = include_original
        self._verbose = verbose

    def _get_prompts(self) -> PromptDictType:
        """Get prompts."""
        return {"hyde_prompt": self._hyde_prompt}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "hyde_prompt" in prompts:
            self._hyde_prompt = prompts["hyde_prompt"]

    def _run(self, query_bundle: QueryBundle, metadata: Dict) -> QueryBundle:
        """Run query transform."""
        query_str = query_bundle.query_str
        hypothetical_doc = self._llm.predict(self._hyde_prompt, context_str=query_str)
        if self._verbose:
            display(
                Markdown(
                    f"<b>[VerboseHyDEQueryTransform]<b> Generated hypothetical document: {str(hypothetical_doc)}\n\n-------------------\n\n"
                )
            )
        embedding_strs = [hypothetical_doc]
        if self._include_original:
            embedding_strs.extend(query_bundle.embedding_strs)
        return QueryBundle(
            query_str=query_str,
            custom_embedding_strs=embedding_strs,
        )


class WeatherQueryEngine(CustomQueryEngine):
    verbose: Optional[bool] = False
    llm: Optional[OpenAI] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")


    def custom_query(self, query_str: str) -> str:
        return "Not implemented yet."

    async def acustom_query(self, query_str: str) -> str:
        cities_prompt = PromptTemplate(
            """Given the following query make a comma separated list of the cities mentioned in it
        Query: {query_str}
        Cities:"""
        )

        if self.verbose:
            display(Markdown("<b>[WeatherQueryEngine]</b> Determining which cities..."))
        cities = self.llm.complete(cities_prompt.format(query_str=query_str))
        if self.verbose:
            display(Markdown(f"<b>[WeatherQueryEngine]</b> Cities: {cities}"))
        context = [await get_weather(city) for city in str(cities).split(",")]

        if self.verbose:
            for weather in context:
                display(Markdown(f"<b>[WeatherQueryEngine]</b> {weather}"))

        res_prompt = PromptTemplate(
            """You're a helpful assistant that helps answer questions using weather forecasts as context
        Question: {query_str}
        
        Forecasts: {context}
        
        Answer:""",
        )
        res = self.llm.complete(
            res_prompt.format(context="\n".join(context), query_str=query_str)
        )
        return str(res)



REWRITE_PROMPT_TEMPLATE = PromptTemplate(
    """You're a helpful AI assistant that helps people learn about different topics. 
Given the following query: 
-----------------------------------
{query_str},
-----------------------------------

Extract each question from the query and categorize it into one of the following categories separated into key and description pairs:
-----------------------------------
{categories_with_descriptions}
-----------------------------------

Your output should a comma separated list of questions with their corresponding category prepended in square brackets.
Example: 
-----------------------------------
"What is the capital of France? And who is Prince" -> "[Geography]What is the capital of France?,[People]Who is Prince?"
-----------------------------------
Answer:
"""
)

QA_PROMPT = PromptTemplate(
    """You are a helpful assistant that answers questions. 

Question: {question}

Context: 
-----------------------------------
{context}
-----------------------------------

Answer:
"""
)

VALIDATE_PROMPT = PromptTemplate(
    """You are a helpful AI assistant that validates, corrects and combines information in answers to a query
Query:
-----------------------------------
{query_stry}
-----------------------------------

Answers:
-----------------------------------
{answers}
-----------------------------------

Validate, correct and combine the answers to provide a single coherent response.
Answer:    
"""
)


class RewriteRetrieveReadQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""

    categories: list[str]
    descriptions: list[str]
    retrievers: Dict[str, BaseRetriever]
    llm: OpenAI = Settings.llm
    verbose: bool = False

    def custom_query(self, query_str: str):
        categories_with_descriptions = "\n".join(
            [
                f"{category} - {description}"
                for category, description in zip(self.categories, self.descriptions)
            ]
        )
        rewrite_prompt = REWRITE_PROMPT_TEMPLATE.format(
            query_str=query_str,
            categories_with_descriptions=categories_with_descriptions,
        )
        rewrite_res = self.llm.complete(rewrite_prompt)

        questions = str(rewrite_res).replace('"', "").split(",")
        if self.verbose:
            print("Questions:", questions)

        answers = []
        for question in questions:
            category, q = question[1:].split("]")
            if self.verbose:
                print("\n\nRetrieving answer for question:", q)
                print("Using category:", category)
            nodes = self.retrievers[category].retrieve(q)
            if self.verbose:
                print("Retrieved nodes:", nodes)
            context = "\n\n".join([n.node.get_content() for n in nodes])
            answer = self.llm.complete(QA_PROMPT.format(question=q, context=context))
            if self.verbose:
                print("Answer:", answer)
            answers.append(answer.text)
        if self.verbose:
            print("\n\nValidating answers")
        response = self.llm.complete(
            VALIDATE_PROMPT.format(query_stry=query_str, answers="\n".join(answers))
        )

        return str(response)
    

STEP_BACK_PROMPT_TMPL = PromptTemplate(
    """
    You are an expert at world knowledge. 
    Your task is to step back and paraphrase a question to a more generic step-back question, which is easier to answer. 
    
    Here are a few examples:
    
    Human: Could the members of The Police perform lawful arrests?
    AI: what can the members of The Police do?
    
    Human: Jan Sindel’s was born in what country?
    AI: what is Jan Sindel’s personal history? 
    
    Question: {query_str}
    Step-back question:"""
)


RESULT_PROMPT_TMPL = PromptTemplate(
    """You are an expert of world knowledge. 
I am going to ask you a question. 
Your response should be comprehensive and not contradicted with the following context if they are relevant. 
Otherwise, ignore them if they are not relevant.

{normal_context}
{step_back_context}

Original Question: {query_str}
Answer:"""
)

class VerboseStepBackQueryEngine(CustomQueryEngine):
    retriever: BaseRetriever
    llm: Optional[OpenAI] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4-turbo")
    verbose: Optional[bool] = False
    include_original: Optional[bool] = True

    def custom_query(self, query_str: str):
        
        step_back_prompt = STEP_BACK_PROMPT_TMPL.format(query_str=query_str)
        step_back_res = self.llm.complete(step_back_prompt)
        if self.verbose:
            print("\n\nStep-back Question:\n\n", step_back_res, "\n\n")
        step_back_context = self.retriever.retrieve(step_back_res.text)
        if self.verbose:
            print("\n\nStep-back Context:\n\n", step_back_context, "\n\n")
        
        if self.include_original:
            normal_context = self.retriever.retrieve(query_str)
            if self.verbose:
                print("\n\nNormal Context:\n\n", normal_context, "\n\n")
        else:
            normal_context = []
        
        result_prompt = RESULT_PROMPT_TMPL.format(
            normal_context="\n".join([n.node.get_content() for n in normal_context]),
            step_back_context="\n".join([n.node.get_content() for n in step_back_context]),
            query_str=query_str,
        )
        response = self.llm.complete(result_prompt)        
        
        return str(response)
