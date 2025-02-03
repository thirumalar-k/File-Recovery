import re

def retrieve_browsing_history(dd_image):
    """Retrieve potential browsing history URLs from a raw disk image using regular expressions.
    
    Args:
        dd_image (str): Path to the raw disk image.
        
    Returns:
        list: A list of strings, each representing a potential URL.
    """
    browsing_history = []
    url_pattern = re.compile(r"(http|https)://[^\s/$.?#].[^\s]*")

    with open(dd_image, "rb") as f:
        data = f.read().decode("utf-8", errors="ignore")
        matches = url_pattern.findall(data)
        browsing_history.extend(matches)

    return browsing_history

if __name__ == "__main__":
    raw_disk_image = "D:\KAVACH\Kavin.002"
    extracted_urls = retrieve_browsing_history(raw_disk_image)
    
    for url in extracted_urls:
        print(url)
