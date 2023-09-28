###############################
# This program lets you       #
# - Create a dashboard        #
# - Evevry dashboard page is  #
# created in a separate file  #
###############################

# Python libraries
import streamlit as st
from PIL import Image

# User module files
#from ml import ml
from recommender import recommender
from advanced_recommender import advanced_recommender
from insights import insights
from movie_comparer import movie_comparer

def main():

    #############
    # Main page #
    #############

    options = ['Home', 'Insights','Basic Recommender', 'Advanced Recommender', 'Movie Comparer', 'Stop']
    choice = st.sidebar.selectbox("Menu",options, key = '1')

    if ( choice == 'Home' ):
      st.title("Welcome to the movie recommender!")
      st.image('./images/cinema.jpeg')
      pass

    elif ( choice == 'Basic Recommender' ):
      recommender()
      pass

    elif ( choice == 'Advanced Recommender' ):
      advanced_recommender()
      pass

    elif ( choice == 'Insights' ):
      insights()
      pass

    elif ( choice == 'Movie Comparer' ):
      movie_comparer()
      pass

    else:
      st.stop()


main()
