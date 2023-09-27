def advanced_recommender():
    # Import python modules
    import pandas as pd
    import random
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import time
    import requests

    st.title("Not yet convinced? Try this! ")
    st.image('./images/pop_corn.jpg')
    st.markdown("Picture from https://www.vecteezy.com/")
    films = pd.read_csv('../films_with_clusters.csv')
    grouped_positive_reviews = pd.read_csv('../grouped_reviews.csv')

    secrets_file = open("../secrets.txt","r")
    string = secrets_file.read()
    api_key = string

    def get_title_from_id(x):
        title = films[films['id'] == x].values[0][2]
        return title
    
    def get_cluster_from_input(x):
        x = x.lower()  
        matching_titles = films[films['title'].str.lower().str.contains(x, na=False)]

        if not matching_titles.empty:
            return matching_titles.iloc[0]['clusters']
        else:
            return None

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
                    st.write('Searching for similiar movies to ', movie_data['Title'], ' from ', movie_data['Year'], ' by ', movie_data['Director'])
                    break
                else:
                    st.write('API request failed with status code:', response.status_code)
            except requests.ConnectionError:
                st.write('connection error, will retry')
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

    def from_id_get_other_films_reviews_by_other_authors(x):
        movie_id_count = {}  
        subset = grouped_positive_reviews[grouped_positive_reviews['id'] == x]
        
        for authors in subset['criticName']:
            parts = authors.split(',')
            
            for author in parts:
                subset2 = grouped_positive_reviews[grouped_positive_reviews['criticName'].str.contains(author)]           
                subset2 = subset2[subset2['id'] != x]
                
                for movie_id in subset2['id']:
                    if movie_id in movie_id_count:
                        movie_id_count[movie_id] += 1
                    else:
                        movie_id_count[movie_id] = 1
        
        sorted_items = sorted(movie_id_count.items(), key=lambda x: x[1], reverse=True)

        top_fourty_items = sorted_items[:40]
                
        return top_fourty_items

    def get_recommendation_in_cluster(x):
        subset = films[films['clusters'] == x].head(10)
        subset = subset.sort_values(by='audienceScore', ascending=False)
        top_10_recommendations = subset.head(10)  
        try:
            random_recommendations = random.sample(top_10_recommendations['title'].tolist(), 3)
            for recommendation in random_recommendations:
                st.write(recommendation)
                return recommendation
        except:
            st.write('could not find any recommendation for the inserted title')
    
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
                    return movie_data['Year'], movie_data['Director'], movie_data['Plot'], movie_data['Language'], movie_data['Poster']
            except requests.ConnectionError:
                print('API request for extra info failed, will retry')
                time.sleep(10)

    def show_more_info(x):
        st.write('Year: ', x[0])
        st.write('Director: ', x[1])
        st.write('Plot: ', x[2])
        st.write('Language(s): ', x[3])
        st.image(x[4], caption='Movie Poster')

    def better_recommender():
    
        user_input = st.text_input('Tell me a movie you like:')
        if user_input:
            movie_id = get_id_from_input(user_input)
            cluster = get_cluster_from_input(user_input)
            other_reviews_recommender = from_id_get_other_films_reviews_by_other_authors(movie_id)

            if not other_reviews_recommender:
                st.write('No similar movies found based on other reviews. You might like this from the same cluster: ')
                title = get_recommendation_in_cluster(cluster)
                try:
                    more_info = get_link_and_extras_from_result(title)
                    show_more_info(more_info)
                    st.write(generate_youtube_search_url(title))
                except:
                    st.write('Not extra info found')
            
            for other_reviews in other_reviews_recommender:
                movie_id = other_reviews[0]
                title = get_title_from_id(movie_id)
                matching_movies = films.loc[films['id'] == movie_id, 'clusters']       
                if not matching_movies.empty and matching_movies.values[0] == cluster:
                    st.write('Found a movie according to other reviewers:', title)
                    st.write('Found a movie according to other reviewers that matches also clusters:', title)
                    more_info = get_link_and_extras_from_result(title)
                    try:
                        show_more_info(more_info)
                        st.write(generate_youtube_search_url(title))
                    except:
                        st.write('No more info found: ')
                    return other_reviews
                else:
                    rec_title = get_title_from_id(other_reviews_recommender[0][0])
                    st.write('Recommendation based on other reviewers :', rec_title)
                    more_info = get_link_and_extras_from_result(rec_title)
                    show_more_info(more_info)
                    st.write(generate_youtube_search_url(rec_title))
                    st.write('You might also like these other movies from the same cluster: ')
                    title = get_recommendation_in_cluster(cluster)
                    try:
                        more_info = get_link_and_extras_from_result(title)
                        show_more_info(more_info)
                        st.write(generate_youtube_search_url(title))
                    except:
                        st.write('No more info found: ')
                    return 
    
    better_recommender()