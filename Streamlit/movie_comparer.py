import streamlit as st
from PIL import Image


def movie_comparer():
    import pandas as pd
    import random
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import numpy as np
    from matplotlib.ticker import FuncFormatter
    import plotly.express as px
    import time
    import requests
    from PIL import Image


    secrets_file = open("../secrets.txt","r")
    string = secrets_file.read()
    api_key = string

    st.title('Still cannot decide between two movies?')

    st.image('./images/curtain.jpg')
    st.markdown("Picture from https://www.vecteezy.com/free-photos")
    films = pd.read_csv('../films_NaNs_treated.csv')
    films_non_treated = pd.read_csv('../rotten_tomatoes_movies.csv')

    def get_title_from_id(x):
        title = films[films['id'] == x].values[0][2]
        return title

    def generate_youtube_search_url(movie_title):
        query = '+'.join(movie_title.split())
        youtube_url = f"https://www.youtube.com/results?search_query={query}+trailer"
        return youtube_url


    def get_id_from_input(x):
        x = x.lower()
        time.sleep(5)
        base_url = 'http://www.omdbapi.com/'
        params = {
        't': x,  
        'apikey': api_key,               
        }
        
        for retry in range(5):
            try:
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    movie_data = response.json()  
                    st.write('I am going to garther data for ', movie_data['Title'], ' from ', movie_data['Year'], ' by ', movie_data['Director'])
                    break
                else:
                    print('API request failed with status code:', response.status_code)
            except requests.ConnectionError:
                print('connection error, will retry')
                time.sleep(12)
        
        matching_titles = films[(films['title'].str.lower() == x) & (films['director'].str.lower() == movie_data['Director'].lower())]

        if not matching_titles.empty:
            return matching_titles.iloc[0]['id']
        else:
            return None

        def generate_youtube_search_url(movie_title):
            query = '+'.join(movie_title.split())
            youtube_url = f"https://www.youtube.com/results?search_query={query}+trailer"
            return youtube_url

    def get_link_and_extras_from_result(x):
        time.sleep(5)
        base_url = 'http://www.omdbapi.com/'
        params_extra = {
        't': x,  
        'apikey': api_key,               
        }
        
        print(params_extra)

        for retry in range(5):
            try:
                response_extra = requests.get(base_url, params=params_extra)
                if response_extra.status_code == 200:
                    movie_data = response_extra.json() 
                    return movie_data
            except requests.ConnectionError:
                print('API request for extra info failed, will retry')
                time.sleep(10)

    def show_more_info(x):
        st.write('Year: ', x[0])
        st.write('Director: ', x[1])
        st.write('Plot: ', x[2])
        st.write('Language(s): ', x[3])
        st.image(x[4], caption='Movie Poster')

    def compare_two_movies(title1, title2):

        st.image(title1['Poster'], caption=title1['Title'])
        st.image(title2['Poster'], caption=title2['Title'])

        if int(title1['Year']) == int(title2['Year']):
            st.write(f"{title1['Title']} and {title2} were both released in {title1['Year']}.")
        elif int(title1['Year']) < int(title2['Year']):
            st.write(f"{title2['Title']} is more recent than {title1['Title']}. {title1['Title']} was released in {title1['Year']}, while {title2['Title']} was released in {title2['Year']}.")
        else:
            st.write(f"{title1['Title']} is more recent than {title2['Title']}. {title2['Title']} was released in {title2['Year']}, while {title1['Title']} was released in {title1['Year']}.")

        runtime1 = int(title1['Runtime'].split()[0])  
        runtime2 = int(title2['Runtime'].split()[0])

        if runtime1 == runtime2:
            st.write(f"{title1['Title']} and {title2['Title']} have the same runtime of {runtime1} minutes.")
        elif runtime1 < runtime2:
            st.write(f"{title1['Title']} has a shorter runtime ({runtime1} minutes) compared to {title2['Title']} ({runtime2} minutes).")
        else:
            st.write(f"{title2['Title']} has a shorter runtime ({runtime2} minutes) compared to {title1['Title']} ({runtime1} minutes).")

        imdb_rating1 = float(title1['imdbRating'])
        imdb_rating2 = float(title2['imdbRating'])

        if imdb_rating1 == imdb_rating2:
            st.write(f"{title1['Title']} and {title2['Title']} have the same IMDb rating of {imdb_rating1}.")
        elif imdb_rating1 > imdb_rating2:
            st.write(f"{title1['Title']} has a higher IMDb rating ({imdb_rating1}) compared to {title2['Title']} ({imdb_rating2}).")
        else:
            st.write(f"{title2['Title']} has a higher IMDb rating ({imdb_rating2}) compared to {title1['Title']} ({imdb_rating1}).")

        try:
            ratings1 = title1['Ratings']
            ratings2 = title2['Ratings']

            for i in range(len(ratings1)):
                if i < len(ratings2):
                    rating1 = ratings1[i]['Value']
                    rating2 = ratings2[i]['Value']

                    source = ratings1[i]['Source']

                    if rating1 == rating2:
                        st.write(f"{title1['Title']} and {title2['Title']} have the same rating at {source}: {rating1}.")
                    elif rating1 > rating2:
                        st.write(f"{title1['Title']} has a higher rating at {source} ({rating1}) compared to {title2['Title']} ({rating2}).")
                    else:
                        st.write(f"{title2['Title']} has a higher rating at  {source} ({rating2}) compared to {title1['Title']} ({rating1}).")
                else:
                    st.write(f"{title1['Title']} has a rating at {source} ({ratings1[i]['Value']}), but {title2['Title']} does not have this rating.")
        except:
            st.write('Cannot compare other ratings')
        
        st.write('You might find the trailer of ', title1['Title'], ' here: ', generate_youtube_search_url(title1['Title']))
        st.write('You might find the trailer of ', title2['Title'], ' here: ', generate_youtube_search_url(title2['Title']))

    def movie_comparer_function():
        film1 = st.text_input('First film you are considering of watching:')
        film2 = st.text_input('Second film you are considering of watching:')
        if film1 and film2:
            movie_id1 = get_id_from_input(film1)
            movie_id2 = get_id_from_input(film2)
            moreinfo1 = get_link_and_extras_from_result(movie_id1)
            moreinfo2 = get_link_and_extras_from_result(movie_id2)
            if moreinfo1['Response'] == 'False' and moreinfo2['Response'] == 'False':
                st.write('Cannot find info for both movies.', ' please, try with other titles')
            elif moreinfo1['Response'] == 'False':
                st.write(f'Cannot find info for {film1}.', ' please, try with another title')
            elif moreinfo2['Response'] == 'False':
                st.write(f'Cannot find info for {film2}.', ' please, try with another title')
            else:
                compare_df = pd.DataFrame({film1: moreinfo1, film2: moreinfo2})
                st.write(compare_df)
                compare_two_movies(moreinfo1, moreinfo2)


    movie_comparer_function()
