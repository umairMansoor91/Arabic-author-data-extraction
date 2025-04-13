import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.helpers import extract_json_from_text, validate_json

def initialize_gemini():
    """Initialize the Gemini API with the API key from environment variables"""
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        st.error("Please set the GOOGLE_API_KEY in your .env file")
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def extract_data_from_text(author, content):
    """
    Extract structured data from text using Gemini API
    
    Args:
        author (str): The author identifier
        content (str): The content text to analyze
        
    Returns:
        str: JSON data if successful, None otherwise
    """
    model = initialize_gemini()
    if not model:
        return None
        
    try:
        # Format the prompt with the author and content
        prompt = f"""
        This data belongs to author: {author}
        The context of this author is: {content}
        - Return structured JSON data as follows:

        ```json
        {{
        "author": {{
            "full_name": "string",
            "aliases": ["string"] | NIL,
            "students": ["string"] | NIL,
            "teachers": ["string"] | NIL,
            "birth_year": "integer" | NIL,
            "death_year": "integer" | NIL,
            "birthplace": "string" | NIL,
            "primary_locations": ["string"] | NIL,
            "era": "string" | NIL,
            "travel_history": [
            {{
                "travel_id": "string",
                "city": "string",
                "year_visited": "integer" | NIL
            }}
            ] | NIL,
            "did_travel_for_hadith": "boolean" | NIL,
            "memory_changes": "string" | NIL,
            "known_tadlis": "boolean" | NIL,
            "scholarly_reliability": "string" | NIL,
            "scholarly_evaluations": ["string"] | NIL
        }},
        "hadiths": [
            {{
            "hadith_id": "string"
            }}
        ] | NIL,
        "places": [
            {{
            "place_id": "string",
            "name": "string",
            "type": "string"
            }}
        ] | NIL
        }}
        
        - Important: Provide a valid JSON response that can be parsed properly.
        - Replace NIL with null if the data is not available.
        - Make sure your response contains only valid JSON that can be parsed with json.loads().
        """

        # Get response from Gemini
        response = model.generate_content([prompt])
        response_text = response.text
        
        # Process the response to extract valid JSON
        json_str = extract_json_from_text(response_text)
        
        if json_str and validate_json(json_str):
            # Parse and re-serialize to ensure proper formatting
            parsed_json = json.loads(json_str)
            return json.dumps(parsed_json, ensure_ascii=False, indent=2)
        else:
            # If we couldn't extract valid JSON, try again with a clearer prompt
            simplified_prompt = f"""
            Analyze this text about author {author} and return ONLY a valid JSON object following this exact structure.
            Your response should contain nothing but the JSON object itself - no explanations, no markdown:
            
            {{
              "author": {{
                "full_name": "The author's full name",
                "aliases": ["alias1", "alias2"] or null,
                "students": ["student1", "student2"] or null,
                "birth_year": 123 or null,
                "death_year": 456 or null
              }}
            }}
            
            Expand with other fields as appropriate from the text: {content[:500]}...
            """
            
            retry_response = model.generate_content([simplified_prompt])
            retry_text = retry_response.text
            
            # Try to extract JSON again
            json_str = extract_json_from_text(retry_text)
            
            if json_str and validate_json(json_str):
                parsed_json = json.loads(json_str)
                return json.dumps(parsed_json, ensure_ascii=False, indent=2)
            else:
                st.warning(f"Could not extract valid JSON for author {author}")
                return None

    except Exception as e:
        st.error(f"Error extracting data: {str(e)}")
        return None


def batch_process_authors(authors_dict, batch_size=5):
    """
    Process multiple authors in batches to optimize API usage
    
    Args:
        authors_dict (dict): Dictionary of author names to content
        batch_size (int): Number of authors to process in each batch
        
    Returns:
        dict: Dictionary of author names to extracted JSON data
    """
    results = {}
    model = initialize_gemini()
    
    if not model:
        return results
    
    # Process authors in batches
    author_items = list(authors_dict.items())
    for i in range(0, len(author_items), batch_size):
        batch = author_items[i:i+batch_size]
        
        for author, content in batch:
            try:
                json_data = extract_data_from_text(author, content)
                if json_data:
                    results[author] = json_data
            except Exception as e:
                st.error(f"Error processing {author}: {str(e)}")
    
    return results