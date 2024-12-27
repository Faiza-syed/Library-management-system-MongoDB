import streamlit as st

def render(db, collection):
    st.subheader("🗑️ Delete a Book")
    delete_id = st.text_input("🔍 Enter Book ID to Delete")
    if delete_id:
        book = collection.find_one({"id": delete_id})
        if book:
            st.warning(f"⚠️ Are you sure you want to delete '{book['title']}'?")
            if st.button("🗑️ Delete Book"):
                collection.delete_one({"id": delete_id})
                st.success(f"✅ Book '{book['title']}' deleted successfully!")
        else:
            st.warning("⚠️ Book ID not found!")
