import base64
import vertexai
import os
from vertexai.generative_models import GenerativeModel, Part, SafetySetting


def encode_images(folder_path):
    """
    Encode images in a folder and append to a list.

    Args:
        folder_path (str): Path to the folder containing images.

    Returns:
        list: List of base64 encoded image strings.
    """
    encoded_images = []
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")):
            image_path = os.path.join(folder_path, filename)
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                encoded_image = base64.b64encode(image_data).decode("utf-8")
                encoded_images.append(encoded_image)
    return encoded_images


def generate(encoded_images):
    vertexai.init(project="the-bird-427712-q7", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
    )
    for encoded_image in encoded_images:
        image1 = Part.from_data(
            mime_type="image/jpeg",
            data=base64.b64decode(encoded_image),
        )
        responses = model.generate_content(
            [image1, """Extract Text from this image"""],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )

        for response in responses:
            print(response.text, end="")


# image_path = "/home/amadgakkhar/code/MultimodalRAG_VertexAI/Images/1.jpeg"

# with open(image_path, "rb") as image_file:
#     image_data = image_file.read()
#     encoded_image = base64.b64encode(image_data).decode("utf-8")


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
]

folder_path = "/home/amadgakkhar/code/MultimodalRAG_VertexAI/Images"
encoded_images = encode_images(folder_path=folder_path)
generate(encoded_images=encoded_images)
