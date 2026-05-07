import os
import shutil
import json

base_dir = r"d:\website\raw-assets\projects"
dest_dir = r"d:\website\assets\img\projects"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

categories = {
    "full brand identity": "brand",
    "logos": "logo",
    "photo manipulation": "manipulation",
    "social media": "social"
}

projects_data = []

for category_dir_name, category_slug in categories.items():
    cat_path = os.path.join(base_dir, category_dir_name)
    if not os.path.exists(cat_path):
        continue
    
    for project_folder in os.listdir(cat_path):
        project_path = os.path.join(cat_path, project_folder)
        if not os.path.isdir(project_path):
            continue
        
        # Find thumbnail
        thumb_file = None
        for file in os.listdir(project_path):
            if file.lower().startswith("thumbnail"):
                thumb_file = file
                break
        
        if thumb_file:
            ext = os.path.splitext(thumb_file)[1]
            slug = project_folder.lower().replace(" ", "-")
            new_thumb_name = f"{slug}{ext}"
            
            src_file = os.path.join(project_path, thumb_file)
            dest_file = os.path.join(dest_dir, new_thumb_name)
            
            shutil.copy(src_file, dest_file)
            image_path = f"assets/img/projects/{new_thumb_name}"
        else:
            image_path = ""
            slug = project_folder.lower().replace(" ", "-")

        project_obj = {
            "id": slug,
            "title": project_folder.title() if project_folder != "المتحف المصري الكبير" else "المتحف المصري الكبير",
            "description": "Short description placeholder.",
            "image": image_path,
            "category": category_slug,
            "challenge": "Challenge text placeholder. Please provide the text from the PDF.",
            "solution": "Solution text placeholder. Please provide the text from the PDF."
        }
        projects_data.append(project_obj)

print("DATA_START")
print(json.dumps(projects_data, indent=4))
print("DATA_END")
