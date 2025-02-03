import subprocess

def create_disk_image(source_disk, output_image):
    try:
        subprocess.run(["sudo", "dd", "if=" + source_disk, "of=" + output_image, "bs=4M"])
        print("Disk image created successfully.")
    except subprocess.CalledProcessError as e:
        print("Error creating disk image:", e)

if __name__ == "__main__":
    source_disk = "D:\e01"  # Replace with the actual disk path
    output_image = "gayu_image.raw"  # Replace with the desired output image file name

    create_disk_image(source_disk, output_image)
