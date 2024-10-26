# import streamlit as st
# import requests
# import json
# import os
# from dotenv import load_dotenv
# import hashlib
# from utils.cert_utils import generate_certificate
# from utils.streamlit_utils import view_certificate
# from connection import contract, w3
# from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

# st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# hide_icons()
# hide_sidebar()
# remove_whitespaces()

# load_dotenv()

# api_key = os.getenv("PINATA_API_KEY")
# api_secret = os.getenv("PINATA_API_SECRET")


# def upload_to_pinata(file_path, api_key, api_secret):
#     # Set up the Pinata API endpoint and headers
#     pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
#     headers = {
#         "pinata_api_key": api_key,
#         "pinata_secret_api_key": api_secret,
#     }

#     # Prepare the file for upload
#     with open(file_path, "rb") as file:
#         files = {"file": (file.name, file)}

#         # Make the request to Pinata
#         response = requests.post(pinata_api_url, headers=headers, files=files)

#         # Parse the response
#         result = json.loads(response.text)

#         if "IpfsHash" in result:
#             ipfs_hash = result["IpfsHash"]
#             print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
#             return ipfs_hash
#         else:
#             print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
#             return None


# options = ("Generate NTA Certificate", "View NTA Certificates")
# selected = st.selectbox("", options, label_visibility="hidden")

# if selected == options[0]:
#     form = st.form("Generate-Certificate")
#     uid = form.text_input(label="UID")
#     candidate_name = form.text_input(label="Student Name")
#     course_name = form.text_input(label="Exam Name")
#     org_name = form.text_input(label="Percentile")

#     submit = form.form_submit_button("Submit")
#     if submit:
#         pdf_file_path = "nta.pdf"
#         institute_logo_path = "../assets/logo.jpg"
#         generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)

#         # Upload the PDF to Pinata
#         ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
#         os.remove(pdf_file_path)
#         data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
#         certificate_id = hashlib.sha256(data_to_hash).hexdigest()

#         # Smart Contract Call
#         contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash).transact({'from': w3.eth.accounts[0]})
#         st.success(f"NTA Certificate successfully generated with Certificate ID: {certificate_id}")

# else:
#     form = st.form("View-Certificate")
#     certificate_id = form.text_input("Enter the Certificate ID")
#     submit = form.form_submit_button("Submit")
#     if submit:
#         try:
#             view_certificate(certificate_id)
#         except Exception as e:
#             st.error("Invalid Certificate ID!")
        


import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import displayPDF, view_certificate
from connection import contract, w3
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")
pinata_gateway_base_url = "https://gateway.pinata.cloud/ipfs"

def upload_to_pinata(file_path, api_key, api_secret):
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)

        # Parse the response
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None


def update_certificate_json(candidate_name, certificate_type, certificate_id):
    # Define the JSON file path
    json_file_path = "certificates.json"

    # Load existing data or initialize it as an empty list
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            try:
                data = json.load(file)
                # Ensure the data is a list of dictionaries
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                # If the file is not a valid JSON, start with an empty list
                data = []
    else:
        data = []

    # Check if the user already exists in the data
    user_found = False
    for user in data:
        if isinstance(user, dict) and user.get("Name") == candidate_name:
            # Update the existing user's certificate information
            user[certificate_type] = ipfs_hash
            user_found = True
            break

    # If the user was not found, add a new user entry
    if not user_found:
        new_user = {
            "Name": candidate_name,
            certificate_type: ipfs_hash
        }
        data.append(new_user)

    # Save updated data back to the file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Updated certificates.json with {certificate_type} for {candidate_name}: {ipfs_hash}")


options = ("Generate NTA Certificate","View Past Certificates", "View NTA Certificates")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    form = st.form("Generate-Certificate")
    uid = form.text_input(label="UID")
    candidate_name = form.text_input(label="Student Name")
    course_name = form.text_input(label="Exam Name")
    org_name = form.text_input(label="Percentile")

    submit = form.form_submit_button("Submit")
    if submit:
        pdf_file_path = "nta.pdf"
        institute_logo_path = "../assets/logo.jpg"
        generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)

        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)
        data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()

        # Update JSON file with the certificate ID and candidate name
        update_certificate_json(candidate_name, "NTA_Certificate_Id", certificate_id)

        # Smart Contract Call
        contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash).transact({'from': w3.eth.accounts[0]})
        st.success(f"NTA Certificate successfully generated with Certificate ID: {certificate_id}")


elif selected == options[1]:
    st.write("Past Certification:")
    aadhar_number = st.text_input("Enter your Aadhar Number:")
    if aadhar_number:
        # Load the certificates from the JSON file
        json_file_path = "certificates.json"
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as file:
                certificates_data = json.load(file)
                
            # Filter the certificates by Aadhar number
            user_certificates = [user for user in certificates_data if user.get("Aadhar") == aadhar_number]
            
            if user_certificates:
                st.write("Your Certificates:")
                for user in user_certificates:
                    candidate_name = user.get("Name")
                    st.write(f"**Name:** {candidate_name}")
                    for certificate_type, certificate_id in user.items():
                        if certificate_type != "Name" and certificate_type != "Aadhar":
                            view_button = st.button(f"View {certificate_type.replace('_', ' ').title()}", key=certificate_id)
                            if view_button:
                                ipfs_hash = certificate_id
                                content_url = f"{pinata_gateway_base_url}/{ipfs_hash}"
                                
                                # Debugging information
                                # st.write(f"Fetching certificate from: {content_url}")
                                
                                response = requests.get(content_url)
                                
                                # st.write(f"Response status code: {response.status_code}")
                                if response.status_code == 200:
                                    st.success("Certificate fetched successfully!")
                                    with open("temp.pdf", 'wb') as pdf_file:
                                        pdf_file.write(response.content)
                                    displayPDF("temp.pdf")
                                    os.remove("temp.pdf")
                                else:
                                    st.error(f"Failed to fetch the certificate from IPFS. Status Code: {response.status_code}, Reason: {response.text}, Content: {response.content}")


            else:
                st.write("No certificates found for the provided Aadhar number.")


else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
