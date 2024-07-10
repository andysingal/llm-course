from dotenv import load_dotenv
##to load credentials
load_dotenv()

import os
omdb_api_key = os.getenv('OMDB_API_KEY')

import omdb
omdb.set_default('apikey', omdb_api_key)

## Langchain imports
from langchain_community.tools import tool

class OmdbAPI():

  @tool("Movie_Info_By_Title_Year")
  def get_movie_info_by_title(data):
    """Call this tool to get information about a movie if you have its title. Optionally you can also specify a movie's year.
       The input to this tool is a movie title. Year can also be optionally specified. If year is specified it must be separated by pipe
       Example if the user is look True Grit then input should be `True%20Grit`. Represent space as %20
       Example if the user is look True Grit movie from 1969 then input should be `True%20Grit|1969`. Represent space as %20. Separate year by |
       The output from this tool will be information on title, plot, director and tomato meter rating of the movie that best matches
    """
    try:
      year = None
      if '|' in data:
        title, year = data.split('|')
      else:
        title = data
      title = title.replace('%20', ' ')
      if year:
        result = omdb.get(title=title, year=year, fullplot=True, tomatoes=True)
      else:
        result = omdb.get(title=title, fullplot=True, tomatoes=True)
      
      return result
    except Exception as e:
      print(e)
      return "Error with the input format for the tool."
    

  @tool("Search_Movie")
  def search_movie(data):
    """Call this tool to search for a movie based on search string. The input to the tool is a search string.
       The output from the tool is all the results that match the search criteria
       Example if the user is look for a movie Naruto, then data=Naruto
    """
    try:
      result = omdb.search_movie(data)
      
      return result
    except Exception as e:
      print(e)
      return "Error with the input format for the tool."
  
  @tool("Search_Series")
  def search_series(data):
    """Call this tool to search for a TV series based on search string. The input to the tool is a search string.
       The output from the tool is all the results that match the search criteria
       Example if the user is look for a TV series called Friends, then data=Friends
    """
    try:
      result = omdb.search_series(data)
      
      return result
    except Exception as e:
      print(e)
      return "Error with the input format for the tool."
    