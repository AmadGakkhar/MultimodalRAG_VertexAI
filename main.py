import PIL.Image
import os
import csv
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json

load_dotenv()


class Prescription(BaseModel):
    hospital_name: str
    doctor_name: str
    patient_name: str
    gender: str
    age: str
    diagnosis: str
    medication: str


def get_model():

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel("gemini-1.5-flash")
    return model


def get_prescription(model, images, image_names):
    json_data = []
    prompt = """
    
    The image is a doctor's prescription. 
    Please extract the following information.
    
    Hospital/Clinic Name, Doctor Name, Patient Name, Gender, Age, Diagnosis, Medication
    if any information is not present return null.
    
    """

    for image_name, image in zip(image_names, images):
        response = model.generate_content(
            [prompt, image],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=Prescription
            ),
        )
        # print(response.text)
        json_item = Prescription.model_validate(json.loads(response.text)).model_dump()
        json_data.append(json_item)
    print(json_data)
    print(type(json_data[0]))
    json_to_csv(json_data=json_data, csv_filename=file_path_prescription)


def get_engine_numbers(model, images, image_names):
    engineNumbers = []
    imageNames = []
    prompt = """
        
        The image is a close up of an engine. Please extract the engine number from it. 
        Your output should only be the extracted engine number and nothing else.        
        """
    for image_name, image in zip(image_names, images):
        response = model.generate_content([prompt, image])
        engineNumbers.append(response.text.strip())
        imageNames.append(image_name)
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


def json_to_csv(json_data, csv_filename):
    """Writes JSON data to a CSV file.

    Args:
      json_data: A list of JSON objects.
      csv_filename: The name of the CSV file to create.
    """

    # Get the field names from the first JSON object
    fieldnames = json_data[0].keys()

    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in json_data:
            writer.writerow(data)


folder_path_engine = "/home/amadgakkhar/code/MultimodalRAG_VertexAI/engine"
folder_path_prescription = "/home/amadgakkhar/code/MultimodalRAG_VertexAI/prescription"
file_path_engine = "/home/amadgakkhar/code/MultimodalRAG_VertexAI/engine_numbers.csv"
file_path_prescription = (
    "/home/amadgakkhar/code/MultimodalRAG_VertexAI/prescriptions.csv"
)


image_names, images = get_images(folder_path=folder_path_prescription)
get_prescription(model=get_model(), image_names=image_names, images=images)
