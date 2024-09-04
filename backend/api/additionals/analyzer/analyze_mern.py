def validate_backend_structure(folder_structure):
    try:
        app_js_found = False
        controllers_found = False
        models_found = False
        routes_found = False
        package_json_found = False

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
                    found_items.append(item)
                if current_node['children']:
                    for child in current_node['children']:
                        found_items.extend(search_for_items([item], child, current_node['name']))
            return found_items

        # Validate the backend files (app.js, server.js, index.js, main.js)
        backend_file_found = False
        for file in required_files["backend_files"]:
            found_files = search_for_items([file], folder_structure[0])
            if found_files:
                # logger.info(f"{file} found in a valid backend folder.")
                print(f"{file} found in a valid backend folder.")
                backend_file_found = True
                app_js_found = True
                break
        if not backend_file_found:
            # logger.error("None of the required backend files (app.js, server.js, index.js, main.js) were found in a valid backend folder.")
            print("None of the required backend files (app.js, server.js, index.js, main.js) were found in a valid backend folder.")

        # Validate the backend folders (models, controllers, routes)
        for folder in required_files["backend_folders"]:
            found_folders = search_for_items([folder], folder_structure[0])
            if found_folders:
                if folder == "controllers":
                    controllers_found = True
                elif folder == "models":
                    models_found = True
                elif folder == "routes":
                    routes_found = True
                # logger.info(f"{folder} folder found.")
                print(f"{folder} folder found.")
            else:
                # logger.error(f"{folder} folder not found.")
                print(f"{folder} folder not found.")

        # Validate the package.json file
        package_json_found = validate_backend_package_json(folder_structure)
        if package_json_found:
            # logger.info("package.json found.")
            print("package.json found.")
        else:
            # logger.error("package.json not found in a valid backend folder.")
            print("package.json not found in a valid backend folder.")
        
        # Return the validation results
        files = {
            "app.js": app_js_found,
            "controllers": controllers_found,
            "models": models_found,
            "routes": routes_found,
            "package_json": package_json_found
        }

        if app_js_found and controllers_found and models_found and routes_found and package_json_found:
            return True, None
        else:
            not_found = []
            for file, found in files.items():
                if not found:
                    not_found.append(file)
            errors = [f"Missing required file or folder: {file}" for file in not_found]
            print(errors)
            return False, errors
    except Exception as e:
        # logger.error(f"An error occurred during backend structure validation: {str(e)}")
        print(f"An error occurred during backend structure validation: {str(e)}")
        return False, str(e)


def validate_backend_package_json(folder_structure):
    package_file = "package.json"
    frontend_folders = ["client", "frontend"]
    backend_folders = ["server", "backend", folder_structure[0]['name']]

    def search_for_package_json(current_node, parent_name=None):
        # If we find package.json, check the parent name
        if current_node['name'] == package_file:
            if parent_name in frontend_folders:
                return False
            elif parent_name in backend_folders or parent_name is None:
                return True
        # Recursively search through children
        for child in current_node['children']:
            result = search_for_package_json(child, current_node['name'])
            if result:
                return result
        return None

    # Start searching from the root level
    result = search_for_package_json(folder_structure[0])
    return result