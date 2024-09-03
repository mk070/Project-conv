import os
import git
import zipfile
import shutil
from rest_framework.exceptions import APIException

def handle_github_link(media_path, github_link):
    try:
        repo_name = github_link.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(media_path, 'repos', repo_name)
        if os.path.exists(media_path):
            shutil.rmtree(media_path)
        os.makedirs(repo_path)
        git.Repo.clone_from(github_link, repo_path)
        return repo_path
    except Exception as e:
        raise APIException(f"Failed to clone repository: {str(e)}")

def handle_upload(media_path, file):
    try:
        upload_path = os.path.join(media_path, 'uploads')
        if os.path.exists(media_path):
            shutil.rmtree(media_path)
        os.makedirs(upload_path)

        file_path = os.path.join(upload_path, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        extract_path = os.path.join(upload_path, os.path.splitext(file.name)[0])
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(upload_path)

        # Remove the zip file after extraction
        os.remove(file_path)

        return extract_path
    except Exception as e:
        raise APIException(f"Failed to handle upload: {str(e)}")

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

