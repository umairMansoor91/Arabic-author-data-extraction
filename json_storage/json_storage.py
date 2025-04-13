import os
import json
from datetime import datetime

class AuthorJsonStorage:
    """Class to handle JSON file storage for author data"""
    
    def __init__(self, storage_dir="authors_data"):
        """
        Initialize the JSON storage system
        
        Args:
            storage_dir (str): Directory to store JSON files
        """
        self.storage_dir = storage_dir
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Create the necessary directory structure if it doesn't exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
        # Create an index file if it doesn't exist
        index_path = os.path.join(self.storage_dir, "index.json")
        if not os.path.exists(index_path):
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump({"authors": {}, "last_updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    
    def save_author(self, author_name, json_data):
        """
        Save author data to JSON file
        
        Args:
            author_name (str): The name identifier of the author
            json_data (str): JSON string containing author data
            
        Returns:
            str: The file path where the author data is saved
        """
        try:
            # Parse the JSON data
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            
            # Create a filename-safe version of the author name
            safe_name = "".join([c if c.isalnum() or c in ['-', '_'] else '_' for c in author_name])
            file_name = f"{safe_name}.json"
            file_path = os.path.join(self.storage_dir, file_name)
            
            # Extract basic author info for the index
            author_data = data.get("author", {})
            basic_info = {
                "full_name": author_data.get("full_name"),
                "birth_year": author_data.get("birth_year"),
                "death_year": author_data.get("death_year"),
                "era": author_data.get("era"),
                "file_path": file_path,
                "extraction_date": datetime.now().isoformat()
            }
            
            # Save the full author data to individual file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Update the index
            index_path = os.path.join(self.storage_dir, "index.json")
            index_data = {}
            
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    try:
                        index_data = json.load(f)
                    except json.JSONDecodeError:
                        index_data = {"authors": {}}
            else:
                index_data = {"authors": {}}
            
            # Add or update this author in the index
            index_data["authors"][author_name] = basic_info
            index_data["last_updated"] = datetime.now().isoformat()
            
            # Save the updated index
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            
            return file_path
            
        except Exception as e:
            print(f"Error saving author to JSON file: {str(e)}")
            return None
    
    def get_author(self, author_name):
        """
        Retrieve author data from JSON file
        
        Args:
            author_name (str): The name identifier of the author
            
        Returns:
            dict: Author data
        """
        index_path = os.path.join(self.storage_dir, "index.json")
        
        if not os.path.exists(index_path):
            return None
        
        try:
            # Get author's file path from index
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            authors = index_data.get("authors", {})
            if author_name not in authors:
                return None
            
            author_file_path = authors[author_name].get("file_path")
            
            if not author_file_path or not os.path.exists(author_file_path):
                # Try to find by safe name
                safe_name = "".join([c if c.isalnum() or c in ['-', '_'] else '_' for c in author_name])
                alt_path = os.path.join(self.storage_dir, f"{safe_name}.json")
                if os.path.exists(alt_path):
                    author_file_path = alt_path
                else:
                    return None
            
            # Read the author data
            with open(author_file_path, 'r', encoding='utf-8') as f:
                author_data = json.load(f)
            
            return author_data
            
        except Exception as e:
            print(f"Error retrieving author data: {str(e)}")
            return None
    
    def search_authors(self, search_term):
        """
        Search for authors by name
        
        Args:
            search_term (str): Term to search for in author names
            
        Returns:
            list: Matching author records
        """
        index_path = os.path.join(self.storage_dir, "index.json")
        
        if not os.path.exists(index_path):
            return []
        
        try:
            # Load the index
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            authors = index_data.get("authors", {})
            results = []
            
            # Search in author names and full names
            for author_name, author_info in authors.items():
                if (search_term.lower() in author_name.lower() or 
                    (author_info.get("full_name") and search_term.lower() in author_info.get("full_name").lower())):
                    # Include the author_name in the result
                    result = {**author_info, "author_name": author_name}
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error searching authors: {str(e)}")
            return []
    
    def export_all_data(self, output_file="all_authors_export.json"):
        """
        Export all author data to a single JSON file
        
        Args:
            output_file (str): Path to save the exported JSON
            
        Returns:
            str: Path to the exported file
        """
        index_path = os.path.join(self.storage_dir, "index.json")
        
        if not os.path.exists(index_path):
            return None
        
        try:
            # Load the index
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            authors = index_data.get("authors", {})
            all_data = {}
            
            # Collect data for all authors
            for author_name in authors:
                author_data = self.get_author(author_name)
                if author_data:
                    all_data[author_name] = author_data
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            
            return output_file
            
        except Exception as e:
            print(f"Error exporting authors: {str(e)}")
            return None
    
    def get_all_authors(self):
        """
        Get list of all authors in the storage
        
        Returns:
            list: List of all author basic info
        """
        index_path = os.path.join(self.storage_dir, "index.json")
        
        if not os.path.exists(index_path):
            return []
        
        try:
            # Load the index
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            authors = index_data.get("authors", {})
            results = []
            
            # Format results
            for author_name, author_info in authors.items():
                result = {**author_info, "author_name": author_name}
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error getting all authors: {str(e)}")
            return []