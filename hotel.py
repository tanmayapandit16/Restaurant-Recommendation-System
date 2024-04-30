import streamlit as st
import pickle
import pandas as pd
import re

st.set_page_config(page_title="Restaurant Recommendation System",
                #    page_icon="🍽",
                   layout="wide")

def normalize_name(name):
    # Remove extra spaces and convert to lowercase
    return re.sub(r'[^\w\s]', '', name).strip().lower()
    

def recommend(hotel):
    hotel = normalize_name(hotel)
    hotel_index = hotels[hotels['rest_name'].apply(normalize_name).str.contains(hotel)].index[0]
    distances = similarity[hotel_index]
    hotels_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]
    
    # recommended_hotels =[]
    # links=[]
    recommendations = []
    for i in hotels_list:
        # recommended_hotels.append(hotels.iloc[i[0]].rest_name)
        # links.append(hotels.iloc[i[0]].link)
        recommended_hotel = hotels.iloc[i[0]].rest_name
        link = hotels.iloc[i[0]].link
        recommendations.append((recommended_hotel, link))
    return recommendations

hotel_dict = pickle.load(open('hotel_dict.pkl','rb'))
hotels = pd.DataFrame(hotel_dict)

similarity = pickle.load(open('hotel_similarity.pkl','rb'))


st.title('Restaurant Recommendation System')
st.write('Enter a Restaurant name situated in Pune and get related recommendations from in and around the area.')

selected_hotel = st.selectbox(
    'Enter a Restaurant name', hotels['rest_name'].values
)

# if st.button('Recommend'):
#     names = recommend(selected_hotel)
    
#     for i in names:
#         st.write(i)

        
if st.button('Recommend'):
    recommendations = recommend(selected_hotel)
    i=0
    for name, link in recommendations:
   
        st.write(f"Number {i+1}:", name)
        st.markdown(f"[{link}]({link})")
        i+=1
