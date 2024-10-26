import streamlit as st
from PIL import Image
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


st.title("Certificate Validation System")
st.write("")
st.subheader("Select Your Role")

col1, col2 = st.columns(2)
institite_logo = Image.open("../assets/institute_logo.png")
with col1:
    st.image(institite_logo, output_format="jpg", width=230)
    clicked_institute = st.button("Institute")

company_logo = Image.open("../assets/company_logo.jpg")
with col2:
    st.image(company_logo, output_format="jpg", width=230)
    clicked_verifier = st.button("Verifier")

if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')


# import streamlit as st
# from PIL import Image
# from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
# from streamlit_extras.switch_page_button import switch_page
# from streamlit_extras import add_vertical_space

# # Initial Setup
# st.set_page_config(page_title="Certificate Validation System", layout="wide", initial_sidebar_state="collapsed")
# hide_icons()
# hide_sidebar()
# remove_whitespaces()

# # CSS Styling
# st.markdown("""
#     <style>
#         /* Centering main content */
#         .main { 
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             padding: 20px;
#         }
#         /* Title styling */
#         h1 {
#             font-size: 2.5rem;
#             color: #2c3e50;
#             text-align: center;
#         }
#         /* Subheader styling */
#         .subheader {
#             color: #34495e;
#             font-weight: bold;
#             font-size: 1.5rem;
#             margin-top: -10px;
#             text-align: center;
#         }
#         /* Button styling */
#         .stButton > button {
#             border-radius: 10px;
#             font-size: 1.2rem;
#             width: 100%;
#             padding: 0.5em;
#             color: #fff;
#         }
#         /* Institute button */
#         #Institute {
#             background-color: #3498db;
#         }
#         /* Verifier button */
#         #Verifier {
#             background-color: #2ecc71;
#         }
#         /* Adjust columns on smaller screens */
#         [data-testid="column"] {
#             flex: 1 1 50%;
#             padding: 10px;
#         }
#         /* Logo adjustments */
#         img {
#             width: 100%;
#             height: auto;
#             margin-bottom: 10px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Page Content
# st.title("Certificate Validation System")
# st.write("")
# st.markdown('<div class="subheader">Select Your Role</div>', unsafe_allow_html=True)
# add_vertical_space(2)

# # Display Role Selection with Icons and Buttons
# col1, col2 = st.columns(2)

# # Institute Option
# institite_logo = Image.open("../assets/institute_logo.png")
# with col1:
#     st.image(institite_logo, output_format="PNG")
#     clicked_institute = st.button("Institute", key="Institute")

# # Verifier Option
# company_logo = Image.open("../assets/company_logo.jpg")
# with col2:
#     st.image(company_logo, output_format="JPG")
#     clicked_verifier = st.button("Verifier", key="Verifier")

# # Redirect based on selection
# if clicked_institute:
#     st.session_state.profile = "Institute"
#     switch_page('login')
# elif clicked_verifier:
#     st.session_state.profile = "Verifier"
#     switch_page('login')
