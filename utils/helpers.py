import json
import re
import os
from datetime import datetime

def validate_json(json_str):
    """
    Validate if a string is valid JSON
    
    Args:
        json_str (str): JSON string to validate
        
    Returns:
        bool: True if valid JSON, False otherwise
    """
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

def clean_author_name(author_name):
    """
    Clean up author name for use in filenames
    
    Args:
        author_name (str): Original author name
        
    Returns:
        str: Cleaned author name safe for filenames
    """
    # Replace any characters that might be problematic in filenames
    cleaned = re.sub(r'[\\/*?:"<>|]', "", author_name)
    # Replace spaces with underscores
    cleaned = cleaned.replace(" ", "_")
    return cleaned

def extract_json_from_text(text):
    """
    Extract JSON from text that might contain markdown or other content
    
    Args:
        text (str): Text that might contain JSON
        
    Returns:
        str: Extracted JSON string or None if not found
    """
    # Try to extract JSON from markdown code blocks
    json_pattern = re.compile(r'```(?:json)?\s*([\s\S]*?)\s*```')
    match = json_pattern.search(text)
    
    if match:
        json_str = match.group(1).strip()
        if validate_json(json_str):
            return json_str
    
    # If no valid JSON in code blocks, try to find JSON directly
    try:
        # Check if the entire text is valid JSON
        json.loads(text)
        return text
    except json.JSONDecodeError:
        # Try to find JSON-like structures with braces
        brace_pattern = re.compile(r'(\{[\s\S]*\})')
        match = brace_pattern.search(text)
        
        if match:
            potential_json = match.group(1)
            if validate_json(potential_json):
                return potential_json
    
    return None

def save_json_to_file(data, filename=None, directory="extracted_data"):
    """
    Save JSON data to a file
    
    Args:
        data (dict or str): Data to save (dict will be converted to JSON)
        filename (str, optional): Filename to use, defaults to timestamped name
        directory (str, optional): Directory to save in, defaults to 'extracted_data'
        
    Returns:
        str: Path to saved file
    """
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"authors_data_{timestamp}.json"
    
    # Construct full path
    file_path = os.path.join(directory, filename)
    
    # Convert data to JSON string if it's a dict
    if isinstance(data, dict):
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        json_data = data
    
    # Write to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_data)
    
    return file_path

def merge_json_files(directory="extracted_data", output_filename="merged_data.json"):
    """
    Merge multiple JSON files in a directory into a single file
    
    Args:
        directory (str): Directory containing JSON files
        output_filename (str): Name for the merged file
        
    Returns:
        str: Path to merged file
    """
    merged_data = {}
    
    # List all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Read and merge each file
    for file in json_files:
        file_path = os.path.join(directory, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Add each author's data to merged data
                for author, content in data.items():
                    merged_data[author] = content
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
    
    # Save merged data
    output_path = os.path.join(directory, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    return output_path