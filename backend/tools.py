from smolagents import tool
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

@tool
def recommend(movie: str, min_year: str = "1900", max_year: str = "2023") -> str:
    """
    Recommend movies based on the given movie name and year range.
    Args:
        movie (str): The name of the movie to base recommendations on.
        min_year (str): The minimum year for the recommendations.
        max_year (str): The maximum year for the recommendations.
    Returns:
        str: A string of 10 recommended movie titles.
    """
    movies_df = pd.read_csv('/Users/neeraj/Library/CloudStorage/OneDrive-Personal/Coding/Netflix/backend/inputs/movies.csv', encoding = 'ISO-8859-1', usecols=range(3))
    predictions = pd.read_csv('/Users/neeraj/Library/CloudStorage/OneDrive-Personal/Coding/Netflix/backend/inputs/predictions5264.csv')

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

@tool
def time() -> str:
    """
    Get the current date and time to provide context for the agent, such as holidays or events.
    No Args.
    Returns:
        str: A string containing the current date and time and upcoming holidays.
    """
    today = date.today()
    holidays_list = {
            date(today.year, 2, 14): "Valentine's Day",
            date(today.year, 3, 17): "St. Patrick's Day",
            date(today.year, 5, 5): "Cinco de Mayo",
            date(today.year, 7, 4): "Independence Day",
            date(today.year, 9, 4): "Labor Day",
            date(today.year, 10, 31): "Halloween",
            date(today.year, 11, 11): "Veterans Day",
            date(today.year, 11, 24): "Thanksgiving Day",
            date(today.year, 12, 25): "Christmas Day",
            date(today.year+1, 1, 1): "New Year's Day",
        }
    current_date = date.today()
    current_time = datetime.now().strftime("%H:%M")
    two_weeks_later = current_date + timedelta(weeks=2)
    holidays_within_two_weeks = [
        (date, name) for date, name in holidays_list.items() if current_date <= date <= two_weeks_later
    ]
    if not holidays_within_two_weeks:
        return f"Current date: {current_date}, Current time: {current_time}, No upcoming holidays within two weeks."
    return f"Current date: {current_date}, Current time: {current_time}, Holidays within two weeks: {holidays_within_two_weeks}."
    
    