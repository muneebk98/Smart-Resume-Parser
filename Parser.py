import zipfile
import os
import re
import json
import logging

from constants import email_pattern, phone_pattern, skills_keywords

path = 'resume_samples.zip'

class Parser:
    def __init__(self, zip_path, extract_path="extracted_resumes"):
        self.zip_path = zip_path
        self.extract_path = extract_path
        self.txt_files = []

    def extract_zip_folder(self):
        logging.info('We are extracting zip folder')
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_path)
        except Exception as e:
            logging.error(f"Failed to extract zip: {e}")

    def get_txt_files(self):
        self.txt_files = []
        logging.info('Only using .txt files')
        for root, dirs, files in os.walk(self.extract_path):
            for file in files:
                if file.lower().endswith(".txt"):
                    full_path = os.path.join(root, file)
                    self.txt_files.append(full_path)
        return self.txt_files

    def parse_files(self):
        data = []
        logging.info('Parsing data')
        for path in self.txt_files:
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

    def save_json(self, data):
        try:
            with open("parsed_resumes.json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            logging.error(f"Error saving JSON: {e}")

def main():
    p = Parser(path)
    p.extract_zip_folder()
    p.get_txt_files()
    data = p.parse_files()
    p.save_json(data)

main()
