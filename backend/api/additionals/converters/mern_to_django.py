from api.additionals.subprocess_projects import subprocess_django
from api.additionals.llm import mern_to_django_llm
from api.additionals.remove_markers import remove_code_markers
import os

def to_requirements(MERN_PROJECT_FILES, PATH):
    try:
        BACKEND_PATH = os.path.join(PATH, 'backend')
        requirements_txt_path = os.path.join(BACKEND_PATH, 'requirements.txt')
        package_json_path = MERN_PROJECT_FILES['package_json']

        package_json_content = ""
        with open(package_json_path, 'r') as file:
            package_json_content = file.read()
                
        response = mern_to_django_llm.to_requirements_llm(package_json_content)
        clean_response = remove_code_markers(response)
        
        with open(requirements_txt_path, 'w') as file:
            file.write(clean_response)

        return True, "Requirements converted successfully."    

    except Exception as e:
        return False, f"Failed to convert requirements: {str(e)}"
    

def to_settings(MERN_PROJECT_FILES, PATH):
    try:
        BACKEND_PROJECT_PATH = os.path.join(PATH, 'backend', 'backend')
        settings_path = os.path.join(BACKEND_PROJECT_PATH, 'settings.py')
        app_js_path = MERN_PROJECT_FILES['app_js']

        app_js_content = ""
        with open(app_js_path, 'r') as file:
            app_js_content = file.read()

        settings_content = ""
        with open(settings_path, 'r') as file:
            settings_content = file.read()

        response = mern_to_django_llm.to_settings_llm(app_js_content, settings_content)
        clean_response = remove_code_markers(response)
        
        with open(settings_path, 'w') as file:
            file.write(clean_response)

        return True, "Settings converted successfully."    

    except Exception as e:
        return False, f"Failed to convert settings: {str(e)}"


def to_models(MERN_PROJECT_FILES, PATH):
    try:
        BACKEND_APP_PATH = os.path.join(PATH, 'backend', 'app')
        models_path = os.path.join(BACKEND_APP_PATH, 'models.py')
        mern_models_folder = MERN_PROJECT_FILES['models']
        
        models_content = ""
        for file in os.listdir(mern_models_folder):
            with open(os.path.join(mern_models_folder, file), 'r') as f:
                models_content += f"### {file}\n{f.read()}\n"

        response = mern_to_django_llm.to_models_llm(models_content)
        clean_response = remove_code_markers(response)
        
        with open(models_path, 'w') as file:
            file.write(clean_response)

        return True, "Models converted successfully."    

    except Exception as e:
        return False, f"Failed to convert models: {str(e)}"


def to_views(MERN_PROJECT_FILES, PATH):
    try:
        BACKEND_APP_PATH = os.path.join(PATH, 'backend', 'app')
        views_path = os.path.join(BACKEND_APP_PATH, 'views.py')
        mern_controllers_folder = MERN_PROJECT_FILES['controllers']
        
        controllers_content = ""
        for file in os.listdir(mern_controllers_folder):
            with open(os.path.join(mern_controllers_folder, file), 'r') as f:
                controllers_content += f"### {file}\n{f.read()}\n"

        response = mern_to_django_llm.to_views_llm(controllers_content)
        clean_response = remove_code_markers(response)
        
        with open(views_path, 'w') as file:
            file.write(clean_response)

        return True, "Views converted successfully."    

    except Exception as e:
        return False, f"Failed to convert views: {str(e)}"


def to_urls(MERN_PROJECT_FILES, PATH):
    try:
        BACKEND_APP_PATH = os.path.join(PATH, 'backend', 'app')
        urls_path = os.path.join(BACKEND_APP_PATH, 'urls.py')
        mern_routes_folder = MERN_PROJECT_FILES['routes']
        
        routes_content = ""
        for file in os.listdir(mern_routes_folder):
            with open(os.path.join(mern_routes_folder, file), 'r') as f:
                routes_content += f"### {file}\n{f.read()}\n"

        response = mern_to_django_llm.to_urls_llm(routes_content)
        clean_response = remove_code_markers(response)
        
        with open(urls_path, 'w') as file:
            file.write(clean_response)

        return True, "URLs converted successfully."
    
    except Exception as e:
        return False, f"Failed to convert URLs: {str(e)}"


def run(MERN_PROJECT_FILES, PATH):
    subprocess_django.create_django_project(PATH)
    
    req_status, req_message = to_requirements(MERN_PROJECT_FILES, PATH)
    if not req_status:
        return False, req_message
    
    settings_status, settings_message = to_settings(MERN_PROJECT_FILES, PATH)
    if not settings_status:
        return False, settings_message

    models_status, models_message = to_models(MERN_PROJECT_FILES, PATH)
    if not models_status:
        return False, models_message

    views_status, views_message = to_views(MERN_PROJECT_FILES, PATH)
    if not views_status:
        return False, views_message

    urls_status, urls_message = to_urls(MERN_PROJECT_FILES, PATH)
    if not urls_status:
        return False, urls_message   