import os
import google.generativeai as genai
from dotenv import load_dotenv
from api.additionals.prompts import mern_to_django_prompt
import logging

logger = logging.getLogger('api')

# Load environment variables
load_dotenv()

# Load the API key from the environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def to_requirements_llm(package_json_content):
    try:
        logger.info('LLM Triggered: Converting requirements')
        refined_prompt = mern_to_django_prompt.to_requirements_prompt(package_json_content)
        prompt = [
            {
                'role': 'user',
                'parts': [refined_prompt]
            }
        ]
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        # print(response)
        return response.text
    except Exception as e:
        logger.error(f'Failed to convert requirements: {str(e)}')
        raise Exception(f"Failed to convert requirements: {str(e)}")


def to_settings_llm(app_js_content, settings_content):
    try:
        logger.info('LLM Triggered: Converting settings')
        refined_prompt = mern_to_django_prompt.to_settings_prompt(app_js_content, settings_content)
        prompt = [
            {
                'role': 'user',
                'parts': [refined_prompt]
            }
        ]
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        # print(response)
        return response.text
    except Exception as e:
        logger.error(f'Failed to convert settings: {str(e)}')
        raise Exception(f"Failed to convert settings: {str(e)}")


def to_models_llm(models_content):
    try:
        logger.info('LLM Triggered: Converting models')
        refined_prompt = mern_to_django_prompt.to_models_prompt(models_content)
        prompt = [
            {
                'role': 'user',
                'parts': [refined_prompt]
            }
        ]
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        # print(response)
        return response.text
    except Exception as e:
        logger.error(f'Failed to convert models: {str(e)}')
        raise Exception(f"Failed to convert models: {str(e)}")


def to_views_llm(controllers_content):
    try:
        logger.info('LLM Triggered: Converting views')
        refined_prompt = mern_to_django_prompt.to_views_prompt(controllers_content)
        prompt = [
            {
                'role': 'user',
                'parts': [refined_prompt]
            }
        ]
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        # print(response)
        return response.text
    except Exception as e:
        logger.error(f'Failed to convert views: {str(e)}')
        raise Exception(f"Failed to convert views: {str(e)}")
    

def to_urls_llm(routes_content):
    try:
        logger.info('LLM Triggered: Converting urls')
        refined_prompt = mern_to_django_prompt.to_urls_prompt(routes_content)
        prompt = [
            {
                'role': 'user',
                'parts': [refined_prompt]
            }
        ]
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        # print(response)
        return response.text
    except Exception as e:
        logger.error(f'Failed to convert urls: {str(e)}')
        raise Exception(f"Failed to convert urls: {str(e)}")