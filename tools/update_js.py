import re
import json

with open(r"d:\website\pdf_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Normalize spacing
lines = text.split("\n")
clean_lines = []
for line in lines:
    line = line.strip()
    if line:
        clean_lines.append(line)

full_text = " ".join(clean_lines)

# Split by project #
projects_raw = re.split(r'project\s*#\d+', full_text)[1:]

extracted_info = {}

for raw in projects_raw:
    # Extract name
    name_match = re.search(r'name:\s*(.*?)(?=\s*Overview)', raw, re.IGNORECASE)
    overview_match = re.search(r'Overview:?\s*(.*?)(?=\s*The Challenge)', raw, re.IGNORECASE)
    challenge_match = re.search(r'The Challenge:?\s*(.*?)(?=\s*The Solution)', raw, re.IGNORECASE)
    solution_match = re.search(r'The Solution:?\s*(.*?)(?=\s*(Logo|Social Media|mockups))', raw, re.IGNORECASE)
    
    if name_match:
        name = name_match.group(1).strip()
        slug = name.lower().replace(" ", "-")
        # Special case for Arabic name
        if 'المتحف' in name:
            slug = 'المتحف-المصري-الكبير'
            
        overview = overview_match.group(1).strip() if overview_match else "Overview not provided."
        challenge = challenge_match.group(1).strip() if challenge_match else "Challenge not provided."
        solution = solution_match.group(1).strip() if solution_match else "Solution not provided."
        
        extracted_info[slug] = {
            "title": name,
            "description": overview,
            "challenge": challenge,
            "solution": solution
        }

print("Extracted Info keys:", extracted_info.keys())

with open(r"d:\website\assets\js\main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# We need to replace the projectsData block safely.
# Let's write the JSON manually in Python and edit the file if possible.
# Actually, I'll print the extracted_info to stdout so the AI can use replace_file_content.
print("--- Extracted Data ---")
print(json.dumps(extracted_info, ensure_ascii=False, indent=4))
