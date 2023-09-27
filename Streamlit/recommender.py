def recommender():
    # Import python modules
    import pandas as pd
    import random
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px

    st.title("Find out the next movie you will watch! ")

    st.image('./images/recommender.jpg')

    st.markdown("Picture from https://www.vecteezy.com/")

    films = pd.read_csv('../films_with_clusters.csv')


    def get_cluster_from_input(x):
        x = x.lower()
        matching_titles = films[films['title'].str.lower().str.contains(x, na=False)]

        if not matching_titles.empty:
            return matching_titles.iloc[0]['clusters']
        else:
            return None

    def get_recommendation_in_cluster(x):
        subset = films[films['clusters'] == x].head(10)
        subset = subset.sort_values(by='audienceScore', ascending=False)
        top_10_recommendations = subset.head(10)
        random_recommendations = random.sample(top_10_recommendations['title'].tolist(), 3)
        return random_recommendations


    def basic_recommender():
        user_input = st.text_input('Tell me a movie you like:')
        if user_input:
            cluster = get_cluster_from_input(user_input)
            if cluster is not None:
                recommendation = get_recommendation_in_cluster(cluster)
                st.write('Top 3 Recommendations:')
                for movie in recommendation:
                    st.write(movie)
            else:
                st.write('Movie not found or no recommendations available.')

    basic_recommender()

