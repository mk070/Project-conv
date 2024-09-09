import subprocess
import os
from api import utils
import logging

logger = logging.getLogger('api')

def create_django_project(PATH):
    try:
        base_dir =  PATH
        project_name = "backend"
        app_name = "app"

        utils.clean_folder(base_dir)

        # Change the current directory to the CONVERTED_FOLDER
        os.chdir(base_dir)

        logger.info(f"Creating Django project at: {base_dir}")

        # Create the Django project
        subprocess.run(['django-admin', 'startproject', project_name], check=True)

        # Navigate to the newly created Django project directory
        os.chdir(os.path.join(base_dir, project_name))

        logger.info(f"Django project created successfully at: {base_dir}")

        logger.info(f"Creating Django app: \"{app_name}\"")

        # Create the app within the Django project
        subprocess.run(['python', 'manage.py', 'startapp', app_name], check=True)

        logger.info(f"Django app created successfully: \"{app_name}\"")

        # Create the urls.py file in the app directory
        create_urls_py(base_dir, project_name, app_name)

        # Include the app's urls.py in the project's urls.py
        include_app_urls(base_dir, project_name, app_name)

        logger.info("Django project setup completed successfully")
        print('\n-----------------------------------------------------------------------\n')

    except Exception as e:
        logger.error(f"Failed to create Django project: {str(e)}")
        print('\n-----------------------------------------------------------------------\n')
        raise Exception(f"Failed to create Django project: {str(e)}")

def create_urls_py(base_dir, project_name, app_name):    
    # Path to the app directory
    app_dir = os.path.join(base_dir, project_name, app_name)

    # Create the urls.py file in the app directory
    urls_file_path = os.path.join(app_dir, 'urls.py')
    
    # Content to be written in urls.py
    urls_content = """from django.urls import path

urlpatterns = [
    # Define your URL patterns here
]
""" 
    # Write the content to urls.py
    with open(urls_file_path, 'w') as f:
        f.write(urls_content)

    logger.info(f"Created urls.py (backend) at: {urls_file_path}")
    

def include_app_urls(base_dir, project_name, app_name):
    # Path to the project's urls.py file
    proj_urls_file_path = os.path.join(base_dir, project_name, project_name, 'urls.py')

    # Content to be added to the project's urls.py file
    import_statement = "from django.urls import path, include\n"
    app_url_pattern = f"path('', include('{app_name}.urls')),"

    if os.path.exists(proj_urls_file_path):
        with open(proj_urls_file_path, 'r+') as f:
            content = f.read()

            # Add include method in import
            if "from django.urls import path" in content:
                content = content.replace("from django.urls import path", import_statement)

            # Check if the app URL pattern is already in urlpatterns
            if app_url_pattern.strip() not in content:
                # Add the app URL pattern to the urlpatterns
                content = content.replace("urlpatterns = [", f"urlpatterns = [\n    {app_url_pattern}")

            # Overwrite the file with the updated content
            f.seek(0)
            f.write(content)
            f.truncate()

        logger.info(f"Updated urls.py at: {proj_urls_file_path}")
    else:
        logger.error(f"urls.py not found at: {proj_urls_file_path}")