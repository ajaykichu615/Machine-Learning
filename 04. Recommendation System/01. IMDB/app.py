import streamlit as st
import pickle
import pandas as pd
from movie_recommender_module import recommend_movie,get_high_quality_image
with open("movie_reco.pkl",'rb') as obj1:
    data=pickle.load(obj1)
movie_dict=data['movie_dictionary']
st.title("Movie Recommendation App")
movie=st.selectbox("Select a movie",movie_dict.keys())

button=st.button("Recommendations")
df=data['df']
a,b=st.columns([1,1])
if button and movie:
    movie_list=recommend_movie(movie,movie_dict,n=6)
    for i in movie_list[:3]:
        with a:
            poster_link=df.loc[df['Series_Title']==i,"Poster_Link"].iloc[0]
            link=get_high_quality_image(poster_link,width=150,height=150)
            st.image(link)
            year=df.loc[df['Series_Title']==i,"Released_Year"].iloc[0]
            genre=df.loc[df['Series_Title']==i,"Genre"].iloc[0]
            director=df.loc[df['Series_Title']==i,"Director"].iloc[0]
            st.subheader(i)
            st.write(f"Year : {year}")
            st.write(f"Genre : {genre}")
            st.write(f"Director: {director}")
    for i in movie_list[3:]:
        with b:
            poster_link=df.loc[df['Series_Title']==i,"Poster_Link"].iloc[0]
            link=get_high_quality_image(poster_link,width=150,height=150)
            st.image(link)
            year=df.loc[df['Series_Title']==i,"Released_Year"].iloc[0]
            genre=df.loc[df['Series_Title']==i,"Genre"].iloc[0]
            director=df.loc[df['Series_Title']==i,"Director"].iloc[0]
            st.subheader(i)
            st.write(f"Year : {year}")
            st.write(f"Genre : {genre}")
            st.write(f"Director: {director}")