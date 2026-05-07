import json
import re

with open(r'd:\website\gallery_json.json', 'r', encoding='utf-8') as f:
    gallery_data = json.load(f)

with open(r'd:\website\assets\js\main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

def replace_id(match):
    id_str = match.group(1)
    galleries = gallery_data.get(id_str, [])
    # replace backslashes if any in galleries
    safe_galleries = [g.replace("\\", "/") for g in galleries]
    galleries_json = json.dumps(safe_galleries)
    return f'id: "{id_str}",\n        gallery: {galleries_json},'

new_js = re.sub(r'id:\s*"([^"]+)",(?:\s*gallery:\s*\[.*?\],)*', replace_id, js_content)

with open(r'd:\website\assets\js\main.js', 'w', encoding='utf-8') as f:
    f.write(new_js)

print('INJECTED GALLERY!')
