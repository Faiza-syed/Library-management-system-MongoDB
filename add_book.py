import os
import streamlit as st

UPLOAD_FOLDER_IMAGES = "book_covers"
UPLOAD_FOLDER_PDFS = "book_pdfs"
os.makedirs(UPLOAD_FOLDER_IMAGES, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_PDFS, exist_ok=True)

def save_file(uploaded_file, folder, book_id):
    file_path = os.path.join(folder, f"{book_id}_{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def render(db, collection):
    st.subheader("➕ Add a New Book")
    with st.form("add_book_form", clear_on_submit=True):
        book_id = st.text_input("📋 Book ID")
        title = st.text_input("📖 Title")
        author = st.text_input("✍️ Author")
        genre = st.text_input("📚 Genre")
        published_year = st.number_input("📅 Published Year", min_value=0)
        available = st.checkbox("Available")
        cover_image = st.file_uploader("🖼️ Upload Book Cover", type=["jpg", "jpeg", "png"])
        pdf_file = st.file_uploader("📄 Upload Book PDF", type=["pdf"])

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
                "pdf_file": pdf_path,
            }
            collection.insert_one(new_book)
            st.success(f"✅ Book '{title}' added successfully!")
