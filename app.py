import streamlit as st
import os
import json
from extractors.pdf_extractor import extract_authors_from_pdf
from processors.gemini_processor import extract_data_from_text
from ui.components import add_rtl_support, create_author_card, show_success_message, show_error_message
from utils.helpers import clean_author_name
# Import the class directly from the json_storage module
from json_storage.json_storage import AuthorJsonStorage

# Initialize JSON storage by creating an instance of the class
storage = AuthorJsonStorage()

def main():
    """Main function for the Streamlit application"""
    st.title("Arabic PDF Author Extractor")
    st.write("Upload an Arabic PDF file to extract paragraphs related to authors.")
    
    # Add RTL support for Arabic text
    add_rtl_support()
    
    # Create tabs for different functionality
    tab1, = st.tabs(["Extract Authors"])
    with tab1:
        process_pdf_upload()
    

def process_pdf_upload():
    """Handle PDF upload and extraction"""
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        st.success("File successfully uploaded!")
        
        # Extract author information
        with st.spinner("Extracting author information..."):
            authors = extract_authors_from_pdf(uploaded_file)
        
        if authors:
            st.success(f"Found {len(authors)} author sections in the document.")
            
            # Dictionary to store all processed JSON data
            all_extracted_data = {}
            
            # Create placeholders for each author's data
            placeholders = {}
            for author in authors.keys():
                with st.expander(f"Author: {author}"):
                    st.text_area(f"Content for {author}", value=authors[author], height=200)
                    # Create a placeholder for this author's JSON
                    placeholders[author] = st.empty()
                    
                    # Add a download button for each author's content
                    content_bytes = authors[author].encode('utf-8')
                    st.download_button(
                        label=f"Download {author}'s content",
                        data=content_bytes,
                        file_name=f"{clean_author_name(author)}.txt",
                        mime="text/plain"
                    )
            
            # Process each author and update their placeholder as results become available
            progress_bar = st.progress(0)
            for i, (author, content) in enumerate(authors.items()):
                # Process this author's content
                json_data = extract_data_from_text(author, content)
                
                # Update this author's placeholder with the result
                if json_data:
                    with st.expander(f"Processed Data: {author}"):
                        st.json(json_data)
                    
                    # Add download button for individual JSON data
                    st.download_button(
                        label=f"Download {author}'s JSON data",
                        data=json_data,
                        file_name=f"{clean_author_name(author)}_data.json",
                        mime="application/json"
                    )
                    
                    # Store in our complete dataset
                    try:
                        parsed_data = json.loads(json_data)
                        all_extracted_data[author] = parsed_data
                        
                        # Save to JSON storage
                        file_path = storage.save_author(author, json_data)
                        if file_path:
                            st.success(f"Saved {author} to JSON file: {os.path.basename(file_path)}")
                    except json.JSONDecodeError:
                        st.error(f"Could not parse JSON data for {author}")
                
                # Update progress
                progress_bar.progress((i + 1) / len(authors))
                
            progress_bar.progress(100)
            st.success("All authors processed successfully!")
            
            # Save all data to a single JSON file
            if all_extracted_data:
                # Convert to JSON string for download button
                all_data_json = json.dumps(all_extracted_data, ensure_ascii=False, indent=2)
                
                # Create a download button for all data
                st.download_button(
                    label="Download All Extracted Data (JSON)",
                    data=all_data_json,
                    file_name="all_authors_data.json",
                    mime="application/json"
                )
                
                # Also save to disk as a consolidated file
                try:
                    output_file = "all_authors_extracted.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(all_extracted_data, f, ensure_ascii=False, indent=2)
                    st.success(f"All data saved to {output_file}")
                except Exception as e:
                    st.error(f"Error saving data to disk: {str(e)}")
                
        else:
            st.warning("No author sections found in the document. Make sure the document contains author sections starting with numbers followed by dashes.")



if __name__ == "__main__":
    main()