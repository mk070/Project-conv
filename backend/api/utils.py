import os
import git
import zipfile
import shutil
import stat
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger('api')

def handle_github_link(uploads_path, github_link):
    try:
        logger.info(f'Cloning repository from: {github_link}')
        repo_name = github_link.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(uploads_path, repo_name)
        if os.path.exists(uploads_path):
            clean_folder(uploads_path)
        os.makedirs(repo_path, exist_ok=True)
        git.Repo.clone_from(github_link, repo_path)
        logger.info(f'Repository cloned successfully to: {repo_path}')
        return repo_path
    
    except Exception as e:
        logger.error(f'Failed to clone repository: {str(e)}')
        raise APIException(f"Failed to clone repository: {str(e)}")
    

def handle_upload(uploads_path, file):
    try:
        if os.path.exists(uploads_path):
            clean_folder(uploads_path)
        os.makedirs(uploads_path, exist_ok=True)

        file_path = os.path.join(uploads_path, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        extract_path = os.path.join(uploads_path, os.path.splitext(file.name)[0])
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(uploads_path)

        # Remove the zip file after extraction
        os.remove(file_path)
        logger.info(f'File uploaded and extracted successfully to: {extract_path}')
        return extract_path
    
    except Exception as e:
        logger.error(f'Failed to handle upload: {str(e)}')
        raise APIException(f"Failed to handle upload: {str(e)}")


def parse_project_structure(base_path):
    try:
        def create_node(name, path):
            return {
                'name': name,
                'path': path,
                'children': []
            }

        def add_node(root, path_parts, file_name, full_file_path):
            if not path_parts:
                root['children'].append(create_node(file_name, full_file_path))
                return
            for child in root['children']:
                if child['name'] == path_parts[0]:
                    add_node(child, path_parts[1:], file_name, full_file_path)
                    return
            new_node_path = os.path.join(root['path'], path_parts[0]) if root['path'] else path_parts[0]
            new_node = create_node(path_parts[0], new_node_path.replace('\\', '/'))
            root['children'].append(new_node)
            add_node(new_node, path_parts[1:], file_name, full_file_path)

        folder_structure = []
        root = create_node(os.path.basename(base_path), base_path.replace('\\', '/'))
        for root_dir, dirs, files in os.walk(base_path):
            for file_name in files:
                relative_dir = os.path.relpath(root_dir, base_path).replace('\\', '/')
                path_parts = relative_dir.split('/') if relative_dir != '.' else []
                full_file_path = os.path.join(root_dir, file_name).replace('\\', '/')
                add_node(root, path_parts, file_name, full_file_path)
        folder_structure.append(root)
        logger.info(f'Parsed project structure successfully' )
        return folder_structure
    
    except Exception as e:
        logger.error(f'Failed to parse project structure: {str(e)}')
        raise APIException(f"Failed to parse project structure: {str(e)}")


def zip_project(project_path, zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, project_path))
    except Exception as e:
        raise APIException(f"Failed to zip project: {str(e)}")


def clean_folder(FOLDER_PATH):
    if os.path.exists(FOLDER_PATH):
        def remove_readonly(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        shutil.rmtree(FOLDER_PATH, onerror=remove_readonly)
    os.makedirs(FOLDER_PATH)