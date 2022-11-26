import streamlit as st
import pickle
import re
import random
import requests
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from smtplib import SMTP_SSL
from email.message import EmailMessage
from mimetypes import guess_type
import json
import qrcode
import time
import math
import smtplib


#otp generation
def generate_otp():
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    return OTP

if "otp" not in st.session_state:
    st.session_state.otp = generate_otp()
    if "otpf1" not in st.session_state:
        st.session_state.otpf1 = f"{st.session_state.otp}.jpg"
if "otp2" not in st.session_state:
    st.session_state.otp2 = generate_otp()
    if "otpf2" not in st.session_state:
        st.session_state.otpf2 = f"{st.session_state.otp2}.jpg"
if "resend" not in st.session_state:
    st.session_state.resend = 1

#Generating qrcode
def generate_qrcode():
    qrimage = qrcode.make(st.session_state.otp)
    qrimage.save(f"{st.session_state.otp}.jpg")


#Mail auth
file = open("cred.json")
data = json.load(file)

SENDER_EMAIL = data["email"]
MAIL_PASSWORD = data["password"]
RECIEVER_EMAIL = "tvrraviteja@gmail.com"   #give your mail while testing and " df_new[st.session_state.username][0] " ---->  gives the user email
subject = "BookIFY Two-Factor Authentication"
content = """
Hello User,
Scan the attached  QRCode for the otp. Enter the OTP with in 60 sec

This is a system generted mail from BookIFY.. do not reply or respond

Thanks and regards,
BookIFY
"""
# file_name = f"{otp}.jpg"

def send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,file_name):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIEVER_EMAIL
    msg["Subject"] = subject
    msg.set_content(content)
    mime_type, encoding = guess_type(file_name)
    app_type , sub_type = mime_type.split("/")[0], mime_type.split("/")[1]

    with open(file_name,"rb") as file:
        file_data = file.read()
        msg.add_attachment(file_data,maintype=app_type,subtype = sub_type, filename = file_name)
        file.close()
    print(msg)
    with SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL,MAIL_PASSWORD)
        smtp.send_message(msg)
        smtp.close()
    st.session_state.mail = True
    print("Mail Sent!")


#Database
excel_file = "books app database.xlsx"
df = pd.read_excel(excel_file)
df_new = df.set_index('Username').T.to_dict('list')



def add_to_database(username,email,password):
    df = pd.read_excel(excel_file)
    df.loc[-1] = [username,email,password] # list you want to insert
    df.to_excel(excel_file,index=False)
    df = pd.read_excel(excel_file) #reading updated excel sheet
    df_new = df.set_index('Username').T.to_dict('list')

st.set_page_config(
    page_title="Books App",
    page_icon="📕",
    layout="wide"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_gjmecwii.json") # Login


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
#regex to check email format
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_mail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

#func to print books
def print_books(book):

    try :
        data = recommend(book)
        st.success("You Entered " + f"**{book}**" )
        st.header("Here are your top 5 book recommendations!")
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
def change_login_session():
    st.session_state.login = not st.session_state.login
def change_loggedIn_session():
    st.session_state.loggedIn = not st.session_state.loggedIn

# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )

# including a timer
def timer():
    with st.empty():
        for seconds in range(60):       #for 60 secs
            st.write(f"⏳ {60 - seconds} sec left")
            time.sleep(1)
    st.error("Timeout! Login again")
    time.sleep(1)
    st.empty()
    st.session_state.tfa = True
    st.experimental_rerun()

selected = option_menu(
        menu_title = None,  #required
        options = ["Home","Top Books", "Recommend", "Profile","About"], #required
        icons = ['house','star','book','person',"search"],
        menu_icon = "cast",
        default_index=0,
        orientation="horizontal",
        styles={
        "container": {"padding": "0!important"},
        "icon": {"color": "White", "font-size": "20px"},
        "nav-link": {"font-size": "15px", "text-align": "middle", "margin":"0px","--hover-color": "#3d3d3d"},
        "nav-link-selected": {"background-color": "saffron"},
        }
        )

if selected == "Home":
    # add_bg_from_local('bimg-19.jpg')
    #FF4B4B
    lottie_hello = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_arirrjzh.json")
    lottie_hi = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_kq5rGs.json")
    # st.markdown("<h1 style='text-align: center;color: white;'>Bookify</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:90px; color:#FF4B4B'>BookIFY</h1>",unsafe_allow_html=True)
    col = st.columns([2,1])
    cols = st.columns([2,1])
    with cols[0]:
        st.header("")
        st.header("")
        st.header("All In one place for Readers")
        st.subheader("Some text here aswell....")
    with cols[1]:
        st_lottie(
        lottie_hi,
        speed=1.25,
        reverse=False,
        loop=True,
        quality="high", # medium ; high, # canvas
        height=600,
        width=600,
        key=None,)
    with col[0]:
        st_lottie(
        lottie_hello,
        speed=1.25,
        reverse=False,
        loop=True,
        quality="high", # medium ; high, # canvas
        height=600,
        width=600,
        key=None,)
    if 'loggedIn' not in st.session_state:
        st.session_state.loggedIn = False
    if 'login' not in st.session_state:
        st.session_state.login = False
    if 'mail' not in st.session_state:
        st.session_state.mail = False
    if "tfa" not in st.session_state:
        st.session_state.tfa = True
    if st.session_state.loggedIn == False:
        if st.session_state.login == False:
            with col[1]:
                with st.form(key='Sign Up',clear_on_submit=True):
                    st.subheader("New User? Sign Up")
                    email = st.text_input('Enter your email address',placeholder="Ex:- xyz@gmail.com")
                    username = st.text_input('Enter your username')
                    password = st.text_input('Enter your password',type = 'password')

                    bool = (username in df['Username'].unique())
                    bool2 = (email in df['Email'].unique())
                    bool3 = (password in df['Passwords'].unique())

                    if st.form_submit_button("Sign Up",type = 'primary'):
                        if check_mail(email) == False:
                            st.error("Incorrect email format")
                        elif bool2:
                            st.error("You're not a new user. Please Login")
                        elif bool:
                            st.error("This username is already taken")
                        elif bool3:
                            st.error("This Password is already taken")
                        else:
                            add_to_database(username,email,password)
                            st.success("Succesfully Signed Up 👍  ")
                            change_login_session()
                            st.balloons()
                            st.markdown("##### Now you can login with your credentials. Visit the Login Page")
                            st.experimental_rerun()
                st.subheader("Already a User? Login")
                if st.button("Login",type = 'primary'):
                    change_login_session()
                    st.experimental_rerun()
        elif st.session_state.login == True:
            if st.session_state.tfa == True:
                with col[1]:
                    with st.form(key='Login',clear_on_submit=True):
                        st.subheader("Login")
                        # email = st.text_input('Enter your email address',placeholder="Ex:- xyz@gmail.com")
                        username = st.text_input('Enter your username')
                        password = st.text_input('Enter your password',type = 'password')

                        if st.form_submit_button("Login",type = 'primary'):
                            if not(username in df_new.keys()):
                                st.error("Incorrect Username")
                            elif not (df_new[username][1] == password):
                                st.error("Incorrect Password")
                            else:
                                generate_qrcode()
                                send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf1)
                                with st.spinner('Wait for it...'):
                                        time.sleep(2)
                                st.success('Mail Sent!')
                                if st.session_state.mail == True:
                                    if 'username' not in st.session_state:
                                        st.session_state.username = username
                                    st.session_state.tfa = False
                                    st. experimental_rerun()
                                else:
                                    st.error("email not sent succesfully")
                    st.subheader("New User? Sign Up")
                    if st.button("Sign Up",type = 'primary'):
                        change_login_session()
                        st.experimental_rerun()
            elif st.session_state.tfa == False:
                with col[1]:
                    st.title("Two Factor Authentication")
                    st.subheader("OTP has been sent to your registered mail")
                    uotp = st.text_input("Enter your otp")
                    button1 = st.button("Ok",type = "primary")
                    button2 = st.button("Resend",type = "primary")
                    if button1:
                        if int(uotp) == int(st.session_state.otp):
                            st.success("Login Succesful!")
                            st.session_state.loggedIn = True
                            time.sleep(0.5)
                            st.experimental_rerun()
                        else:
                            st.error("Incorrect otp. Try resending it")
                    if button2:
                        if st.session_state.resend == 1:
                            st.session_state.otp = st.session_state.otp2
                            st.session_state.resend = 0
                            generate_qrcode()
                            send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf2)
                            st.success("OTP resent")
                            time.sleep(0.5)
                            st.experimental_rerun()
                        else:
                            st.error("OTP limit exceeded... Please login again")
                            st.session_state.tfa = True
                            time.sleep(1)
                            st.experimental_rerun()
                    timer()
    elif st.session_state.loggedIn == True:
        with col[1]:
            st.header("Succesfully LoggedIn! Have A Great Time")
            st.subheader("Login And Dive Into The World Of 📖 ")
            st.subheader("Some text here.....")

if selected == "Top Books":
    if 'loggedIn' not in st.session_state:
        st.session_state.loggedIn = False
    if 'login' not in st.session_state:
        st.session_state.login = False
    if st.session_state.loggedIn == False:
        st.markdown("<h1 style=' font-size:44px;'>Please Login To Your Account</h1>",unsafe_allow_html=True)
        col = st.columns([2,1])
        if st.session_state.tfa == True:
                with col[1]:
                    with st.form(key='Login',clear_on_submit=True):
                        st.subheader("Login")
                        # email = st.text_input('Enter your email address',placeholder="Ex:- xyz@gmail.com")
                        username = st.text_input('Enter your username')
                        password = st.text_input('Enter your password',type = 'password')

                        if st.form_submit_button("Login",type = 'primary'):
                            if not(username in df_new.keys()):
                                st.error("Incorrect Username")
                            elif not (df_new[username][1] == password):
                                st.error("Incorrect Password")
                            else:
                                generate_qrcode()
                                send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf1)
                                with st.spinner('Wait for it...'):
                                        time.sleep(2)
                                st.success('Mail Sent!')
                                if st.session_state.mail == True:
                                    if 'username' not in st.session_state:
                                        st.session_state.username = username
                                    st.session_state.tfa = False
                                    st. experimental_rerun()
                                else:
                                    st.error("email not sent succesfully")
        elif st.session_state.tfa == False:
            with col[1]:
                st.title("Two Factor Authentication")
                st.subheader("OTP has been sent to your registered mail")
                uotp = st.text_input("Enter your otp")
                button1 = st.button("Ok",type = "primary")
                button2 = st.button("Resend",type = "primary")
                if button1:
                    if int(uotp) == int(st.session_state.otp):
                        st.success("Login Succesful!")
                        st.session_state.tfa = True
                        st.session_state.loggedIn = True
                        time.sleep(0.5)
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect otp. Try resending it")
                if button2:
                    if st.session_state.resend == 1:
                        st.session_state.otp = st.session_state.otp2
                        st.session_state.resend = 0
                        generate_qrcode()
                        send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf2)
                        st.success("OTP resent")
                        time.sleep(0.5)
                        st.experimental_rerun()
                    else:
                        st.error("OTP limit exceeded... Please login again")
                        st.session_state.tfa = True
                        time.sleep(1)
                        st.experimental_rerun()
                timer()
    elif st.session_state.loggedIn == True:
        # lottie_rec = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_btps9sdj.json")
        # cols = st.columns([2,1])
        # with cols[0]:
        st.markdown("<h2 style='text-align:center; font-size:50px'> Top 20 Trending Books 📚   </h2>",unsafe_allow_html=True)
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

if selected == "Recommend":
    if 'loggedIn' not in st.session_state:
        st.session_state.loggedIn = False
    if 'login' not in st.session_state:
        st.session_state.login = False
    if st.session_state.loggedIn == False:
        st.markdown("<h1 style=' font-size:44px;'>Please Login To Your Account</h1>",unsafe_allow_html=True)
        col = st.columns([2,1])
        if st.session_state.tfa == True:
                with col[1]:
                    with st.form(key='Login',clear_on_submit=True):
                        st.subheader("Login")
                        # email = st.text_input('Enter your email address',placeholder="Ex:- xyz@gmail.com")
                        username = st.text_input('Enter your username')
                        password = st.text_input('Enter your password',type = 'password')

                        if st.form_submit_button("Login",type = 'primary'):
                            if not(username in df_new.keys()):
                                st.error("Incorrect Username")
                            elif not (df_new[username][1] == password):
                                st.error("Incorrect Password")
                            else:
                                generate_qrcode()
                                send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf1)
                                with st.spinner('Wait for it...'):
                                        time.sleep(2)
                                st.success('Mail Sent!')
                                if st.session_state.mail == True:
                                    if 'username' not in st.session_state:
                                        st.session_state.username = username
                                    st.session_state.tfa = False
                                    st. experimental_rerun()
                                else:
                                    st.error("email not sent succesfully")
        elif st.session_state.tfa == False:
            with col[1]:
                st.title("Two Factor Authentication")
                st.subheader("OTP has been sent to your registered mail")
                uotp = st.text_input("Enter your otp")
                button1 = st.button("Ok",type = "primary")
                button2 = st.button("Resend",type = "primary")
                if button1:
                    if int(uotp) == int(st.session_state.otp):
                        st.success("Login Succesful!")
                        st.session_state.tfa = True
                        st.session_state.loggedIn = True
                        time.sleep(0.5)
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect otp. Try resending it")
                if button2:
                    if st.session_state.resend == 1:
                        st.session_state.otp = st.session_state.otp2
                        st.session_state.resend = 0
                        generate_qrcode()
                        send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf2)
                        st.success("OTP resent")
                        time.sleep(0.5)
                        st.experimental_rerun()
                    else:
                        st.error("OTP limit exceeded... Please login again")
                        st.session_state.tfa = True
                        time.sleep(1)
                        st.experimental_rerun()
                timer()
    elif st.session_state.loggedIn == True:
            st.markdown("<h1 style='text-align:center;font-size:45px;color:#FF4B4B'>Get Book Recommendation Here</h1>",unsafe_allow_html=True)

            book = st.text_input( 'Enter a Book Title 👇 (Case Sensitive)', placeholder = 'Ex :  Harry Potter and the Prisoner of Azkaban (Book 3)')
            if st.button('Submit',type = "primary"):
                if any(book in word for word in book_names):
                    print_books(book)
                else:
                    st.error("The Book You've Entered Is Not Available... Please Try Again")
                    with st.expander("Some Of The Books Available Are"):
                        st.markdown(book_name)


if selected == "Profile":
    if 'loggedIn' not in st.session_state:
        st.session_state.loggedIn = False
    if 'login' not in st.session_state:
        st.session_state.login = False
    if st.session_state.loggedIn == False:
        st.markdown("<h1 style=' font-size:44px;'>Please Login To Your Account</h1>",unsafe_allow_html=True)
        col = st.columns([2,1])
        if st.session_state.tfa == True:
                with col[1]:
                    with st.form(key='Login',clear_on_submit=True):
                        st.subheader("Login")
                        # email = st.text_input('Enter your email address',placeholder="Ex:- xyz@gmail.com")
                        username = st.text_input('Enter your username')
                        password = st.text_input('Enter your password',type = 'password')

                        if st.form_submit_button("Login",type = 'primary'):
                            if not(username in df_new.keys()):
                                st.error("Incorrect Username")
                            elif not (df_new[username][1] == password):
                                st.error("Incorrect Password")
                            else:
                                generate_qrcode()
                                send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf1)
                                with st.spinner('Wait for it...'):
                                        time.sleep(2)
                                st.success('Mail Sent!')
                                if st.session_state.mail == True:
                                    if 'username' not in st.session_state:
                                        st.session_state.username = username
                                    st.session_state.tfa = False
                                    st. experimental_rerun()
                                else:
                                    st.error("email not sent succesfully")
        elif st.session_state.tfa == False:
            with col[1]:
                st.title("Two Factor Authentication")
                st.subheader("OTP has been sent to your registered mail")
                uotp = st.text_input("Enter your otp")
                button1 = st.button("Ok",type = "primary")
                button2 = st.button("Resend",type = "primary")
                if button1:
                    if int(uotp) == int(st.session_state.otp):
                        st.success("Login Succesful!")
                        st.session_state.tfa = True
                        st.session_state.loggedIn = True
                        time.sleep(0.5)
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect otp. Try resending it")
                if button2:
                    if st.session_state.resend == 1:
                        st.session_state.otp = st.session_state.otp2
                        st.session_state.resend = 0
                        generate_qrcode()
                        send_mail(SENDER_EMAIL,RECIEVER_EMAIL,MAIL_PASSWORD,subject,content,st.session_state.otpf2)
                        st.success("OTP resent")
                        time.sleep(0.5)
                        st.experimental_rerun()
                    else:
                        st.error("OTP limit exceeded... Please login again")
                        st.session_state.tfa = True
                        time.sleep(1)
                        st.experimental_rerun()
                timer()

    elif st.session_state.loggedIn == True:
        st.markdown("<h1 style='text-align:center;font-size:45px;color:#FF4B4B'>My Profile</h1>",unsafe_allow_html=True)
        col = st.columns([2,1])
        with col[0]:
            st.button("Logout",type="primary",on_click = change_loggedIn_session)
            st.markdown(f"# Welcome {st.session_state.username}! 👋")
            st.markdown("<h1 style='font-size:35px;color:#FF4B4B'>Profile Picture</h1>",unsafe_allow_html=True)
            st.subheader("User features to be added...")

#Use local CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

if selected == "About":
    st.markdown("<h1 style='text-align:center; font-size:45px;color:#FF4B4B'>BookIFY Is A One Stop Book Application For All Book Lovers </h1>",unsafe_allow_html=True)
    col = st.columns([2,1])
    lottie_hello = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_1a8dx7zj.json")
    lottie_con = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_u25cckyh.json")
    with col[0]:
        st.markdown("#### _The books are recommended to a user using a recommendor system which recommend books by item based collaberative filtering by machine learning_ ")
        st.markdown("""
        ### User
        - ##### _Users can view top 20 trending books and get recommendations of books of their interest_
        - ##### _Can bookmark and save their interested books, get information and sources to download their books_
        - ##### _Get access to info like people who read similar books, user reviews about those books , AI generated summary of the book, Highlights of the books and many more.._

        ## Happy Reading 😊   !!
        """)
        st.info("Note that the app is still in the developing phase and gets updated soon... stay tuned!")
    with col[1]:
        st_lottie(
        lottie_hello,
        speed=0.75,
        reverse=False,
        loop=True,
        quality="high", # medium ; high, # canvas
        height=500,
        width=450,
        key=None,)
    st.header("")
    st.markdown("<h2 style='text-align:center; font-size:45px; color:#FF4B4B'> Get In Touch With Me! </h2>",unsafe_allow_html=True)
    cols = st.columns([1,2])
    with cols[0]:
        st_lottie(
        lottie_con,
        speed=1.5,
        reverse=False,
        loop=True,
        quality="high", # medium ; high, # canvas
        height=450,
        width=450,
        key=None,)
    with cols[1]:
        st.subheader("Contact Form")
        contact_form = """
        <form action="https://formsubmit.co/rands2211@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder = "Your Name" required>
            <input type="email" name="email" placeholder = "Your Mail" required>
            <textarea name="message" placeholder="Type your message here"></textarea>
            <button type="submit">Send</button>
        </form>
        """

        st.markdown(contact_form, unsafe_allow_html = True)

        local_css("C:/Users/tvrra/Documents/BRS/website/style/style.css")







