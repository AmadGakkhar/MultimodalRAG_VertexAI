ENGINE_PROMPT = """
Extract Text from this image

Your output should be of the form

"""
PRESCRIPTION_PROMPT = """
    
    The image is a doctor's prescription. 
    Please extract the following information.
    
    Hospital/Clinic Name, Doctor Name, Patient Name, Gender, Age, Diagnosis, Medication
    if any information is not present return null.
    
    Your output should be in JSON format
    Expected Output Format:
    {
    "hospital_name": "",
    "doctor_name": "",  
    "patient_name": "",
    "gender": "",
    "age": "",
    "diagnosis": "",
    "medication": ""
    }     
    """
