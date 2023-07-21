from PIL import Image
from get_skin import get_skin
from io import BytesIO
import requests

def overlayImage(username, rank):
    # Open the user's skin PNG file using the provided username
    background = Image.open(BytesIO(get_skin(username)))

    # Create a new image with RGBA mode and dimensions (64x64)
    new_img = Image.new("RGBA", (64, 64))

    # Paste the top-left quadrant (head) (32x16) of the user's skin onto the new image
    new_img.paste(background.crop((0, 0, 32, 16)))

    # Paste the bottom-left quadrant (hat) (32x5) of the user's skin onto the new image,
    # starting from coordinates (32, 11) on the new image
    new_img.paste(background.crop((32, 11, 64, 16)), (32, 11, 64, 16))

    # Set the updated skin image as the background for further processing
    background = new_img

    # Based on the rank, retrieve the appropriate overlay image from the given URLs
    if rank == "resident":
        response = requests.get("https://media.discordapp.net/attachments/566768030995054613/1131341745255358554/mailmanresident.png")
    elif rank == "buke":
        response = requests.get("https://media.discordapp.net/attachments/566768030995054613/1131341745792225390/mailmanbuke.png")
    elif rank == "bushi":
        response = requests.get("https://media.discordapp.net/attachments/566768030995054613/1131341746207465532/mailmanbushi.png")
    elif rank == "shogun":
        response = requests.get("https://media.discordapp.net/attachments/566768030995054613/1131341746643664946/mailmanshogun.png")
    elif rank == "yako":
        response = requests.get("https://media.discordapp.net/attachments/566768030995054613/1131341747134406717/mailmanyako.png")

    # Read the overlay image from the response content
    image_stream = BytesIO(response.content)
    overlay = Image.open(image_stream)

    # Create a new image with transparency (RGBA mode) to combine the background and overlay
    result = Image.new("RGBA", overlay.size)

    # Paste the background image onto the new image
    result.paste(background, (0, 0))

    # Paste the overlay image onto the new image with transparency using the overlay as a mask
    result.paste(overlay, (0, 0), mask=overlay)

    # Save the resulting image to a BytesIO stream in PNG format
    image_stream = BytesIO()
    result.save(image_stream, format="PNG")
    image_stream.seek(0)

    # Return the resulting image stream
    return image_stream
