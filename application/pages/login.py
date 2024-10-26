import streamlit as st
from db.firebase_app import login
from dotenv import load_dotenv
import os
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

form = st.form("login")
email = form.text_input("Enter your email")
password = form.text_input("Enter your password", type="password")

if st.session_state.profile != "Institute":
    clicked_register = st.button("New user? Click here to register!")

    if clicked_register:
        switch_page("register")

submit = form.form_submit_button("Login")
if submit:
    if st.session_state.profile == "Institute":
        valid_email = os.getenv("rto_email")
        valid_pass = os.getenv("rto_password")
        if email == valid_email and password == valid_pass:
            switch_page("rto")
        else:
            st.error("Invalid credentials!")
    if st.session_state.profile == "Institute":
        valid_email = os.getenv("nta_email")
        valid_pass = os.getenv("nta_password")
        if email == valid_email and password == valid_pass:
            switch_page("nta")
        else:
            st.error("Invalid credentials!")

    if st.session_state.profile == "Institute":
        valid_email = os.getenv("college_email")
        valid_pass = os.getenv("college_password")
        if email == valid_email and password == valid_pass:
            switch_page("college")
        else:
            st.error("Invalid credentials!")
    
    if st.session_state.profile == "Institute":
        valid_email = os.getenv("coursera_email")
        valid_pass = os.getenv("coursera_password")
        if email == valid_email and password == valid_pass:
            switch_page("coursera")
        else:
            st.error("Invalid credentials!")

    if st.session_state.profile == "Institute":
        valid_email = os.getenv("birth_email")
        valid_pass = os.getenv("birth_password")
        if email == valid_email and password == valid_pass:
            switch_page("birth")
        else:
            st.error("Invalid credentials!")
    
    else:
        st.error("Invalid credentials!")
        

# import streamlit as st
# from db.firebase_app import login
# from dotenv import load_dotenv
# import os
# from streamlit_extras.switch_page_button import switch_page
# from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

# # Page setup
# st.set_page_config(page_title="Login - Certificate Validation System", layout="wide", initial_sidebar_state="collapsed")
# hide_icons()
# hide_sidebar()
# remove_whitespaces()
# load_dotenv()

# # CSS styling for centering and improved UI
# st.markdown("""
#     <style>
#         /* Center main container */
#         .main {
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             height: 100vh;
#         }
#         /* Form container styling */
#         .form-container {
#             background-color: #f8f9fa;
#             padding: 2rem;
#             border-radius: 10px;
#             box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
#             width: 100%;
#             max-width: 400px;
#             text-align: center;
#         }
#         /* Text input styling */
#         .stTextInput > div > div > input {
#             border-radius: 5px;
#             padding: 0.75rem;
#         }
#         /* Login button */
#         .stButton > button {
#             width: 100%;
#             padding: 0.75rem;
#             font-size: 1rem;
#             color: white;
#             background-color: #007bff;
#             border-radius: 5px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Centered form layout
# st.markdown('<div class="form-container">', unsafe_allow_html=True)
# st.title("Login to Certificate Validation System")
# form = st.form("login_form")
# email = form.text_input("Enter your email")
# password = form.text_input("Enter your password", type="password")
# submit = form.form_submit_button("Login")

# # Registration prompt
# if "profile" in st.session_state and st.session_state.profile != "Institute":
#     clicked_register = st.button("New user? Click here to register!")
#     if clicked_register:
#         switch_page("register")

# # Handling login submission
# if submit:
#     # Credentials and routes mapping
#     credentials = {
#         "rto": (os.getenv("rto_email"), os.getenv("rto_password")),
#         "nta": (os.getenv("nta_email"), os.getenv("nta_password")),
#         "college": (os.getenv("college_email"), os.getenv("college_password")),
#         "coursera": (os.getenv("coursera_email"), os.getenv("coursera_password")),
#         "birth": (os.getenv("birth_email"), os.getenv("birth_password"))
#     }

#     # Check credentials based on profile
#     for route, (valid_email, valid_pass) in credentials.items():
#         if email == valid_email and password == valid_pass:
#             switch_page(route)
#             break
#     else:
#         st.error("Invalid credentials!")

# st.markdown('</div>', unsafe_allow_html=True)

