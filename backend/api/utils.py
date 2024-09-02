import os
import git
import shutil
from rest_framework.exceptions import APIException

def handle_github_link(github_link):
    try:
        repo_name = github_link.split('/')[-1].replace('.git', '')
        repo_path = os.path.join('media', 'repos', repo_name)
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        os.makedirs(repo_path)
        git.Repo.clone_from(github_link, repo_path)
        return repo_path
    except Exception as e:
        raise APIException(f"Failed to clone repository: {str(e)}")

def parse_project_structure(base_path):
    def create_node(name, path):
        return {
            'name': name,
            'path': path,
            'children': []
        }

    def add_node(root, path_parts, file_name):
        if not path_parts:
            root['children'].append(create_node(file_name, file_name))
            return
        for child in root['children']:
            if child['name'] == path_parts[0]:
                add_node(child, path_parts[1:], file_name)
                return
        new_node = create_node(path_parts[0], path_parts[0])
        root['children'].append(new_node)
        add_node(new_node, path_parts[1:], file_name)

    folder_structure = []
    root = create_node(os.path.basename(base_path), "")
    for root_dir, dirs, files in os.walk(base_path):
        for file_name in files:
            relative_dir = os.path.relpath(root_dir, base_path).replace('\\', '/')
            path_parts = relative_dir.split('/') if relative_dir != '.' else []
            add_node(root, path_parts, file_name)
    folder_structure.append(root)
    return folder_structure

def validate_project_structure(folder_structure, source_stack):
    """
    Validates the project structure based on the source tech stack.

    Args:
        folder_structure (list): The parsed folder structure.
        source_stack (str): The tech stack of the uploaded project (e.g., 'mern', 'django').

    Returns:
        tuple: A boolean indicating success, and a list of validation error messages.
    """

    # Example validation rules for different tech stacks
    required_files = {
        'mern': ['package.json', 'src/index.js'],
        'django': ['manage.py', 'requirements.txt']
    }

    missing_files = []
    for required_file in required_files.get(source_stack, []):
        if not find_file_in_structure(folder_structure, required_file):
            missing_files.append(required_file)

    if missing_files:
        return False, [f"Missing required file: {file}" for file in missing_files]

    return True, []

def find_file_in_structure(folder_structure, file_name):
    """
    Recursively searches for a specific file in the folder structure.

    Args:
        folder_structure (list): The parsed folder structure.
        file_name (str): The file name or relative path to search for.

    Returns:
        bool: True if the file is found, False otherwise.
    """
    for node in folder_structure:
        if node['path'] == file_name:
            return True
        if node['children']:
            if find_file_in_structure(node['children'], file_name):
                return True
    return False

