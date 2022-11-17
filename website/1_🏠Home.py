import streamlit as st
import pickle
import requests
from pathlib import Path
import streamlit_authenticator  as stauth
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Book Recommender App",
    page_icon="📕",
    layout="wide"
)
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

    st.title("Top 20 Trending Books 📚   ")


    popular_df = pickle.load(open('popular.pkl','rb'))
    # st.write(popular_df)

    book_name = list(popular_df['Book-Title'].values)
    author = list(popular_df['Book-Author'].values)
    image = list(popular_df['Image-URL-M'].values)
    votes = list(popular_df['num_ratings'].values)
    rating = list(popular_df['avg_rating'].values)

    global x
    x=0


    for i in range(1, 6):
        cols = st.columns(4)
        with cols[0]:
            st.header("")
            string = image[x]
            st.image(string, width=150)
            st.markdown( f'##### {book_name[x]}')
            st.markdown( f'###### **By _{author[x]}_**')
            st.markdown( f'##### Votes - **_{votes[x]}_**')
            st.markdown( f'##### Rating - **_{round(rating[x],1)} / 6_**')
            x+=1
        with cols[1]:
            st.header(" ")
            string = image[x]
            st.image(string, width=150)
            st.markdown( f'##### {book_name[x]}')
            st.markdown( f'###### **By  _{author[x]}_**')
            st.markdown( f'##### Votes - **_{votes[x]}_**')
            st.markdown( f'##### Rating - **_{round(rating[x],1)} / 6_**')
            x+=1
        with cols[2]:
            st.header(" ")
            string = image[x]
            st.image(string, width=150)
            st.markdown( f'##### {book_name[x]}')
            st.markdown( f'###### **By  _{author[x]}_**')
            st.markdown( f'##### Votes - **_{votes[x]}_**')
            st.markdown( f'##### Rating - **_{round(rating[x],1)} / 6_**')
            x+=1
        with cols[3]:
            st.header(" ")
            string = image[x]
            st.image(string, width=150)
            st.markdown( f'##### {book_name[x]}')
            st.markdown( f'###### **By  _{author[x]}_**')
            st.markdown( f'##### Votes - **_{votes[x]}_**')
            st.markdown( f'##### Rating - **_{round(rating[x],1)} / 6_**')
            x+=1

