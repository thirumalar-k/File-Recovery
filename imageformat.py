import os
import hashlib

def calculate_hash(data, hash_algorithm='sha256'):
    """Calculate hash of data."""
    hash_obj = hashlib.new(hash_algorithm)
    hash_obj.update(data)
    return hash_obj.hexdigest()

def extract_images(dd_image_path, output_folder):
    """Extract image files from a DD image and save them to a folder."""
    with open(dd_image_path, 'rb') as image_file:
        offset = 0
        image_number = 1
        chunk_size = 1024

        while True:
            image_data = image_file.read(chunk_size)
            if not image_data:
                break

            image_hash = calculate_hash(image_data)
            image_name = f"image_{image_number:03d}.bin"
            image_path = os.path.join(output_folder, image_name)

            with open(image_path, 'wb') as output_image:
                output_image.write(image_data)

            print(f"Saved {image_name} - Hash: {image_hash}")
            
            offset += chunk_size
            image_number += 1

def main():
    dd_image_path = "F:\hy\Kavin.002"  # Update with the path to your DD image
    output_folder = "F:\hx"  # Update with the path to your output folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extract_images(dd_image_path, output_folder)
    print("Image extraction completed. Images saved to the output folder.")

if __name__ == "__main__":
    main()


    