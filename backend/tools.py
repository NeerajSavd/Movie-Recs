from smolagents import tool
import pandas as pd
import requests
from bs4 import BeautifulSoup

@tool
def recommend(movie: str, min_year:str = "1900", max_year: str = "2023") -> str:
    """
    Recommend movies based on the given movie name and year range.
    Args:
        movie (str): The name of the movie to base recommendations on.
        min_year (str): The minimum year for the recommendations.
        max_year (str): The maximum year for the recommendations.
    Returns:
        str: A string of 10 recommended movie titles.
    """
    movies_df = pd.read_csv('backend/inputs/movies.csv', encoding = 'ISO-8859-1', usecols=range(3))
    predictions = pd.read_csv('backend/inputs/predictions5264.csv')

    try:
        index = movies_df[movies_df['Name'] == movie]['Id'].iloc[0]
    except:
        return "Movie not found in the database."
    pred_list = predictions[predictions['Id'] == index].values.tolist()[0][1:]

    recs = []
    for i in pred_list:
        if i == index:
            continue
        if len(recs) == 10:
            break
        year = int(float(movies_df[movies_df['Id'] == i]['Year'].iloc[0]))
        if year >= int(min_year) and year <= int(max_year):
            recs.append(movies_df[movies_df['Id'] == i]['Name'])
    
    recs = [i.values[0] for i in recs]
    recs = [str(i+1) + ". " + recs[i] for i in range(len(recs))]
    recs = "\n".join(recs)
    
    return recs

@tool
def trending() -> str:
    """
    Fetch the top 10 trending movies from IMDb.
    No Args.
    Returns:
        str: A string containing the titles and ratings of the top 10 trending movies.
    """
    url = "https://www.imdb.com/chart/moviemeter/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")
    movies = []
    movie_items = soup.select(".ipc-metadata-list-summary-item")[:10]

    for movie in movie_items:
        title_element = movie.select_one(".ipc-title__text")
        rating_element = movie.select_one(".ipc-rating-star")

        movies.append({
            "title": title_element.get_text(strip=True) if title_element else "N/A",
            "rating": rating_element.get_text(strip=True) if rating_element else "N/A"
        })
    return str(movies)