import logging

logger = logging.getLogger('api')

def validate_backend_structure(folder_structure):
    try:
        app_js_path = None
        controllers_path = None
        models_path = None
        routes_path = None
        package_json_path = None

        backend_folders = ["server", "backend", folder_structure[0]["name"]]
        required_files = {
            "backend_files": ["app.js", "server.js", "index.js", "main.js"],
            "backend_folders": ["models", "controllers", "routes"]
        }

        # Function to recursively search for files or folders
        def search_for_items(items, current_node, parent_name=None):
            found_items = []
            for item in items:
                if item == current_node['name'] and (parent_name in backend_folders or parent_name is None):
                    found_items.append({"name": item, "path": current_node['path']})
                if current_node['children']:
                    for child in current_node['children']:
                        found_items.extend(search_for_items([item], child, current_node['name']))
            return found_items

        # Validate the backend files (app.js, server.js, index.js, main.js)
        backend_file_found = False
        for file in required_files["backend_files"]:
            found_files = search_for_items([file], folder_structure[0])
            if found_files:
                logger.info(f"{file} found in a valid backend folder at {found_files[0]['path']}")
                backend_file_found = True
                app_js_path = found_files[0]['path']
                break
        if not backend_file_found:
            logger.error("None of the required backend files (app.js, server.js, index.js, main.js) were found in a valid backend folder.")

        # Validate the backend folders (models, controllers, routes)
        for folder in required_files["backend_folders"]:
            found_folders = search_for_items([folder], folder_structure[0])
            if found_folders:
                if folder == "controllers":
                    controllers_path = found_folders[0]['path']
                elif folder == "models":
                    models_path = found_folders[0]['path']
                elif folder == "routes":
                    routes_path = found_folders[0]['path']
                logger.info(f"{folder} folder found at {found_folders[0]['path']}.")
            else:
                logger.error(f"{folder} folder not found.")

        # Validate the package.json file
        package_json_path = validate_backend_package_json(folder_structure)
        if package_json_path:
            logger.info(f"package.json found at {package_json_path}.")
        else:
            logger.error("package.json not found in a valid backend folder.")
        
        # Return the validation results
        files = {
            "app_js": app_js_path,
            "controllers": controllers_path,
            "models": models_path,
            "routes": routes_path,
            "package_json": package_json_path
        }

        if app_js_path and controllers_path and models_path and routes_path and package_json_path:
            return True, files
        else:
            not_found = []
            for file, path in files.items():
                if not path:
                    not_found.append(file)
            errors = [f"Missing required file or folder: {file}" for file in not_found]
            logger.error(f"Backend structure validation failed: {errors}")
            return False, errors
    except Exception as e:
        logger.error(f"An error occurred during backend structure validation: {str(e)}")
        return False, str(e)


def validate_backend_package_json(folder_structure):
    package_file = "package.json"
    frontend_folders = ["client", "frontend"]
    backend_folders = ["server", "backend", folder_structure[0]['name']]

    def search_for_package_json(current_node, parent_name=None):
        # If we find package.json, check the parent name
        if current_node['name'] == package_file:
            if parent_name in frontend_folders:
                return None
            elif parent_name in backend_folders or parent_name is None:
                return current_node['path']
        # Recursively search through children
        for child in current_node['children']:
            path = search_for_package_json(child, current_node['name'])
            if path:
                return path
        return None

    # Start searching from the root level
    path = search_for_package_json(folder_structure[0])
    return path