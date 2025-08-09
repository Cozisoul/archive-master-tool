# archive_master_v2.py

import os
import json
import re
from collections import defaultdict

# --- CONFIGURATION ---
JSON_PATH = 'data/projects.json'
IMAGE_FOLDER = 'public/images/Thapelo Madiba Masebe Portfolio F'
# --- END CONFIGURATION ---

def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[^a-z0-9\s-]+', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text

def load_projects():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_projects(projects):
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)
    print("\n✅ Changes have been saved to projects.json.")

def get_next_project_id(projects):
    if not projects: return "proj-001"
    max_id = 0
    for p in projects:
        if p.get('id', '').startswith('proj-'):
            try:
                num = int(p['id'].split('-')[1])
                if num > max_id: max_id = num
            except (ValueError, IndexError): continue
    return f"proj-{(max_id + 1):03d}"

def parse_index_range(input_str):
    indices = set()
    for part in input_str.split(','):
        part = part.strip()
        if not part: continue
        if '-' in part:
            start, end = map(int, part.split('-'))
            indices.update(range(start, end + 1))
        else:
            indices.add(int(part))
    return sorted(list(indices))

def find_image_file_by_index(index):
    base_name = str(index)
    for ext in ['.jpg', '.jpeg', '.png', '.svg', '.gif']:
        path = os.path.join(IMAGE_FOLDER, base_name + ext)
        if os.path.exists(path): return base_name + ext
    return None

def assign_numbered_images(project, projects):
    if not project:
        print("❌ No project selected.")
        return
    image_indices_str = input(f"\nEnter image indices for '{project['title']}' (e.g., '24, 30-35'): ").strip()
    if not image_indices_str: return

    try:
        indices = parse_index_range(image_indices_str)
        media_list = project.get('media', [])
        
        for index in indices:
            old_filename = find_image_file_by_index(index)
            if not old_filename:
                print(f"⚠️ WARNING: Image for index {index} not found.")
                continue
            
            project_slug = slugify(project['title'])
            new_file_index = len(media_list) + 1
            new_filename = f"{project_slug}-{new_file_index}{os.path.splitext(old_filename)[1]}"
            
            old_path = os.path.join(IMAGE_FOLDER, old_filename)
            new_path = os.path.join(IMAGE_FOLDER, new_filename)
            
            if os.path.exists(new_path):
                print(f"⚠️ WARNING: Filename '{new_filename}' already exists. Skipping.")
                continue

            os.rename(old_path, new_path)
            print(f"✅ Renamed '{old_filename}' to '{new_filename}'")
            
            web_path = f"/images/Thapelo Madiba Masebe Portfolio F/{new_filename}"
            media_list.append({"type": "image", "url": web_path})

        project['media'] = media_list
        if not project.get('coverImageUrl') and project.get('media'):
            project['coverImageUrl'] = project['media'][0]['url']
        
        save_projects(projects)

    except ValueError:
        print("❌ ERROR: Invalid index format.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_project_from_prompts(projects):
    title = input("Enter the new project title: ").strip()
    if not title: return None
    
    new_project = {
        "id": get_next_project_id(projects),
        "title": title,
        "tags": [t.strip() for t in input("Enter tags, comma-separated: ").split(',')],
        "year": int(input("Enter year: ")),
        "description": input("Enter description: "),
        "coverImageUrl": "", "media": [], "projectUrl": "",
        "chaosLayout": {"x": 100, "y": 100, "width": "350px", "rotation": 0}
    }
    projects.append(new_project)
    print(f"\nProject '{title}' created with ID {new_project['id']}.")
    return new_project

def discover_and_ingest_projects(projects):
    print("\nScanning for pre-named project image groups...")
    existing_slugs = {slugify(p['title']) for p in projects}
    
    # Group files by their base name (e.g., 'lebus-1' and 'lebus-2' both group under 'lebus')
    potential_projects = defaultdict(list)
    for filename in os.listdir(IMAGE_FOLDER):
        match = re.match(r'([a-z0-9-]+)-\d+\..+', filename)
        if match:
            slug = match.group(1)
            if slug not in existing_slugs:
                potential_projects[slug].append(filename)

    if not potential_projects:
        print("No new, pre-named project groups found.")
        return

    for slug, files in potential_projects.items():
        title_guess = slug.replace('-', ' ').title()
        choice = input(f"\nFound group '{slug}' with {len(files)} images. Create project '{title_guess}'? (y/n): ").strip().lower()
        if choice == 'y':
            new_project = {
                "id": get_next_project_id(projects),
                "title": title_guess,
                "tags": [slug] + [t.strip() for t in input("Enter additional tags, comma-separated: ").split(',')],
                "year": int(input("Enter year: ")),
                "description": input("Enter description: "),
                "coverImageUrl": "",
                "media": [{"type": "image", "url": f"/images/Thapelo Madiba Masebe Portfolio F/{f}"} for f in sorted(files)],
                "projectUrl": "",
                "chaosLayout": {"x": 100, "y": 100, "width": "350px", "rotation": 0}
            }
            if new_project['media']:
                new_project['coverImageUrl'] = new_project['media'][0]['url']
            
            projects.append(new_project)
            print(f"✅ Project '{title_guess}' created and ingested.")
        else:
            print(f"Skipping group '{slug}'.")
    
    save_projects(projects)

def main():
    while True:
        projects = load_projects()
        project_map = {p['title'].lower(): p for p in projects}

        print("\n--- Thapelo Masebe Archival Master v2 ---")
        print("1: Assign numbered images to an EXISTING project")
        print("2: Create a NEW project (from numbered images)")
        print("3: Discover and ingest pre-named project folders")
        print("4: Exit")
        
        choice = input("> ").strip()

        if choice == '1':
            print("\nWhich existing project to add images to?")
            for title in project_map.keys(): print(f"  - {title.title()}")
            proj_choice = input("> ").strip().lower()
            
            found_project = None
            for title, data in project_map.items():
                if proj_choice in title:
                    found_project = data
                    break
            
            if found_project:
                assign_numbered_images(found_project, projects)
            else:
                print("Project not found.")

        elif choice == '2':
            new_project = create_project_from_prompts(projects)
            if new_project:
                assign_numbered_images(new_project, projects)

        elif choice == '3':
            discover_and_ingest_projects(projects)
            
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()