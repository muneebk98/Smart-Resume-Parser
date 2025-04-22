import zipfile
import os
import re
import json
import logging

path = 'resume_samples.zip'
extract = 'extracted_resumes'

email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
phone_pattern = r'(\+92-\d{3}-\d{7})|(0\d{3}-\d{7})'
skills_keywords = ["Python", "Java", "C++", "SQL", "Django", "React","Communication", "JavaScript", "Machine Learning","Data Analysis","Node.js"]

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
    print("Valid resume files:")
    for tf in txt_files:
        print(tf)
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

                found_skills = []
                for skill in skills_keywords:
                    if skill.lower() in content.lower():
                        found_skills.append(skill)

                resume_info["skills"] = found_skills

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

#printing json file
def print_json():
    try:
        with open("parsed_resumes.json", "r", encoding="utf-8") as file:
            data_r = json.load(file)
        for resume in data_r:
            print(resume)
    except Exception as e:
        logging.error(f"Error reading or parsing JSON: {e}")


def main():
    extract_zip_folder()
    txt_files = get_txt_files()
    data = parse_files(txt_files)
    save_json(data)
    print_json()

main()
