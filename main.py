from website import create_app
from flask import Flask, render_template, request
import pandas as pd

app = create_app()

movies_df = pd.read_csv('inputs\movies.csv', encoding = 'ISO-8859-1', usecols=range(3))
movie_list = movies_df['Name'].values.tolist()

predictions = pd.read_csv('inputs\predictions5264.csv')

year_list = [str(i) for i in range(2020, 1899, -1)]

@app.route('/', methods=['GET', 'POST'])
def dropdown():
    selected_movie = None
    recommendation = None
    recs = None
    if request.method == 'POST':
        minyear = request.form.get('minyear')
        maxyear = request.form.get('maxyear')

        selected_movie = request.form.get('movies')
        index = movies_df[movies_df['Name'] == selected_movie]['Id'].iloc[0]
        pred_list = predictions[predictions['Id'] == index].values.tolist()[0][1:]

        recs = []
        for i in pred_list:
            if i == index:
                continue
            if len(recs) == 10:
                break
            year = int(float(movies_df[movies_df['Id'] == i]['Year'].iloc[0]))
            if year >= int(minyear) and year <= int(maxyear):
                recs.append(movies_df[movies_df['Id'] == i]['Name'])
        
        recs = [i.values[0] for i in recs]
        recs = [str(i+1) + ". " + recs[i] for i in range(len(recs))]
        recs = "\n".join(recs)

    return render_template('index.html', movie_list=movie_list, recommendation=recs, year_list=year_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)