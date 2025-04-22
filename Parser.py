import zipfile
import os
import re
import json
import logging

from constants import email_pattern, phone_pattern, skills_keywords


path = 'resume_samples.zip'
extract = 'extracted_resumes'


# Extracting zip file
def extract_zip_folder():
    logging.info('We are extracting zip folder')
    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(extract)
    except Exception as e:
        logging.error(f"Failed to extract zip: {e}")


def get_txt_files():
    txt_files = []
    # check for .txt files
    logging.info('Only using .txt files')
    for root, dirs, files in os.walk(extract):
        for file in files:
            if file.lower().endswith(".txt"):
                full_path = os.path.join(root, file)
                txt_files.append(full_path)
    return txt_files

def parse_files(txt_files):
    data = []
    logging.info('Parsing data')
    for path in txt_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                resume_info = {
                    "name": None,
                    "email": None,
                    "phone": None,
                    "skills": []
                }
                email_match = re.search(email_pattern, content)
                if email_match:
                    resume_info["email"] = email_match.group()

                phone_match = re.search(phone_pattern, content)
                if phone_match:
                    resume_info["phone"] = phone_match.group()

                resume_info["skills"] = [skill for skill in skills_keywords if skill.lower() in content.lower()]

                resume_info["name"]=[]

                lines = content.strip().splitlines()
                for line in lines:
                    if line.strip():
                        resume_info["name"] = line.strip()
                        break

                if not any([resume_info["name"], resume_info["email"], resume_info["phone"], resume_info["skills"]]):
                    logging.warning('File was empty')
                    continue
                else:
                    data.append(resume_info)

        except Exception as e:
            logging.error('File not opening')
            print(f"Failed to process {path}: {e}")
    return data

#creating json file after parsing 
def save_json(data):
    try:
        with open("parsed_resumes.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        logging.error(f"Error saving JSON: {e}")



def main():
    extract_zip_folder()
    txt_files = get_txt_files()
    data = parse_files(txt_files)
    save_json(data)

main()
