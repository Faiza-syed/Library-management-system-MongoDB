import streamlit as st
from pymongo import MongoClient
import os
from PIL import Image

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client['library_db']
collection = db['library']

# Directories for storing files
UPLOAD_FOLDER_IMAGES = "book_covers"
UPLOAD_FOLDER_PDFS = "book_pdfs"
os.makedirs(UPLOAD_FOLDER_IMAGES, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_PDFS, exist_ok=True)

# Page Config
st.set_page_config(page_title="Library Management System", layout="wide")
st.markdown(
    """
    <style>
    /* General Page Styling */
    body {
        background-color: #f5f5f5;
    }
    .stApp {
        background-image: linear-gradient(to bottom right, #FFFFFF, #DDDDDD);
        color: #333333;
    }
    h1, h2, h3 {
        color: #5A5A5A;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
    }
    .stButton > button:hover {
        background-color: #0056b3;
        color: white;
    }
    .card {
        border: 2px solid #007BFF;
        border-radius: 10px;
        background-color: #E6F2FF;
        padding: 10px;
        margin-bottom: 20px;
    }
    .card-header {
        font-size: 18px;
        font-weight: bold;
        color: #0056b3;
    }
    .card-subtext {
        font-size: 14px;
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True
)

# Helper Functions
def add_book(book):
    collection.insert_one(book)

def update_book(book_id, updated_data):
    collection.update_one({'id': book_id}, {'$set': updated_data})

def delete_book(book_id):
    book = collection.find_one({"id": book_id})
    if book and "cover_image" in book and os.path.exists(book["cover_image"]):
        os.remove(book["cover_image"])
    if book and "pdf_file" in book and os.path.exists(book["pdf_file"]):
        os.remove(book["pdf_file"])
    collection.delete_one({"id": book_id})

def save_file(uploaded_file, folder, book_id):
    file_path = os.path.join(folder, f"{book_id}_{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# UI Components
st.title("📚 **Library Management System**")
st.write("---")

# Add Book Section
st.subheader("➕ **Add a New Book**")
with st.form("add_book_form", clear_on_submit=True):
    book_id = st.text_input("📋 Book ID", key="add_id")
    title = st.text_input("📖 Title", key="add_title")
    author = st.text_input("✍️ Author", key="add_author")
    genre = st.text_input("📚 Genre", key="add_genre")
    published_year = st.number_input("📅 Published Year", min_value=0, key="add_year")
    available = st.checkbox(" Available", key="add_available")
    cover_image = st.file_uploader("🖼️ Upload Book Cover", type=["jpg", "jpeg", "png"], key="add_image")
    pdf_file = st.file_uploader("📄 Upload Book PDF", type=["pdf"], key="add_pdf")

    submit_add = st.form_submit_button("Add Book")
    if submit_add:
        image_path = save_file(cover_image, UPLOAD_FOLDER_IMAGES, book_id) if cover_image else None
        pdf_path = save_file(pdf_file, UPLOAD_FOLDER_PDFS, book_id) if pdf_file else None
        new_book = {
            "id": book_id,
            "title": title,
            "author": author,
            "genre": genre,
            "published_year": published_year,
            "available": available,
            "cover_image": image_path,
            "pdf_file": pdf_path
        }
        add_book(new_book)
        st.success(f"✅ **Book '{title}' added successfully!**")
st.write("---")

# Update Book Section
st.subheader("✏️ **Update a Book**")
update_id = st.text_input("🔍 Enter Book ID to Update", key="update_id")
if update_id:
    book = collection.find_one({"id": update_id})
    if book:
        with st.form("update_book_form"):
            new_title = st.text_input("📖 Title", value=book['title'], key="upd_title")
            new_author = st.text_input("✍️ Author", value=book['author'], key="upd_author")
            new_genre = st.text_input("📚 Genre", value=book['genre'], key="upd_genre")
            new_year = st.number_input("📅 Published Year", value=book['published_year'], key="upd_year")
            new_available = st.checkbox(" Available", value=book['available'], key="upd_available")
            new_cover_image = st.file_uploader("🖼️ Replace Cover Image", type=["jpg", "jpeg", "png"], key="upd_image")
            new_pdf_file = st.file_uploader("📄 Replace PDF File", type=["pdf"], key="upd_pdf")

            submit_update = st.form_submit_button("Update Book")
            if submit_update:
                updated_data = {
                    "title": new_title,
                    "author": new_author,
                    "genre": new_genre,
                    "published_year": new_year,
                    "available": new_available
                }
                if new_cover_image:
                    updated_data["cover_image"] = save_file(new_cover_image, UPLOAD_FOLDER_IMAGES, update_id)
                if new_pdf_file:
                    updated_data["pdf_file"] = save_file(new_pdf_file, UPLOAD_FOLDER_PDFS, update_id)
                update_book(update_id, updated_data)
                st.success(f"✅ **Book '{new_title}' updated successfully!**")
    else:
        st.warning("⚠️ Book ID not found!")
st.write("---")

# Delete Book Section
st.subheader("🗑️ **Delete a Book**")
delete_id = st.text_input("🔍 Enter Book ID to Delete", key="delete_id")
if delete_id:
    book = collection.find_one({"id": delete_id})
    if book:
        st.warning(f"⚠️ Are you sure you want to delete '{book['title']}'?")
        if st.button("🗑️ Delete Book"):
            delete_book(delete_id)
            st.success(f"✅ **Book '{book['title']}' deleted successfully!**")
    else:
        st.warning("⚠️ Book ID not found!")
st.write("---")

# Display Books Section
st.subheader("📖 **Books in the Library**")
books = list(collection.find({}, {"_id": 0}))
if books:
    for book in books:
        with st.container():
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-header">📖 {book['title']} by {book['author']}</div>
                    <div class="card-subtext">Genre: {book['genre']} | Year: {book['published_year']} | Available: {'Yes' if book['available'] else 'No'}</div>
                </div>
                """, unsafe_allow_html=True
            )

            # Display Book Cover Image
            if book.get("cover_image") and os.path.exists(book["cover_image"]):
                st.image(book["cover_image"], caption="Book Cover", width=200)

            # Display Download Button for PDF
            if book.get("pdf_file") and os.path.exists(book["pdf_file"]):
                with open(book["pdf_file"], "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name=os.path.basename(book["pdf_file"]),
                        mime="application/pdf",
                        key=f"download_{book['id']}"
                    )
            else:
                st.info("📄 No PDF available for this book.")
else:
    st.info("📚 No books found in the library.")
