python -m venv <name>

scripts/activate

pip install -r requirements.txt

django-admin startproject backend

python manage.py startapp <app_name>


session variables are used in django

### Frontend Configuration:
When making API calls from the React frontend, ensure that session cookies are sent with the request. You can configure this by using credentials: 'include' in your fetch or Axios calls.

Example with fetch:

```javascript```
fetch('http://localhost:8000/api/set_project_files', {
    method: 'GET',
    credentials: 'include'  // Ensures cookies are sent
}).then(response => response.json())
  .then(data => console.log(data));
  


## LAST WORKED ON
converters/mern_to_django -> need to write prompt for settings
=======

