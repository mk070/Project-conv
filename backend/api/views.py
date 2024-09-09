from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from . import utils
from .additionals.analyzer import analyze_mern
from .additionals.converters import mern_to_django
from django.conf import settings
import os
import logging

logger = logging.getLogger('api')


class ProjectUploadView(APIView):
    def post(self, request, *args, **kwargs):
        print('\n-----------------------------------------------------------------------\n')
        uploads_path = settings.UPLOADS_PATH
        folder_structure = None
        is_valid = False
        
        source_stack = request.data.get('sourceStack')
        github_link = request.data.get('github_link', None)

        logger.info(f'Source stack: {source_stack}')

        if github_link:
            logger.info(f'Github link provided: {github_link}')
            repo_path = utils.handle_github_link(uploads_path, github_link)
            folder_structure = utils.parse_project_structure(repo_path)
        
        else:
            file = request.FILES['file']
            logger.info(f'File uploaded: {file.name}')
            file_upload_path = utils.handle_upload(uploads_path, file)
            folder_structure = utils.parse_project_structure(file_upload_path)        

        if source_stack == "mern":
            is_valid, response = analyze_mern.validate_backend_structure(folder_structure)
            request.session['MERN_PROJECT_FILES'] = response

        if is_valid:
            logger.info('Analyzation successful. Project structure is valid.')
            print('\n-----------------------------------------------------------------------\n')
            return Response({'message': 'Project structure is valid.',
                                'folderStructure': folder_structure}, status=status.HTTP_200_OK)
        else: 
            logger.error('Analyzation failed. Project structure is invalid.')
            print('\n-----------------------------------------------------------------------\n')
            return Response({'error': response}, status=status.HTTP_400_BAD_REQUEST)


class ProjectConvertView(APIView):
    def post(self, request, *args, **kwargs):
        print('\n-----------------------------------------------------------------------\n')
        
        # Get the target stack from the request (e.g., 'mern', 'django')
        source_stack = request.data.get('sourceStack')
        target_stack = request.data.get('targetStack')

        logger.info(f'Source stack: {source_stack}')
        logger.info(f'Target stack: {target_stack}')

        if source_stack == "mern" and target_stack == "django":
            logger.info('Converting MERN project to Django project...')
            conversion_status, message = mern_to_django.run(request.session['MERN_PROJECT_FILES'], settings.CONVERTED_PATH)
            print('\n-----------------------------------------------------------------------\n')

            if conversion_status == False:
                return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                django_project_path = os.path.join(settings.CONVERTED_PATH, 'backend')
                zip_file_name = os.path.join(settings.CONVERTED_PATH, 'django_project.zip')
                utils.zip_project(django_project_path, zip_file_name)
                logger.info(f'Zip file created successfully for {target_stack.upper()} project.')
                print('\n-----------------------------------------------------------------------\n')
                with open(zip_file_name, 'rb') as file:
                    response = HttpResponse(file, content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename={zip_file_name}'
                    return response
        else:
            logger.error('Invalid source or target stack.')
            print('\n-----------------------------------------------------------------------\n')
            return Response({'error': 'Invalid source or target stack.'}, status=status.HTTP_400_BAD_REQUEST)