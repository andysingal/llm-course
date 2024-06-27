import os
from exa_py import Exa
from langchain.agents import tool

class ExaSearchToolSet():
    
    @tool
    def search(query:str):
        """Search for a webpage based on the query"""
        return ExaSearchToolSet._exa().search(f"{query}", use_autoprompt=True, num_results=3)
    @tool
    def find_similar(url: str):
        """Search for a webpages similar to a given URL. 
        The url passed in should be a URL returned from 'search'.
        """
        return ExaSearchToolSet._exa().find_similar(url, num_results=3)
    
    @tool
    def get_contents(ids: str):
        """Get the contents of a webpage
        The ids must be ppassed in as a list, a list of ids returned from 'search'.
        """
        # print("ids from params:",ids)
        ids = eval(ids)
        # print("eval ids:",ids)
        
        contents = str(ExaSearchToolSet._exa().get_contents(ids))
        print("contents:",contents)
        contents = contents.split("URL:")
        contents= [content[:1000] for content in contents]
        return "\n\n".join(contents)
    
    def tools():
        return [
            ExaSearchToolSet.search,
            ExaSearchToolSet.find_similar,
            ExaSearchToolSet.get_contents
        ]
    
    def _exa():
        return Exa(api_key=os.environ.get('EXA_API_KEY'))
            