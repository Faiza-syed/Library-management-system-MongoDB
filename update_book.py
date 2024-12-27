import streamlit as st

def render(db, collection):
    st.subheader("✏️ Update a Book")
    update_id = st.text_input("🔍 Enter Book ID to Update")
    if update_id:
        book = collection.find_one({"id": update_id})
        if book:
            with st.form("update_book_form"):
                new_title = st.text_input("📖 Title", value=book['title'])
                new_author = st.text_input("✍️ Author", value=book['author'])
                new_genre = st.text_input("📚 Genre", value=book['genre'])
                new_year = st.number_input("📅 Published Year", value=book['published_year'])
                new_available = st.checkbox("Available", value=book['available'])

                submit_update = st.form_submit_button("Update Book")
                if submit_update:
                    updated_data = {
                        "title": new_title,
                        "author": new_author,
                        "genre": new_genre,
                        "published_year": new_year,
                        "available": new_available,
                    }
                    collection.update_one({'id': update_id}, {'$set': updated_data})
                    st.success(f"✅ Book '{new_title}' updated successfully!")
        else:
            st.warning("⚠️ Book ID not found!")
