import streamlit as st
from pymongo import MongoClient
import add_book
import update_book
import delete_book
import display_books

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client['library_db']
collection = db['library']

# Page Config
st.set_page_config(page_title="Library Management System", layout="wide")
st.sidebar.title("📚 Library Management System")

# Sidebar Navigation
pages = {
    "Add Book": add_book,
    "Update Book": update_book,
    "Delete Book": delete_book,
    "View Books": display_books,
}
page = st.sidebar.radio("Navigate to:", list(pages.keys()))

# Load Selected Page
if page:
    pages[page].render(db, collection)
