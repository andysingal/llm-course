### Reranker using mixedbread-ai/mxbai-rerank-v2

```py
from mxbai_rerank import MxbaiRerankV2

class   MxbaiReranker (BaseReranker):
     def  __init__ (
            self,
            model_name: str　=　"mixedbread-ai/mxbai-rerank-base-v2" ,
        ):
        self.model = MxbaiRerankV2(model_name, device= "cpu" )

    def  rerank (
            self,
            query: str ,
            documents: list [ str ],
            return_documents: bool　=　True ,
            top_n: int　=　3 ,
        ) -> list [RankResult]:
        results = self.model.rank(
                        query,
                        documents,
                        return_documents=return_documents,
                        top_k=top_n,
                    )
        return   results

mxbai_reranker = MxbaiReranker()
```

### Reranker using Alibaba-NLP/gte-multilingual

```py
import torch
 from transformers import AutoModelForSequenceClassification, AutoTokenizer

class  AlibabaReranker (BaseReranker):
     def   __init__ (
            self,
            model_name: str   =   "Alibaba-NLP/gte-multilingual-reranker-base"
        ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
                        model_name,
                        trust_remote_code= True ,
                        torch_dtype=torch.float32,
                    )
        self.model = self.model.to( "cpu" )
        self.model.eval()

def  rerank (
        self,
        query: str ,
        documents: list [ str ],
        return_documents: bool   =   True ,
        top_n: int   =   3 ,
    ) -> list [RankResult]:
    pairs = [[query, doc] for   doc   in   documents]
     with   torch.no_grad():
        inputs = self.tokenizer(pairs, padding= True , truncation= True , return_tensors= 'pt' , max_length= 512 ).to( "cpu" )
        scores = self.model(**inputs, return_dict= True ).logits.view(- 1 , ).float()
    index =   0
    rank_results = []
    for p, s in  zip (pairs, scores):
        rank_results.append(
            RankResult(
                index=index,
                score=s.item(),
                document=p[ 1 ] if   return_documents   else   "" ,
            )
        )
        index +=   1 
    rank_results.sort(key= lambda   x: x.score, reverse rank= True )
     return   rank_results[:top_n]

alibaba_reranker = AlibabaReranker()
```

### Reranking with OpenAI GPT (gpt-4.1-mini)

```py
import   os

from langchain_core.output_parsers import StrOutputParser
 from langchain_core.prompts import ChatPromptTemplate
 from langchain_openai import ChatOpenAI

API_KEY =   "XXXXX" 
os.environ[ "OPENAI_API_KEY" ] = API_KEY

RERANK_PROMPT = """You are given a text that is a query and a text_list containing multiple texts. 
Compare the text in text_list with the query, and sort the text in text_list by how closely it matches the query.

***Conditions*** 
1. Return a list of text indexes and scores sorted by the similarity of the content to the query. 
2. The score should be in the range of 0.0 to 1.0, and the closer the content to the query, the higher the score. 
"""

class  RerankedIndex (BaseModel):
    index: list [ int ] = Field(
        default=[],
        description= "A list of text indexes ordered by their content's proximity to the query."
    )
    score: list [ float ] = Field(
        default=[],
        description= "A list of scores for text ordered by how closely it matches the query."
    )

class  OpenaiReranker (BaseReranker):
     def　__init__(
            self,
            model_name: str = "gpt-4.1-mini" ,
        ):
        self.model = ChatOpenAI(
                        model=model_name,
                        max_tokens= 1000 ,
                         # temperature=0.0, 
                        top_p= 0.01 ,
                        seed= 42 ,
                    )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ( "system" , RERANK_PROMPT),
                ( "human" , "query: '{query}' \n text_list: '{text_list}'" ),
            ])
        self.chain = self.prompt | self.model.with_structured_output(RerankedIndex)

    def  _rerank_text (
            self,
            query: str ,
            text_list: str ,
        ) -> int :
        res = self.chain.invoke({ "query" : query, "text_list" : text_list})
         return   res

    def  rerank (
            self,
            query: str ,
            documents: list [ str ],
            return_documents: bool   =   True ,
            top_n: int   =   3 ,
        ) -> list [RankResult]:
        text_list = [f "{i}. {doc}"   for   i, doc   in   enumerate (documents)]
        text_list =   " \n " .join(text_list)
        res = _rerank_text(query, text_list)
        index_score_pairs =   list ( zip (res.index, res.score))
        rank_results = []
        for   idx, score   in   index_score_pairs:
            rank_results.append(
                RankResult(
                    index=idx,
                    score=score,
                    document=documents[idx] if   return_documents   else   "" ,
                )
            )
        rank_results.sort(key= lambda   x: x.score, reverse= True )
         return   rank_results[:top_n]

openai_reranker = OpenaiReranker()
```

### Running Reranking

```py
test_query =   "Give me the first document."
test_documents = [
    "This is the first document." ,
     "This is the second document." ,
     "This is the third document." ,
     "This is the fourth document." ,
     "This is the fifth document." ,
    ]
res_mxbai = mxbai_reranker.rerank(test_query, test_documents, return_documents= True , top_n= 3 )
res_gte = alibaba_reranker.rerank(test_query, test_documents, return_documents= True , top_n= 3 )
res_openai = openai_reranker.rerank(test_query, test_documents, return_documents= True , top_n= 3 )
```
