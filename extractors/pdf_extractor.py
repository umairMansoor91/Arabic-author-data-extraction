import os
import re
import tempfile
import PyPDF2

def extract_authors_from_pdf(pdf_file):
    """
    Extract author paragraphs from an Arabic PDF file.
    Each author section starts with a number followed by a dash and the author name.
    Excludes cases where there are page numbers or other numeric references.
    
    Args:
        pdf_file: The uploaded PDF file object
        
    Returns:
        dict: Dictionary mapping author identifiers to their content
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(pdf_file.read())
        temp_path = temp_file.name
    
    try:
        # Open the PDF file
        with open(temp_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Define the pattern for author sections
            author_pattern = re.compile(r'(\d+)\s*-\s*(?![0-9\.\]\)\s])([^\n]+)')
            
            # Find all matches
            matches = list(author_pattern.finditer(text))
            
            # Filter out matches that look like page ranges
            filtered_matches = []
            for match in matches:
                after_dash = match.group(2).strip()
                # Check if the text after the dash doesn't start with a number or looks like a reference
                if not re.match(r'^\d', after_dash) and not re.match(r'^[0-9\.\]\)]+$', after_dash):
                    filtered_matches.append(match)
            
            authors = {}
            # Process each author section
            for i in range(len(filtered_matches)):
                current_match = filtered_matches[i]
                author_num = current_match.group(1)
                author_name = current_match.group(2).strip()
                
                # Get the start position of this author section
                start_pos = current_match.end()
                
                # Get the end position (start of next author or end of text)
                if i < len(filtered_matches) - 1:
                    end_pos = filtered_matches[i+1].start()
                else:
                    end_pos = len(text)
                
                # Extract the content
                content = text[start_pos:end_pos].strip()
                
                # Store the author information
                authors[f"{author_num} - {author_name}"] = content
            
            return authors
            
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return {}

# Alternative implementation using PyMuPDF (fitz)
def extract_authors_with_fitz(pdf_file):
    """
    Alternative implementation using PyMuPDF (fitz) which often handles Arabic text better.
    
    Args:
        pdf_file: The uploaded PDF file object
        
    Returns:
        dict: Dictionary mapping author identifiers to their content
    """
    import fitz  # PyMuPDF
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(pdf_file.read())
        temp_path = temp_file.name
    
    try:
        # Open PDF with PyMuPDF
        doc = fitz.open(temp_path)
        
        # Extract text from all pages
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        
        # Continue with the same pattern matching as before
        author_pattern = re.compile(r'(\d+)\s*-\s*(?![0-9\.\]\)\s])([^\n]+)')
        matches = list(author_pattern.finditer(text))
        
        # Filter out matches that look like page ranges
        filtered_matches = []
        for match in matches:
            after_dash = match.group(2).strip()
            if not re.match(r'^\d', after_dash) and not re.match(r'^[0-9\.\]\)]+$', after_dash):
                filtered_matches.append(match)
        
        authors = {}
        # Process each author section
        for i in range(len(filtered_matches)):
            current_match = filtered_matches[i]
            author_num = current_match.group(1)
            author_name = current_match.group(2).strip()
            
            # Get the start position of this author section
            start_pos = current_match.end()
            
            # Get the end position (start of next author or end of text)
            if i < len(filtered_matches) - 1:
                end_pos = filtered_matches[i+1].start()
            else:
                end_pos = len(text)
            
            # Extract the content
            content = text[start_pos:end_pos].strip()
            
            # Store the author information
            authors[f"{author_num} - {author_name}"] = content
        
        return authors
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return {}