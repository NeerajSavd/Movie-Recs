from smolagents import CodeAgent, LiteLLMModel
from smolagents import DuckDuckGoSearchTool
from tools import recommend, trending

model = LiteLLMModel(
    model_id="openrouter/deepseek/deepseek-chat-v3-0324:free",
    api_key="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",
    temperature=0.5,
    max_tokens=500
)

tools = [recommend, trending, DuckDuckGoSearchTool()]

agent = CodeAgent(tools=tools, model=model, max_steps=10)

prompt = """
Your task is to recommend five movies based on user input.
Use multiple tools to gather information and provide a comprehensive answer.
Provide the IMDB rating of the movies you recommend.
Make sure to include the year of release and a brief description of each movie.
Use the following format for your response:
{
    "movie_title": {
        "rating": "IMDB rating",
        "year": "Year of release",
        "description": "Brief description of the movie"
    },
    ...
}
"""
query = "I like The Godfather and Pulp Fiction. What are other old crime movies I should watch?"

response = agent.run(task=prompt+"\n"+query, max_steps=10)
print(response)