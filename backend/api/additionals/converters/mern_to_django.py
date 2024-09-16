from api.additionals.subprocess_projects import subprocess_django
from api.additionals.llm import mern_to_django_llm
from api.additionals.remove_markers import remove_code_markers
import os
import logging

logger = logging.getLogger('api')

def to_requirements(MERN_PROJECT_FILES, PATH):
    try:
        BACKEND_PATH = os.path.join(PATH, 'backend')
        requirements_txt_path = os.path.join(BACKEND_PATH, 'requirements.txt')
        package_json_path = MERN_PROJECT_FILES['package_json']

        package_json_content = ""
        with open(package_json_path, 'r') as file:
            package_json_content = file.read()

        logger.info(f'Converting requirements from package.json: {package_json_path}')

        response = mern_to_django_llm.to_requirements_llm(package_json_content)
        clean_response = remove_code_markers(response)
        
        with open(requirements_txt_path, 'w') as file:
            file.write(clean_response)
        
        logger.info(f'Requirements converted successfully to: {requirements_txt_path}')

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

        logger.info(f'Converting settings from app.js: {app_js_path}')

        response = mern_to_django_llm.to_settings_llm(app_js_content, settings_content)
        clean_response = remove_code_markers(response)
        
        with open(settings_path, 'w') as file:
            file.write(clean_response)

        logger.info(f'Settings converted successfully to: {settings_path}')

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
        
        logger.info(f'Converting models from MERN project: {mern_models_folder}')

        response = mern_to_django_llm.to_models_llm(models_content)
        clean_response = remove_code_markers(response)
        
        with open(models_path, 'w') as file:
            file.write(clean_response)

        logger.info(f'Models converted successfully to: {models_path}')

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

        logger.info(f'Converting views from MERN project: {mern_controllers_folder}')

        response = mern_to_django_llm.to_views_llm(controllers_content)
        clean_response = remove_code_markers(response)
        
        with open(views_path, 'w') as file:
            file.write(clean_response)

        logger.info(f'Views converted successfully to: {views_path}')

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

        logger.info(f'Converting URLs from MERN project: {mern_routes_folder}')

        response = mern_to_django_llm.to_urls_llm(routes_content)
        clean_response = remove_code_markers(response)
        
        with open(urls_path, 'w') as file:
            file.write(clean_response)

        logger.info(f'URLs converted successfully to: {urls_path}')

        return True, "URLs converted successfully."
    
    except Exception as e:
        return False, f"Failed to convert URLs: {str(e)}"


def run(MERN_PROJECT_FILES, PATH):
    try:
        subprocess_django.create_django_project(PATH)

        conversions = [
            ("requirements", to_requirements),
            ("settings", to_settings),
            ("models", to_models),
            ("views", to_views),
            ("urls", to_urls),
        ]

        for name, conversion_fn in conversions:
            status, message = conversion_fn(MERN_PROJECT_FILES, PATH)
            if not status:
                logger.error(f'Failed to convert {name}: {message}')
                return False, message

        logger.info('MERN project converted to Django successfully.')
        return True, "MERN project converted to Django successfully."
    
    except Exception as e:
        logger.error(f'Failed to convert project: {str(e)}')
        return False, f"Failed to convert project: {str(e)}"