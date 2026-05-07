import json

with open(r'd:\website\extracted_json.json', 'r', encoding='utf-8') as f:
    extracted = json.load(f)

with open(r'd:\website\assets\js\main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

start_idx = js_content.find('const projectsData = [')
end_idx = js_content.find('];', start_idx) + 2

categories_map = {
    'brand': ['bait-alasmak', 'phoenix-agency'],
    'logo': ['lumiere-candle', 'sweet-spot', 'tech-lab', 'المتحف-المصري-الكبير'],
    'manipulation': ['intersteller'],
    'social': ['delicacy-restaurant', 'dental-clinic', 'leeloudi-patisserie', 'perfume', 'quran-academy', 'safwa-restaurant', 'sehatna-medical-laboratories']
}

new_projects = []
for cat, slugs in categories_map.items():
    for slug in slugs:
        ext_data = extracted.get(slug, {})
        title = ext_data.get('title', slug.replace('-', ' ').title())
        desc = ext_data.get('description', 'Creative project')
        challenge = ext_data.get('challenge', 'Please see the gallery for more details.')
        solution = ext_data.get('solution', 'Visual designs available below.')
        
        if 'safwa' in slug:
            ext_data = extracted.get('al-safwa-restaurant', {})
            title = ext_data.get('title', title)
            desc = ext_data.get('description', desc)
            challenge = ext_data.get('challenge', challenge)
            solution = ext_data.get('solution', solution)

        proj = {
            'id': slug,
            'title': title,
            'description': desc.replace('"', '\\"'),
            'image': f'assets/img/projects/{slug}.png',
            'category': cat,
            'challenge': challenge.replace('"', '\\"'),
            'solution': solution.replace('"', '\\"')
        }
        new_projects.append(proj)

new_block = 'const projectsData = [\n'
lines = []
for p in new_projects:
    lines.append(f'''    {{
        id: "{p['id']}",
        title: "{p['title']}",
        description: "{p['description']}",
        image: "{p['image']}",
        category: "{p['category']}",
        challenge: "{p['challenge']}",
        solution: "{p['solution']}"
    }}''')
new_block += ',\n'.join(lines) + '\n];'

new_js = js_content[:start_idx] + new_block + js_content[end_idx:]

with open(r'd:\website\assets\js\main.js', 'w', encoding='utf-8') as f:
    f.write(new_js)

print("SUCCESSFULLY INJECTED!")
