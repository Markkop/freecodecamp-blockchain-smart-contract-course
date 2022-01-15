import os
import requests
from pathlib import Path

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFiletoIPFS"
# Challenge: Loop the folder to upload all images
filepath = "./img/pug.png"
filename = filepath.split("/")[-1:][0]


def main():
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY"),
    }
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())


if __name__ == "__main__":
    main()
