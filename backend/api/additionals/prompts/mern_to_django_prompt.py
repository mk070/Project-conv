def to_requirements_prompt(package_json_content):
    prompt = f"""
You are an expert AI specializing in converting project dependency files. Your task is to convert a `package.json` file from a MERN stack backend project into a Django-compatible `requirements.txt` file.

**Instructions:**
1. Convert all the dependencies listed in the provided `package.json` to their equivalent Python packages for a Django project.
2. Ensure the converted dependencies are listed in the correct `requirements.txt` format, including any necessary versions.
3. Only return the content that would be in the `requirements.txt` file. 
4. Do not include any extra explanations, descriptions, or metadata. The output should be a single snippet containing only the list of Python packages and their versions.
5. If a direct equivalent does not exist for a package, find the most commonly used alternative in the Django ecosystem while maintaining similar functionality.
6. Ensure that the `requirements.txt` file is syntactically correct and free of errors.
7. The output should strictly follow the format of a `requirements.txt` file without any additional text.

Here is the `package.json` file:

{package_json_content}
"""
    return prompt


def to_settings_prompt(app_js_content, settings_content):
    prompt = f"""
You are an expert AI specializing in converting project configuration files. Your task is to convert an app.js file from a MERN stack backend project into a Django-compatible settings.py file.

**Instructions:**
1. Convert all relevant configurations in the provided `app.js` file to their equivalent Python configurations for a `settings.py` file in a Django project.
2. Retain the default `settings.py` file content provided below, especially the database configurations, and do not modify them.
3. Add necessary configurations for compatibility with a React.js frontend, including:
   - Adding corsheaders middleware for CORS.
   - Configuring default session management for Django.
4. Ensuring other essential configurations to work without any flaws.
5. The output should only contain the final `settings.py` file content without any additional explanations or metadata.
6. Ensure the file is syntactically correct and free of errors.

Here is the default settings.py file:

{settings_content}

Here is the app.js file:

{app_js_content}
"""
    return prompt


def to_models_prompt(models_content):
    prompt = f"""

"""
    return prompt


def to_views_prompt(controllers_content):
    prompt = f"""

"""
    return prompt


def to_urls_prompt(routes_content):
    prompt = f"""

"""
    return prompt