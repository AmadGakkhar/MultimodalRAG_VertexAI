import PIL.Image
import os
import csv
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


def get_engine_numbers(images, image_names):
    engineNumbers = []
    imageNames = []
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = """
        
        The image is a close up of an engine. Please extract the engine number from it. 
        Your output should only be the extracted engine number and nothing else.        
        """
    for image_name, image in zip(image_names, images):
        response = model.generate_content([prompt, image])
        engineNumbers.append(response.text.strip())
        imageNames.append(image_name)
        # print(engineNumbers)
    write_csv(image_names=imageNames, extracted_text=engineNumbers, filename=file_path)


def get_images(folder_path):

    images = []
    image_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")):
            image_path = os.path.join(folder_path, filename)
            image = PIL.Image.open(image_path)
            images.append(image)
            image_names.append(filename)
    return image_names, images


def write_csv(image_names, extracted_text, filename):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["image_Name", "engine_Number"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for image_name, text in zip(image_names, extracted_text):
            writer.writerow({"image_Name": image_name, "engine_Number": text})


folder_path = "/home/amadgakkhar/code/MultimodalRAG_VertexAI/Images"
file_path = "/home/amadgakkhar/code/MultimodalRAG_VertexAI/image_text_extraction.csv"

image_names, images = get_images(folder_path=folder_path)
get_engine_numbers(image_names=image_names, images=images)
