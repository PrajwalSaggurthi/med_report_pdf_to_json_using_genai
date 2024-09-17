from dotenv import dotenv_values
import google.generativeai as genai
import json
import PyPDF2 # For text-based PDFs
import re
# --- Configuration ---
GOOGLE_API_KEY = dotenv_values('.env').get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_json_From_GEMINI(pdf_path):
# --- PDF Extraction (Text-based example) ---
    pdf_file_path = pdf_path
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # --- Prompt Engineering --- 
    prompt = f"""
    # You are Formatting agent you work just like function, which reads the text and outputs the Json format, i want you to read the text below and make a perfect Json formatted response
    # DONOT NOT ADD ANYTHING OTHER THAN RESPONSE WITH JSON, NO CONSECUTIVE QUESTIONING, NO CONSTRUCTIVE CHATS.
    # DONOT ADD ANYTHING THAT IS NOT THERE IN THE PDF AND DONOT REPEAT THE VALUES OR COLUMNS.
    # DONOT USE MARKDOW TO GIVE RESPONSE, JUST {{key : values}} DONOT ADD ANYTHING.

    Text: 
    {text}
    # ADD EVERYTHING THAT IS THERE IN THE ABOVE TEXT, YOU MUST RETURN IN Json
    # DONOT ADD ANYTHING OUTSIDE OF PDF, ALSO DONT RETURN MARKDOWN BECAUSE YOU ARE FUNCTION WHICH RETURN JUST THE `Json`.

    Json Format:
    ```{{
            "Name": "Name of the person",
            "age": "age of the person",
            "Gender": "Male/Female",
            "Registration ID": "Registration Number",
            "Date": "Registration Date",
            "Tests": [
                        {{
                            "Test Name": "Name of Test1",
                            "Result1": "Results of Test1"
                            "BIOLOGICAL REFERENCE INTERVAL 1": "BIOLOGICAL REFERENCE INTERVAL range 1",
                            "Units 1": "Results Units 1"
                        }},
                        {{
                            "Test Name": "Name of Test2",
                            "Result2": "Results of Test2"
                            "BIOLOGICAL REFERENCE INTERVAL 2": "BIOLOGICAL REFERENCE INTERVAL range 2",
                            "Units 2": "Results Units 2"
                        }}
                    ]
    }}
    ```
    # YOU MUST GENERATE RESPONE IN ABOVE Json 

    """

    # --- Generate with Gemini ---
    response = model.generate_content(prompt)
    # match = re.search(r'```(.*?)```', response.text, re.DOTALL)
    # formatted_text = match.group(1)
    # --- JSON Parsing ---
    text = str(response.text)
    text = text.replace('```','')
    text = text.replace('Raw response: ','')
    text = text.replace('json', '')

    try:
        data = json.loads(text)
        print(data) 
        # output_json_path = 'output.json'  # You can customize the file name
        # with open(output_json_path, 'w') as outfile:
        #     json.dump(data, outfile, indent=4)
        return data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}") 
        print(f"Raw response: {response.text}")