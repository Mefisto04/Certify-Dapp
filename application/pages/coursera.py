

import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate_coursera
from utils.streamlit_utils import view_certificate
from connection import contract, w3
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

hide_sidebar()


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


options = ("Generate Coursera Certificate", "View Coursera Certificates")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    form = st.form("Generate-Certificate")
    uid = form.text_input(label="UID")
    candidate_name = form.text_input(label="Student Name")
    course_name = form.text_input(label="Course Name")
    org_name = form.text_input(label="Course ID")

    submit = form.form_submit_button("Submit")
    if submit:
        pdf_file_path = "coursera.pdf"
        institute_logo_path = "../assets/logo.jpg"
        generate_certificate_coursera(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)

        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)
        data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()

        # Smart Contract Call
        contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash).transact({'from': w3.eth.accounts[0]})

        # Update the certificates JSON
        update_certificate_json(candidate_name, "Coursera_Certificate_Id", certificate_id)

        st.success(f"Coursera Certificate successfully generated with Certificate ID: {certificate_id}")

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
