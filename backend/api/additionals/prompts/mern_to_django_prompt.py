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

The below is the `package.json` file:

<START OF package.json CONTENT>
{package_json_content}
<END OF package.json CONTENT>
"""
    return prompt


def to_settings_prompt(app_js_content, settings_content):
    prompt = f"""
You are an expert AI specializing in converting project configuration files. Your task is to convert an app.js file from a MERN stack backend project into a Django-compatible settings.py file.

**Instructions:**
1. Convert all relevant configurations in the provided `app.js` file to their equivalent Python configurations for a `settings.py` file in a Django project.
2. Retain the default `settings.py` file content provided below, especially the database configurations, and do not modify them.
3. In Application Definition, add necessary configurations for compatibility with a Django project, including:
    - Defining the app name 'app' and including it in the `INSTALLED_APPS` list.
    - Adding 'corsheaders' and 'rest_framework' to the `INSTALLED_APPS` list.
4. Add necessary configurations in Middleware Definition for compatibility with a React.js frontend, including:
   - Adding corsheaders middleware "corsheaders.middleware.CorsMiddleware" for CORS.
   - Configuring default session management for Django.
5. Leave the TEMPLATES configuration as it is, without any modifications.
6. Leave the Database configuration as it is, without any modifications. Let it be SQLite3.
7. Ensuring other essential configurations to work without any flaws.
8. Define the CORS Settings for Django to allow requests from the React.js frontend.
   - Allow all origins by setting `CORS_ORIGIN_ALLOW_ALL` to `True`.
   - Add `CORS_ALLOW_CREDENTIALS` and set it to `True`.
9. The output should only contain the final `settings.py` file content without any additional explanations or metadata.
10. Ensure the file is syntactically correct and free of errors.

The below is the default settings.py file:

<START OF DEFAULT settings.py CONTENT>
{settings_content}
<END OF DEFAULT settings.py CONTENT>

The below is the app.js file:

<START OF MERN app.js CONTENT>
{app_js_content}
<END OF MERN app.js CONTENT>
"""
    return prompt


def to_models_prompt(models_content):
    prompt = f"""
You are an expert AI specializing in converting data models between frameworks. Your task is to convert the provided MERN stack models from a MongoDB-based schema to their equivalent SQL-based schema for a Django project.

**Instructions:**

1. Convert all the data models from the provided MERN stack models to their equivalent Django models using SQL databases.
2. Ensure the models are defined using Django's models.Model and SQL-based field types such as CharField, IntegerField, BooleanField, ForeignKey, ManyToManyField, etc.
3. Maintain the structure of the models, including the field names, types, default values, and relationships.
4. Ensure all fields are appropriately defined for an SQL-based database, avoiding any references to NoSQL or MongoDB-specific features.
5. Make sure to include __str__() methods where applicable, using human-readable fields like name or title for representation.
6. The output should be Python code containing the Django models, formatted for a models.py file. Do not include any additional explanations or metadata.

The below is the MERN stack models content:

<START OF MERN MODELS CONTENT>
{models_content}
<END OF MERN MODELS CONTENT>
"""
    return prompt


def to_views_prompt(controllers_content):
    prompt = f"""
You are an expert AI specializing in converting server-side logic between frameworks. Your task is to convert the provided MERN stack controllers from an Express.js backend to equivalent Django views.

**Instructions:**
1. Convert all the logic from the provided Express.js controllers to Django views using standard Django views (not Django REST framework).
2. Do not use serializers, or any other external modules or dependencies from the Django REST framework.
3. Maintain the same function names from the MERN controllers when converting to Django views, as they will be used directly in `urls.py`.
4. Ensure the views follow Django's best practices for handling requests, responses, and database queries without requiring any external files or modules.
5. Only return the Python code containing the views in Django format—no additional explanations or metadata should be included.

The below is the MERN stack controllers content:

<START OF MERN CONTROLLERS CONTENT>
{controllers_content}
<END OF MERN CONTROLLERS CONTENT>
"""
    return prompt


def to_urls_prompt(routes_content):
    prompt = f"""
You are an expert AI specializing in converting routing configurations between frameworks. Your task is to convert the provided MERN stack routing configuration from an Express.js backend into equivalent Django `urls.py` routing for an app.

**Instructions:**
1. Convert all the routes from the provided Express.js routing file to Django's `urls.py` format using standard Django routing (`path()` or `re_path()`).
2. Do not use Django REST framework's `router` or any serializers—stick to Django’s standard view routing.
3. Ensure that each route points to the correct view function using the same function names as defined in the converted Django views. The function names from the MERN stack controllers should remain the same in the Django views and `urls.py`.
4. Properly handle route parameters and dynamic segments as they are in the MERN routes, using Django’s path converters if necessary.
5. Only return the Python code containing the URL configurations in Django format—no additional explanations or metadata should be included.

The below is the MERN stack routes content:

<START OF MERN ROUTES CONTENT>
{routes_content}
<END OF MERN ROUTES CONTENT>
"""
    return prompt