import fitz # PyMuPDF
import os
import shutil

src_dir = r"d:\website\raw-assets\projects\marketing"
gallery_dir = r"d:\website\assets\img\gallery\elite-core-gym"
projects_img_dir = r"d:\website\assets\img\projects"

os.makedirs(os.path.join(gallery_dir, "presentation"), exist_ok=True)
os.makedirs(os.path.join(gallery_dir, "social-media"), exist_ok=True)
os.makedirs(projects_img_dir, exist_ok=True)

# 1. Copy thumbnail
thumb_src = os.path.join(src_dir, "thumbinail.png")
if os.path.exists(thumb_src):
    print("Copying thumbnail...")
    shutil.copy(thumb_src, os.path.join(projects_img_dir, "elite-core-gym.png"))
else:
    print("Thumbnail not found!")

# 2. Extract PDF
pdf_path = os.path.join(src_dir, "presentation.pdf")
if os.path.exists(pdf_path):
    print("Extracting PDF slides...")
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        # render page to an image
        pix = page.get_pixmap(dpi=150)
        out_path = os.path.join(gallery_dir, "presentation", f"slide-{i+1}.png")
        pix.save(out_path)
    print(f"Extracted {len(doc)} slides.")
else:
    print("PDF not found!")

# 3. Copy social media
social_src = os.path.join(src_dir, "social media")
if os.path.exists(social_src):
    print("Copying social media posts...")
    for f in os.listdir(social_src):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            shutil.copy(os.path.join(social_src, f), os.path.join(gallery_dir, "social-media", f))
else:
    print("Social media directory not found!")
    
# Generate the gallery array for JS
gallery = []
for slide in os.listdir(os.path.join(gallery_dir, "presentation")):
    if slide.endswith(".png"):
        gallery.append(f"assets/img/gallery/elite-core-gym/presentation/{slide}")

for post in os.listdir(os.path.join(gallery_dir, "social-media")):
    if post.endswith((".png", ".jpg", ".jpeg")):
        gallery.append(f"assets/img/gallery/elite-core-gym/social-media/{post}")

print("Gallery JS Array:")
print(repr(gallery).replace("'", '"'))
