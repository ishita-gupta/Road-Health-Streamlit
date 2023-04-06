import streamlit as st
from multiapp import MultiApp
from apps import login,streamlit_app_gallary # import your app modules here

app = MultiApp()

st.markdown("""
# Road Health Safety
""")

# Add all your application here
app.add_app("Home", login.app)
app.add_app("Test", streamlit_app_gallary.app)
# app.add_app("Model", model.app)
# The main app
app.run()