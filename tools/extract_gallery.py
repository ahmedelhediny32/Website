import os, shutil, json
base_dir = r'd:\website\raw-assets\projects'
dest_dir = r'd:\website\assets\img\gallery'
if not os.path.exists(dest_dir): os.makedirs(dest_dir)

categories = {'full brand identity': 'brand', 'logos': 'logo', 'photo manipulation': 'manipulation', 'social media': 'social'}
project_galleries = {}

for cat_name, cat_slug in categories.items():
    cat_path = os.path.join(base_dir, cat_name)
    if not os.path.exists(cat_path): continue
    for proj in os.listdir(cat_path):
        proj_path = os.path.join(cat_path, proj)
        if not os.path.isdir(proj_path): continue
        slug = proj.lower().replace(' ', '-')
        if 'المتحف' in slug or 'egyptian' in slug: slug = 'المتحف-المصري-الكبير'
        if 'safwa' in slug: slug = 'safwa-restaurant'
        
        proj_dest = os.path.join(dest_dir, slug)
        if not os.path.exists(proj_dest): os.makedirs(proj_dest)
        
        gallery = []
        for root, _, files in os.walk(proj_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    rel = os.path.relpath(os.path.join(root, file), proj_path)
                    safe = rel.replace('\\\\', '/').replace(' ', '-')
                    if file.lower().startswith('thumb'): continue
                    dest_file = os.path.join(proj_dest, rel.replace(' ', '-'))
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    shutil.copy(os.path.join(root, file), dest_file)
                    
                    web_path = f"assets/img/gallery/{slug}/{rel.replace(' ', '-').replace(os.sep, '/')}"
                    gallery.append(web_path)
        project_galleries[slug] = gallery

with open(r'd:\website\gallery_json.json', 'w', encoding='utf-8') as f:
    json.dump(project_galleries, f, ensure_ascii=False)
