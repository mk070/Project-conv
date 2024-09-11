from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from . import utils
from .additionals.analyzer import analyze_mern
from .additionals.converters import mern_to_django
from django.conf import settings
from .globals import MERN_PROJECT_FILES
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
            global MERN_PROJECT_FILES
            MERN_PROJECT_FILES = response

        if is_valid:
            logger.info('Analyzation successful. Project structure is valid.')
            print('\n-----------------------------------------------------------------------\n')
            print('MERN_PROJECT_FILES_DATA in UPLOAD: ', )
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
            try:
                logger.info('Converting MERN project to Django project...')
                global MERN_PROJECT_FILES
                print('MERN_PROJECT_FILES_DATA in CONVERT: ', MERN_PROJECT_FILES)
                utils.clean_folder(settings.CONVERTED_PATH)
                conversion_status, message = mern_to_django.run(MERN_PROJECT_FILES, settings.CONVERTED_PATH)
                print('\n-----------------------------------------------------------------------\n')

                if conversion_status == False:
                    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
                
                django_project_path = os.path.join(settings.CONVERTED_PATH, 'backend')
                zip_status, zip_message = utils.zip_project(django_project_path)
                
                if zip_status:
                    logger.info(f'Zip file created successfully for {target_stack.upper()} project.')
                    print('\n-----------------------------------------------------------------------\n')
                else:
                    logger.error(f'Failed to create zip file for {target_stack.upper()} project.')
                    print('\n-----------------------------------------------------------------------\n')
                    return Response({'error': zip_message}, status=status.HTTP_400_BAD_REQUEST)        
              
                return Response({'message': 'Project converted successfully. Click to download as ZIP file.'}, status=status.HTTP_200_OK)
            
            except Exception as e:
                logger.error(f'Failed to convert project: {str(e)}')
                print('\n-----------------------------------------------------------------------\n')
                return Response({'error': f'Failed to convert project: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)    
       
        else:
            logger.error('Invalid source or target stack.')
            print('\n-----------------------------------------------------------------------\n')
            return Response({'error': 'Invalid source or target stack.'}, status=status.HTTP_400_BAD_REQUEST)


class ProjectDownloadView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            zip_file_path = os.path.join(settings.CONVERTED_PATH, 'django_converted.zip')
            if os.path.exists(zip_file_path):
                with open(zip_file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename=django_converted.zip'
                    return response
            else:
                return Response({'error': 'Zip file not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Failed to download project: {str(e)}')
            return Response({'error': f'Failed to download project: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)