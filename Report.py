import json
#loading data
def load():
    try:
        with open("parsed_resumes.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: parsed_resumes.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error: JSON is invalid or corrupted.")
        return []

    


#counting total data
def count_data(data):

    return len(data)
#counting skills
def count_skills(data):
    skills_list = ["Python", "Java", "C++", "SQL", "Django", "React","JavaScript", "Machine Learning","Data Analysis", "Node.js"]

    skill_counts = {}
    for resume in data:
        for skill in skills_list:
            if skill in resume["skills"]:
                if skill not in skill_counts:
                    skill_counts[skill] = 1
                else:
                    skill_counts[skill] += 1

    return skills_list, skill_counts
#sorting top 5
def top_5(skill_counts):
    items = list(skill_counts.items())
    items.sort(key=lambda pair: pair[1], reverse=True)
    top_five = items[:5]
    return top_five

#checking for missing resumes
def missing_resumes(data):
    missing = []
    for resume in data:
        if not resume["phone"] or not resume["skills"]:
            missing.append(resume["name"])
    return missing
#creating report
def write_report(total, top_skills, skills_list, skill_counts, missing):
    lines = []
    lines.append("===== Resume Summary Report =====\n")
    lines.append(f"Total resumes parsed: {total}\n")

    lines.append("\nTop 5 most common skills:")
    for skill, count in top_skills:
        lines.append(f"  {skill}: {count}")

    lines.append("\nSkill frequency:")
    for skill in skills_list:
        count = skill_counts.get(skill, 0)
        lines.append(f"  {skill}: {count}")

    lines.append("\nResumes missing phone or skills:")
    if missing:
        for filename in missing:
            lines.append(f"  - {filename}")
    else:
        lines.append("  None")

    lines.append("\n=================================\n")

    report_text = "\n".join(lines)

    with open("summary_report.txt", "w", encoding="utf-8") as report:
        report.write(report_text)

    print(report_text)


def main():
    data = load()
    total = count_data(data)
    skills_list, skill_counts = count_skills(data)
    top_skills = top_5(skill_counts)
    missing = missing_resumes(data)
    write_report(total, top_skills, skills_list, skill_counts, missing)
    print("summary_report.txt created")

main()
