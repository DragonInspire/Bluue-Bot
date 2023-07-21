import requests
import os
import base64
import json

class SkinDownloadError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(message)

def get_skin(username):
    # Make a GET request to Mojang's API
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

    if response.status_code == 200:
        # Extract the UUID from the response
        uuid = response.json().get("id")

        if uuid is None:
            raise SkinDownloadError(1001, "Failed to retrieve the UUID for the given username.")
        
        # Make a GET request to retrieve the skin data
        skin_response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")

        if skin_response.status_code == 200:
            # Extract the skin URL from the response
            skin_data = skin_response.json()
            properties = skin_data.get("properties", [])

            skin_url = None
            for prop in properties:
                if prop.get("name") == "textures":
                    value = prop.get("value")
                    decoded_value = base64.b64decode(value).decode('utf-8')
                    decoded_value = json.loads(decoded_value)
                    skin_url = decoded_value["textures"]["SKIN"]["url"]
                    break

            if skin_url:
                # Make a GET request to download the skin image
                image_response = requests.get(skin_url)

                if image_response.status_code == 200:
                    # Return the image content
                    return image_response.content
                else:
                    raise SkinDownloadError(1003, "Failed to download the skin image.")
            else:
                raise SkinDownloadError(1002, "No skin URL found in the skin data.")
        else:
            raise SkinDownloadError(1004, "Failed to retrieve the skin data from Mojang's session server.")
    else:
        raise SkinDownloadError(1000, "Invalid username. The username does not exist in Mojang's database.")

try:
    skin = get_skin("username")
    # Do something with the skin image content here (e.g., save it as a PNG file)
except SkinDownloadError as e:
    # Handle specific error codes with corresponding messages
    print(f"Error Code: {e.code}")
    print(f"Error Message: {e.message}")
