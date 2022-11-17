import streamlit as st
import pickle
import sys
import requests
import pandas as pd
from pathlib import Path
import numpy as np
import streamlit_authenticator  as stauth
from streamlit_lottie import st_lottie


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_gjmecwii.json")

BKL = pickle.load(open('BKN.pkl','rb'))
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books  = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

book_names = list(BKL['Book-Title'].values)
book_name = list(popular_df['Book-Title'].values)
author = list(popular_df['Book-Author'].values)
image = list(popular_df['Image-URL-M'].values)
votes = list(popular_df['num_ratings'].values)
rating = list(popular_df['avg_rating'].values)

book_titles = list(books['Book-Title'].values)

def recommend(book_title):
    index = np.where(pt.index==book_title)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return data
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
        speed=1.15,
        reverse=False,
        loop=True,
        quality="high", # medium ; high, # canvas
        height=500,
        width=400,
        key=None,)


def print_books(book):

    try :
        data = recommend(book)
        st.header("Here are your top 5 book recommendations!")
        st.success("You Entered " + f"**{book}**" )
        cols = st.columns(5)
        with cols[0]:
            st.header("")
            string = data[0][2]
            st.image(string, width=150)
            st.markdown( f'##### {data[0][0]}')
            st.markdown( f'###### **By _{data[0][1]}_**')
        with cols[1]:
            st.header("")
            string = data[1][2]
            st.image(string, width=150)
            st.markdown( f'##### {data[1][0]}')
            st.markdown( f'###### **By _{data[1][1]}_**')
        with cols[2]:
            st.header("")
            string = data[2][2]
            st.image(string, width=150)
            st.markdown( f'##### {data[2][0]}')
            st.markdown( f'###### **By _{data[2][1]}_**')
        with cols[3]:
            st.header("")
            string = data[3][2]
            st.image(string, width=150)
            st.markdown( f'##### {data[3][0]}')
            st.markdown( f'###### **By _{data[3][1]}_**')
        with cols[4]:
            st.header("")
            string = data[4][2]
            st.image(string, width=150)
            st.markdown( f'##### {data[4][0]}')
            st.markdown( f'###### **By _{data[4][1]}_**')
    except:
        st.error("The Book You've Entered Is Not Available... Please Try Again or Try Selecting a Book Below")
        with st.expander("Try some of these..."):
            st.markdown(book_name)


if authentication_status:
    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}!")
    st.title("Get Book Recommendations Here")

    book = st.text_input( 'Enter a Book Title 👇 (Case Sensitive)', placeholder = 'Ex :  Harry Potter and the Prisoner of Azkaban (Book 3)')
    if st.button('Submit',type = "primary"):
        if any(book in word for word in book_names):
            print_books(book)
        else:
            st.error("The Book You've Entered Is Not Available... Please Try Again")
            with st.expander("Some Of The Books Available Are"):
                st.markdown(book_name)


