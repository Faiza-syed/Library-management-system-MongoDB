import os
import streamlit as st

def render(db, collection):
    st.subheader("📖 Books in the Library")
    books = list(collection.find({}, {"_id": 0}))
    
    if books:
        for book in books:
            with st.container():
                col1, col2 = st.columns([3, 1])  # Create two columns (3:1 ratio)

                # Left Column: Book Details
                with col1:
                    st.markdown(f"**📖 Title:** {book['title']}")
                    st.markdown(f"**✍️ Author:** {book['author']}")
                    st.markdown(f"**📚 Genre:** {book['genre']}")
                    st.markdown(f"**📅 Published Year:** {book['published_year']}")
                    st.markdown(f"**Available:** {'Yes' if book['available'] else 'No'}")

                    # Display Download Button for PDF
                    if book.get("pdf_file") and os.path.exists(book["pdf_file"]):
                        with open(book["pdf_file"], "rb") as pdf_file:
                            st.download_button(
                                label="📥 Download PDF",
                                data=pdf_file,
                                file_name=os.path.basename(book["pdf_file"]),
                                mime="application/pdf"
                            )
                    else:
                        st.info("📄 No PDF available for this book.")

                # Right Column: Cover Image
                with col2:
                    if book.get("cover_image") and os.path.exists(book["cover_image"]):
                        st.image(book["cover_image"], caption="Book Cover", use_container_width=True)
                    else:
                        st.info("🖼️ No cover image available.")

                st.write("---")  # Separator between books
    else:
        st.info("📚 No books found in the library.")
