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

def main():

    #############
    # Main page #
    #############

    options = ['Home','Recommender', 'Stop']
    choice = st.sidebar.selectbox("Menu",options, key = '1')

    if ( choice == 'Home' ):
      st.title("Welcome to the movie recommender!")
      st.image('./images/cinema.jpeg')
      pass

    elif ( choice == 'Recommender' ):
      recommender()
      pass

    else:
      st.stop()


main()
