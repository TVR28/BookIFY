import streamlit as st
import pickle
import json
import requests
from pathlib import Path
import streamlit_authenticator  as stauth
from streamlit_lottie import st_lottie



def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_gjmecwii.json")

names = ["Raviteja","Anvitha","Guest"]
usernames = ["tvr","anvi","guest"]
passwords = ["tvr28","anvi04","abcd123"]
col = st.columns([2,1])
with col[0]:
    hashed_passwords = stauth.Hasher(passwords).generate()
    # Converting plain text passwords into hashed passwords
    #Streamlit uses bcrypt for password hashing which is a very secure algo
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("wb") as file:
        pickle.dump(hashed_passwords,file)


    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,"Book Recommendor System","abcdef")
    name, authentication_status, username = authenticator.login("Login ","main")
    if authentication_status is None or False:
        st.info("Use username:'guest' and password:'abcd123' to login as a Guest")
    if authentication_status == False:
        st.error("Incorrect username / password")
    if authentication_status is None:
        st.warning("Please enter your username and password")
with col[1]:
    if authentication_status == (False or None):
        st_lottie(
        lottie_hello,
        speed=1.25,
        reverse=False,
        loop=True,
        quality="high", # medium ; high, # canvas
        height=500,
        width=400,
        key=None,)

if authentication_status:
    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}!")
    lottie_hello = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_1a8dx7zj.json")
    with col[0]:
        st.title("About")
        st.header("This Is A Book Recommender Web Application 📖 ")
        st.markdown("#### _The books are recommended to a user using a recommendor system which recommend books by item based collaberative filtering by machine learning_ ")
        st.markdown("### Guest")
        st.markdown("""
        - ##### _Guest can view top 20 trending books and get recommendations of books of their interest_
        ### User
        - ##### _Users can view top 20 trending books and get recommendations of books of their interest_
        - ##### _Can bookmark and save their interested books, get information and sources to download their books_
        - ##### _Get access to info like people who read similar books, user reviews about those books , AI generated summary of the book, Highlights of the books and many more.._
        ## Happy Reading 😊   !!
        """)
    with col[1]:
        st_lottie(
        lottie_hello,
        speed=0.75,
        reverse=False,
        loop=True,
        quality="high", # medium ; high, # canvas
        height=500,
        width=400,
        key=None,)


