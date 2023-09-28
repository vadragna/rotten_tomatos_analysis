# movie_recommender_comparer_project

Movie Comparer and Recommender Project

Data Sources: https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews?select=rotten_tomatoes_movies.csv by Andy Kriebel - https://www.omdbapi.com/

## Installations

pip install omdb
pip install streamlit

## Main Data Source:

- CSVs
  - rotten_tomatoes_movies.csv
    A comprehensive collection of data from Rotten Tomato. Each row corresponds to a specific movie.
  - rotten_tomatoes_movie_reviews.csv
    A comprehensive collection of reviews on Rotten Tomato. Each row corresponds to a movie review

## Main Folders

In the repository, you can find one main folder with the following Jupiter notebook files:

- film_db_cleaning.ipynb
- review_db_cleaning.ipynb
- Analysis.ipynb
- Clustering.ipynb

An other folder called 'Streamlit' - if you download the whole repository, you can run streamlit run deploy_model.py to use the movie recommenders and see the most useful insights from the data.

## Methodology

- Clustering: Movies are clustered into 12 different clusters based on certain criteria.
- Movie Recommender: The recommender uses a mixed approach, considering the number of positive reviews by reviewers and clustering.

## Components:

- Basic Recommender: use clustering
- Advanced Recommender: use mixed approach
- Movie Comparer: garther info from https://www.omdbapi.com/

## Future Improvements:

- Clustering can be further optimized.
- More advanced search featured can be added.
