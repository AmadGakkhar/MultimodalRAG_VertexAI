import streamlit as st
import PIL.Image
import os
import csv
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import pandas as pd


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
        fieldnames = ["Image_Name", "Engine_Number"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for image_name, text in zip(image_names, extracted_text):
            writer.writerow({"Image_Name": image_name, "Engine_Number": text})


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

    write_csv(
        image_names=imageNames, extracted_text=engineNumbers, filename=file_path_engine
    )


def main():
    # Folder path input
    st.title("Engine Number Extraction")
    st.header("Enter Folder Path")
    folder_path = st.text_input("Path")

    # Submit button
    submitted = st.button("Submit")

    if submitted:

        image_names, images = get_images(folder_path=folder_path)
        get_engine_numbers(model=get_model(), image_names=image_names, images=images)
        df = pd.read_csv(file_path_engine)

        # Display results as a table
        st.subheader("Extracted Data")
        st.write(df)


if __name__ == "__main__":

    file_path_engine = (
        "/home/amadgakkhar/code/MultimodalRAG_VertexAI/engine_numbers.csv"
    )
    file_path_prescription = (
        "/home/amadgakkhar/code/MultimodalRAG_VertexAI/prescriptions.csv"
    )
    load_dotenv()
    main()
