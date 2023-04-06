import streamlit as st

import subprocess
import webbrowser

def launch_app():
    port = 8502  # Change to the port where your second app is hosted
    subprocess.Popen(['streamlit', 'run', 'streamlit_app_gallary.py', f'--server.port={port}', '--browser.serverAddress=0.0.0.0'])
    url = f'http://localhost:{port}'
    # webbrowser.open_new_tab(url)





# Add content to your login page
st.header("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "abc" and password == "123":
        st.success("Logged in!")
        launch_app()
    else:
        st.error("Incorrect username or password")
