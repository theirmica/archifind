import folium
import requests
import pandas as pd

from IPython.display import HTML

import streamlit as st
import time
from streamlit_aggrid import AgGrid

#loading functions 
from distance_functions import get_user_location, filter_df, calculate_closest_locations, create_building_map

df = pd.read_csv("1200_buildings_ready_new.csv")

#style drop-down input
style_categories = pd.read_csv("styles_categories.csv")
style_categories.rename(
    index=lambda x: x+1,
    inplace=True
    )
Style_TITLES = ["---"] + list(style_categories['Category'].sort_values()) 

#type drop-down input
type_categories = pd.read_csv("types_categories.csv")
type_categories.rename(
    index=lambda x: x+1,
    inplace=True
    )
Type_TITLES = ["---"] + list(type_categories['Category'].sort_values())


##########################################################
# "Side Bar"
##########################################################

# sidebar
with st.sidebar:
    # title
    st.title("navigation")
    # blank space
    st.write("")
    # selectbox
    page = st.selectbox("where to go next?",
        [
            "archi find",
            "about",
            "appendix"
            ]
        )
    # blank space
    st.write("")
    # image
    st.image('_3240352.jpg') 
    
   


##########################################################
# architecture finder
##########################################################

if page == "archi find":
    
    # image
    st.image('archi_find.png')
    #title
    #st.title("archi find")
        
    #blank space
    st.write("")

    def main():
    
        st.write("This tool is designed to find the Top 5 closest buildings to you, based on walking distance.") 
        st.write("Type the name of the street and if possible the postcode of your startpoint.") 
        st.write("Please be aware, that currently only recommendations only work for **1200** buildings in **Berlin**.")
        user_location = st.text_input("I'm starting in: ")
        api_key = 'AIzaSyDR9lXqqtzp_JJCCmgS0m6a65Ot8KoDCQs'
            
        latitude, longitude = get_user_location(user_location, api_key)
        st.write("Cool, so these are your coordinates. Based on which we will calculate the closest buildings to you.")
        st.write(f"Latitude: {latitude}")
        st.write(f"Longitude: {longitude}")
            
        #blank space
        st.write("")
        
        #explaination
        st.write("Feel free to select any type or style that you want. Be aware, that some combinations might not contain enough buildings.")
        #drop-down style
        st.markdown("####")
        selected_type_category = st.selectbox("Select Building Type", Type_TITLES)
        
        #blank space
        st.write("")
        
        #drop-down type
        st.markdown("####")
        selected_style_category = st.selectbox("Select Architecture Style", Style_TITLES)

        #inserting number of buildings
        num_locations = st.number_input("Enter the number of locations you'd like to be displayed (max. 20)", min_value=1, max_value=20, step=1, value=5)
        
        #blank space
        st.write("")
            
        #search button
        recommend_button = st.button(label="SEARCH FOR BUILDINGS")

        #spinning bar design
        total_steps = 100
                
        st.markdown(
            """
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .spinner {
                display: inline-block;
                border: 4px solid rgba(0, 0, 0, 0.2);
                border-left-color: black;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                animation: spin 1s linear infinite;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        #Handling recommend button click
        try:
            if recommend_button:
                #st.write("Filtering DataFrame...")
                df_filtered = filter_df(df, selected_style_category, selected_type_category)
                
                #start of calculating progress spinner
               
                # Start spinning wheel animation
                spinner_message_placeholder = st.empty()
                spinner_placeholder = st.empty()
                spinner_message_placeholder.write(f"Calculating closest {num_locations} locations...")
                for _ in range(total_steps):
                    time.sleep(0.05)
                    spinner_placeholder.write('<div class="spinner"></div>', unsafe_allow_html=True)
                
                #finding closest locations
                closest_locations_df = calculate_closest_locations(df_filtered, latitude, longitude, num_locations)

                #remove spinner
                spinner_placeholder.empty()
                spinner_message_placeholder.empty()
                # Display closest locations DataFrame
                st.write(f"Closest {num_locations} Locations are:")
                st.dataframe(closest_locations_df)
                
                # Start spinning wheel animation
                spinner_message_placeholder = st.empty()
                spinner_placeholder = st.empty()
                spinner_message_placeholder.write(f"Creating map...")
                for _ in range(total_steps):
                    time.sleep(0.05)
                    spinner_placeholder.write('<div class="spinner"></div>', unsafe_allow_html=True)
            
                #calling map-function                
                building_map = create_building_map(latitude, longitude, df_filtered, df, num_locations)

                #remove spinner
                spinner_placeholder.empty()
                spinner_message_placeholder.empty()
                
                #showing map
                st.components.v1.html(building_map, height=600)

        except ValueError as e:
            st.error("ValueError: " + str(e))
        except Exception as e:
            st.error("An error occurred: " + str(e))


    if __name__ == "__main__":
        main()


          
##########################################################
# about
##########################################################

if page == "about":
    # description
    st.write("""
    As being a photographer who mainly is interested in taking photos of brutalistic architecture that I am,
    it sometimes was extremely difficult to find suiting buildings when visiting new cities. \n
    That's why I came up with the idea of creating a webapp, that finds architecture suggestions based on your interests.\n
    In hope to make the search for more interesting buildings to take photos of easier. \n
    Yet, finding a suiting database is challenging, that's why some features don't work perfectly.
    """)
    # blank space
    st.write("")
    # image
    st.image('_B219365.jpg')
    
    instagram_username = "md.multiverse"
    #st.write("") 
    st.markdown(f"""
                Catch up with my latest photos & reels on [Instagram](https://www.instagram.com/{instagram_username}/). \n
                And get inspired by architecture in a brutalistic style.
                """)

  
            
            
##########################################################
# appendix
##########################################################

if page == "appendix":
    # title
    st.title("appendix")
    st.write("This webapp is the final project as part of the Data Science Bootcamp at SPICED Academy.")
    # blank space
    st.write("")
    # image
    st.image('spiced_logo.png')
   

