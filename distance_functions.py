import folium
import requests
import pandas as pd


#api_key = 'AIzaSyDR9lXqqtzp_JJCCmgS0m6a65Ot8KoDCQs'

## user input
def get_user_location(user_location, api_key):
    api_key = 'AIzaSyDR9lXqqtzp_JJCCmgS0m6a65Ot8KoDCQs'
    
    while True:
        #user_location = input("Where do you want to start?\nType the name of the street and the town.\nAlso the postcode, if possible, else provide the name of the district: ")

        #make a request to the Geocoding API
        geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={user_location}&key={api_key}'
        response = requests.get(geocoding_url)
        data = response.json()

        #parse the response
        if data['status'] == 'OK':
            # Extract latitude and longitude
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']

            #print the results
            print("Cool, so these are your coordinates.")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            return latitude, longitude
        else:
            print("Invalid address. Please try again.")



data_path=("1200_buildings_ready_new.csv")
df = pd.read_csv(data_path)


#filtering the dataset
def filter_df(df, selected_style_category, selected_type_category):
    if selected_style_category == '---' and selected_type_category == '---':
        #if both categories are ‘---‘, return the whole dataframe
        df_filtered = df
    elif selected_style_category == '---':
        #if only ‘selected_style_category’ is ‘---’, select based on ‘selected_type_category’
        df_filtered = df[df['matched_types'].notnull() & df['matched_types'].str.contains(selected_type_category, case=False)]
    elif selected_type_category == '---':
        #if only ‘selected_type_category’ is ‘---’, select based on ‘selected_style_category’
        df_filtered = df[df['matched_styles'].notnull() & df['matched_styles'].str.contains(selected_style_category, case=False)]
    else:
        #if both categories have values, apply both filters
        df_filtered = df[
            (df['matched_styles'].notnull() & df['matched_styles'].str.contains(selected_style_category, case=False)) &
            (df['matched_types'].notnull() & df['matched_types'].str.contains(selected_type_category, case=False))
        ]
    return df_filtered



#Inserting "Distance from User Address" Column

def calculate_closest_locations(df_filtered, latitude, longitude, num_locations):
    api_key = 'AIzaSyDR9lXqqtzp_JJCCmgS0m6a65Ot8KoDCQs'

    closest_locations = []

    #print("I'm checking the Top 5 closest Buildings to you, based on your input.")
    
    for index, row in df_filtered.iterrows():
        location = row['Name']
        destination = f'{row["Latitude"]},{row["Longitude"]}'
        print(destination)
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={latitude},{longitude}&destinations={destination}&key={api_key}'
        response = requests.get(url)
        data = response.json()

        #parse the response and extract the travel distance
        if data['status'] == 'OK':
            distance_text = data['rows'][0]['elements'][0]['distance']['text']
            #distance_value = data['rows'][0]['elements'][0]['distance']['value']

            closest_locations.append({'Name': location, 'DistanceText': distance_text})

    #create a DataFrame from the closest locations
    closest_locations_df = pd.DataFrame(closest_locations)
    
    #sort the DataFrame by distance in ascending order
    closest_locations_df.sort_values('DistanceText', inplace=True)
    closest_locations_df = closest_locations_df.reset_index(drop=True)
    closest_locations_df.index = closest_locations_df.index + 1

    #keep only the closest locations based on user input number
    closest_locations_df = closest_locations_df.head(num_locations)

    return closest_locations_df


#creating a map

def create_building_map(latitude, longitude, filtered_df, df, num_locations):
    #create a map and mark the locations of the closest buildings
    map_center = (latitude, longitude)
    #building_map = folium.Map(location=map_center, zoom_start=13, tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', attr='Google Maps')
    building_map = folium.Map(location=map_center, zoom_start=13, tiles='https://stamen-tiles.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png', attr='Stamen Toner Lite')
    #add a marker for the user's start location with a different color
    folium.Marker(location=map_center, popup="Start Location", icon=folium.Icon(color='red')).add_to(building_map)

    #calculate the closest locations and obtain the top 5 closest buildings
    closest_locations_df = calculate_closest_locations(filtered_df, latitude, longitude, num_locations)
    closest_buildings = closest_locations_df.head(num_locations)

    for index, row in closest_buildings.iterrows():
        building_name = row['Name']
        building_latitude = df.loc[df['Name'] == building_name, 'Latitude'].iloc[0]
        building_longitude = df.loc[df['Name'] == building_name, 'Longitude'].iloc[0]
        building_location = (building_latitude, building_longitude)
        folium.Marker(building_location, popup=building_name).add_to(building_map)

     #return the map as an HTML string
    return building_map._repr_html_()



##Getting everything done

#get user location
#latitude_user, longitude_user = get_user_location('AIzaSyDR9lXqqtzp_JJCCmgS0m6a65Ot8KoDCQs')

#select categories
#selected_style_category = get_style_category()
#selected_type_category = get_type_category()

#filter the dataframe
#filtered_df = filter_df(df, selected_style_category, selected_type_category)

#calculate closest locations and obtain the resulting DataFrame
#closest_locations_df = calculate_closest_locations(filtered_df, latitude_user, longitude_user)

#print the closest locations DataFrame
#print(closest_locations_df)

#create the building map using the user's location and filtered dataframe
#building_map = create_building_map(latitude_user, longitude_user, filtered_df, df)

#display the map
#display(building_map)




