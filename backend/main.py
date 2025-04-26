from flask import Flask, request, jsonify
from smolagents import CodeAgent, LiteLLMModel
from smolagents import DuckDuckGoSearchTool
from tools import recommend, trending, time
import os
from dotenv import load_dotenv
from flask_cors import CORS
import json
import re

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'awesome'
    return app
app = create_app()
CORS(app)

load_dotenv()
openrouter_key = os.getenv("OPENROUTER_API_KEY")

model = LiteLLMModel(
    model_id="openrouter/deepseek/deepseek-chat-v3-0324:free",
    api_key=openrouter_key,
    temperature=0.5,
    max_tokens=500
)

tools = [trending, DuckDuckGoSearchTool(), time]

agent = CodeAgent(tools=tools, model=model, max_steps=10)

@app.route('/recommend', methods=['POST'])
def recommend():
    prompt = """
    Your task is to recommend five movies based on user input.
    Use multiple tools to gather information and provide a comprehensive answer.
    Provide the IMDB rating of the movies you recommend.
    Try to recommend movies with a rating of 7 or higher if possible.
    Make sure to include the year of release and provide a reason for why you are recommending each movie.
    Do not spoil the plot of the movies.
    
    Use the following format for your response. The Final output should ONLY be a JSON object:
    {"movie_title": {"rating": "IMDB rating", "year": "Year of release", "description": "Brief description of the movie"},...}
    Make sure to not include any other text in the response and use double quotes for the keys and values.
    Start the response with a '{' and end with a '}'.
    """
    query = request.form.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    response = agent.run(task=prompt+"\n"+query, max_steps=2)
    # response = '{"Goodfellas": {"rating": "8.7", "year": "1990", "description": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen and his mob partners Jimmy Conway and Tommy DeVito."}, "Casino": {"rating": "8.2", "year": "1995", "description": "A tale of greed, deception, money, power, and murder occur between two best friends: a mafia enforcer and a casino executive, compete against each other over a gambling empire, and over a fast-living and fast-loving socialite."}, "Scarface": {"rating": "8.3", "year": "1983", "description": "In 1980 Miami, a determined Cuban immigrant takes over a drug cartel and succumbs to greed."}, "Reservoir Dogs": {"rating": "8.3", "year": "1992", "description": "When a simple jewelry heist goes horribly wrong, the surviving criminals begin to suspect that one of them is a police informant."}, "The Untouchables": {"rating": "7.9", "year": "1987", "description": "During the era of Prohibition in the United States, Federal Agent Eliot Ness sets out to stop ruthless Chicago gangster Al Capone."}}'
    print(response)
    print(type(response))
    json_match = re.search(r'```(.*?)```', response, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
        try:
            python_obj = json.loads(json_str)
            print("Valid JSON parsed successfully")
        except json.JSONDecodeError:
            print("Invalid JSON, attempting repair...")
            try:
                from json_repair import repair_json
                repaired_json = repair_json(json_str)
                python_obj = json.loads(repaired_json)
                print("JSON repaired successfully")
            except:
                print("Failed to repair JSON")
                python_obj = None
    else:
        print("No JSON found in the response")
        return jsonify({"error": "No JSON found in the response"}), 400
    if python_obj:
        print("Parsed JSON object:")
        print(python_obj)

    return jsonify({"response": python_obj}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)