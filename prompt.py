prompt = '''
Act as a recruiter, automatically extracting and generating variations of key skills from a resumes.

NOTE:
Identify and extract all relevant skills and technical skills mentioned in a resumes.
For each extracted skill, generate common variations. For example:
For "MySQL": Include "MySQL," "My SQL," "My-SQL," and "SQL and MySQL."
For "Python": Include "Py," "Python3," and "Python 3.x."
For "JavaScript": Include "JS," "Java Script," and "ECMAScript."
Ensure that these variations are ready to be matched against candidate resumes, optimizing for ATS systems to ensure all relevant skills are recognized, regardless of their formatting.

FORMATTING INSTRUCTIONS:

Provide output only in the JSON format below. Do not add anything else.
Output JSON format:
json
{
    "skills": [
        {"skill_name": "skill_variations"}
    ]
}
'''