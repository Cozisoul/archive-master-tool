# Archive Master v2

**Archive Master v2** is a command-line utility designed to streamline the content management workflow for the Thapelo Masebe digital ecosystem. Written in Python, this script acts as a local "CMS" (Content Management System), allowing for the quick, easy, and consistent ingestion of new projects into the static `projects.json` file that powers the Next.js front-end.

The core philosophy of this tool is to bridge the gap between a messy folder of raw image assets and a perfectly structured, data-driven portfolio. It automates the tedious tasks of ID generation, file renaming, and JSON formatting, allowing the artist to focus on the creative work itself.

## Core Features

-   **Project Creation:** Interactively create new project entries with prompts for title, tags, year, and description.
-   **Image Ingestion & Renaming:** Assign raw, numbered images (e.g., `24.jpg`, `30.jpg`) to a project. The script automatically renames these files to a clean, slug-based format (e.g., `reading-genesis-art-sale-1.jpg`) and updates the project's media gallery.
-   **Automatic Discovery:** Scan the image folder for pre-named project groups (e.g., `lebus-1.jpg`, `lebus-2.jpg`) and intelligently suggest them as new projects to be ingested.
-   **Safe & Idempotent:** The script is designed to be safe. It checks for existing files to prevent overwriting, loads and saves the JSON file carefully, and provides clear feedback to the user.
-   **Data Consistency:** Automatically generates sequential, correctly formatted project IDs (`proj-001`, `proj-002`, etc.) and sets the `coverImageUrl` based on the first image added.

## The Workflow

This script is the central tool in the content update process:

1.  **Prepare Assets:** Place all new, raw image files (which may have simple numeric names like `1.jpg`, `2.jpg`) into the designated `public/images/Thapelo Madiba Masebe Portfolio F` folder.
2.  **Run the Script:** Navigate to the project's root directory in your terminal and run the command:
    ```bash
    python archive_master_v2.py
    ```
3.  **Follow the Prompts:** Use the interactive menu to either create a new project from scratch, assign images to an existing project, or let the script discover new projects for you.
4.  **Commit & Push:** Once the script has run, it will have modified your `data/projects.json` file and renamed your image files. Simply commit these changes to your Git repository and push them.
5.  **Automatic Deployment:** Vercel (or your chosen hosting platform) will detect the push and automatically trigger a new production build of your Next.js site with the updated content.

## Technical Details

-   **Language:** Python 3
-   **Dependencies:** None (uses only standard libraries like `os`, `json`, and `re`).
-   **Configuration:** All core paths (the JSON file location and the image folder) are defined as constants at the top of the script for easy modification.

### Key Functions

-   `slugify(text)`: Converts any string into a URL-safe, lowercase, hyphenated slug.
-   `load_projects()` / `save_projects(projects)`: Safely read from and write to the `projects.json` file.
-   `assign_numbered_images(project, projects)`: The core logic for finding, renaming, and linking raw image files to a project entry.
-   `discover_and_ingest_projects(projects)`: The intelligent scanner that finds pre-named image groups and offers to convert them into full project entries.

## Future Roadmap

This tool can be expanded with more advanced features, such as:
-   Directly integrating with a headless CMS API.
-   Adding support for video files.
-   Generating `chaosLayout` coordinates automatically.
-   Providing an option to edit existing project metadata.