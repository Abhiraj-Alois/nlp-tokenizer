import os
import json
import pandas as pd
from pdfminer.high_level import extract_text
from groq import Groq
import prompt as prompt

prompt_string = prompt

def extract_pdf_text(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

def process_resume_groq(pdf_path, groq_client):
    resume_text = extract_pdf_text(pdf_path)
    if not resume_text:
        return None
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": prompt_string
            },
            {
                "role": "user",
                "content": resume_text
            },
        ],
        temperature=0.2,
        max_tokens=8192,
        top_p=1,
        stream=False,
        # response_format={"type": "json_object"},
    )
    
    
    response_content = response.choices[0].message.content

    print(response_content)
    exit(0)
    if not response_content.strip():
        print(f"\nNo content received from Groq API for {pdf_path}. Skipping.")
        return None

    try:
        print(type(response_content))
        response_dict = json.loads(response_content)
    except json.JSONDecodeError as e:
        print(f"\nError decoding JSON for {pdf_path}: {e}")
        print(f"\nReceived content: {response_content}")
        return None

    # Output JSON structure
    output = {
        "resume_filename": os.path.basename(pdf_path),
        "resume_text": resume_text,
        "skills": response_dict.get("skills", [])
    }
    
    return output

def save_json(output, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(output, json_file, indent=4)
        print(f"Saved JSON response for {output['resume_filename']} to {output_path}")

def convert_json_to_excel(json_directory, excel_output_path):
    all_data = []
    
    for json_file in os.listdir(json_directory):
        if json_file.endswith('.json'):
            with open(os.path.join(json_directory, json_file), 'r') as file:
                data = json.load(file)
                all_data.append(data)
    
    df = pd.json_normalize(all_data, sep='_')
    df.to_excel(excel_output_path, index=False)
    print(f"Converted JSON files to Excel at {excel_output_path}")

def main(input_directory, output_directory, excel_output_path, api_key):
    os.makedirs(output_directory, exist_ok=True)
    groq_client = Groq(api_key=api_key)
    
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(input_directory, pdf_file)
        json_output_path = os.path.join(output_directory, f"{os.path.splitext(pdf_file)[0]}.json")
        
        if os.path.exists(json_output_path):
            print(f"JSON file for {pdf_file} already exists. Skipping.")
            continue
        
        output = process_resume_groq(pdf_file_path, groq_client)
        
        if output:
            save_json(output, json_output_path)
    
    convert_json_to_excel(output_directory, excel_output_path)

if __name__ == "__main__":
    main(
        input_directory=r'C:\Abhiraj\7_Skills_Dataset\groq-skills-variation-fetch\input_resumes',
        output_directory=r'C:\Abhiraj\7_Skills_Dataset\groq-skills-variation-fetch\output',
        excel_output_path=r'C:\Abhiraj\7_Skills_Dataset\groq-skills-variation-fetch\output\resumes_output.xlsx',
        api_key="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"
    )
