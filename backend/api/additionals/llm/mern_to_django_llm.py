import os
import google.generativeai as genai
from dotenv import load_dotenv
from api.additionals.prompts import mern_to_django_prompt

# Load environment variables
load_dotenv()

# Load the API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def to_requirements_llm(package_json_content):
    refined_prompt = mern_to_django_prompt.to_requirements_prompt(package_json_content)
    prompt = [
        {
            'role': 'user',
            'parts': [refined_prompt]
        }
    ]
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response)
    return response.text


def to_settings_llm(app_js_content, settings_content):
    refined_prompt = mern_to_django_prompt.to_settings_prompt(app_js_content, settings_content)
    prompt = [
        {
            'role': 'user',
            'parts': [refined_prompt]
        }
    ]
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response)
    return response.text


def to_models_llm(models_content):
    refined_prompt = mern_to_django_prompt.to_models_prompt(models_content)
    prompt = [
        {
            'role': 'user',
            'parts': [refined_prompt]
        }
    ]
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response)
    return response.text


def to_views_llm(controllers_content):
    refined_prompt = mern_to_django_prompt.to_views_prompt(controllers_content)
    prompt = [
        {
            'role': 'user',
            'parts': [refined_prompt]
        }
    ]
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response)
    return response.text


def to_urls_llm(routes_content):
    refined_prompt = mern_to_django_prompt.to_urls_prompt(routes_content)
    prompt = [
        {
            'role': 'user',
            'parts': [refined_prompt]
        }
    ]
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response)
    return response.text