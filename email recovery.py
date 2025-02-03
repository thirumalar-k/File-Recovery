import os
import hashlib
import re

def calculate_hash(file_path, hash_algorithm='sha256', chunk_size=65536):
    """Calculate hash of a file."""
    hash_obj = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def search_email_content(dd_image_path, keyword):
    """Search for email-related content within a DD image and save to a text file."""
    output_file_path = "search_results.txt"

    with open(output_file_path, 'w') as output_file:
        output_file.write(f"Analysis of image: {dd_image_path}\n")
        
        # Calculate hash (e.g., SHA-256)
        hash_value = calculate_hash(dd_image_path, hash_algorithm='sha256')
        output_file.write(f"SHA-256 hash: {hash_value}\n\n")
        
        # Search for the keyword in the image content
        with open(dd_image_path, 'rb') as image_file:
            content = image_file.read().decode(errors='ignore')
            matches = re.findall(keyword, content, re.IGNORECASE)
            
            if matches:
                output_file.write(f"Found {len(matches)} instances of '{keyword}':\n")
                for match in matches:
                    output_file.write(match + "\n")

if __name__ == "__main__":
    dd_image_path = "E:\Image\E02 in DD\Kavin.002"
    keyword_to_search = "the"  # Replace with the keyword you're searching for
    search_email_content(dd_image_path, keyword_to_search)