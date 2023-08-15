from website import create_app
from flask import Flask, render_template, request
import pandas as pd

app = create_app()

movies_df = pd.read_csv('inputs\movies.csv')
movie_list = movies_df['Name'].values.tolist()

predictions = pd.read_csv('inputs\predictions.csv')

@app.route('/', methods=['GET', 'POST'])
def dropdown():
    selected_movie = None
    recommendation = None
    if request.method == 'POST':
        selected_movie = request.form.get('movies')
        index = movies_df[movies_df['Name'] == selected_movie].index[0]
        recommendation = predictions.iloc[index].tolist()[1:]
        r_list = zip(range(1,11), recommendation)
        r_list = [str(i) + '. ' + str(j) for i, j in r_list]
        recommendation = "\n".join(r_list)

    return render_template('index.html', movie_list=movie_list, recommendation=recommendation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)