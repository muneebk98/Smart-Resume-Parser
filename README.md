# Smart-Resume-Parser


This Python project reads a set of `.txt` resumes, extracts key information, and generates a clean summary report using only built-in libraries.


## Project Overview

The program does the following:

1. Loads resumes from `parsed_resumes.json`.
2. Extracts and counts:
   - Name, Email, Phone, Skills
3. Generates a report that includes:
   - Total resumes parsed
   - Number of emails and phone numbers found
   - Top 5 most common skills
   - Skill frequency
   - Resumes missing phone or skills
4. Saves the report to `summary_report.txt` and also prints it to the console.

---

##  How to Run

1. Make sure `parsed_resumes.json` is in the same folder.
2. Run the Python file:

