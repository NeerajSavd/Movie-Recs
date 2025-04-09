import pandas as pd

movies_df = pd.read_csv('backend/inputs/movies.csv', encoding = 'ISO-8859-1', usecols=range(3))
movie_list = movies_df['Name'].values.tolist()
year = int(float(movies_df[movies_df['Id'] == 12277]['Year'].iloc[0]))
print(year)
year = int(float(movies_df[movies_df['Id'] == 13457]['Year'].iloc[0]))
print(year)

# in paris 12277
# creepier 13457
