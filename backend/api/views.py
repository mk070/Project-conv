from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import utils
from .additionals.analyzer import analyze_mern
from .additionals.subprocess import subprocess_django
from backend import settings

class ProjectUploadView(APIView):
    def post(self, request, *args, **kwargs):
        print('\n-----------------------------------------------------------------------\n')
        uploads_path = settings.UPLOADS_PATH
        folder_structure = None
        is_valid = False
        error = None
        
        github_link = request.data.get('github_link', None)

        if github_link:
            repo_path = utils.handle_github_link(uploads_path, github_link)
            folder_structure = utils.parse_project_structure(repo_path)
        
        else:
            file = request.FILES['file']
            file_upload_path = utils.handle_upload(uploads_path, file)
            folder_structure = utils.parse_project_structure(file_upload_path)

        # Get the source stack from the request (e.g., 'mern', 'django')
        source_stack = request.data.get('sourceStack')

        if source_stack == "mern":
            is_valid, error = analyze_mern.validate_backend_structure(folder_structure)
            print('\n-----------------------------------------------------------------------\n')

        if is_valid:
            return Response({'message': 'Project structure is valid.',
                                'folderStructure': folder_structure}, status=status.HTTP_200_OK)
        else: 
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)


class ProjectConvertView(APIView):
    def post(self, request, *args, **kwargs):
        print('\n-----------------------------------------------------------------------\n')
        
        # Get the target stack from the request (e.g., 'mern', 'django')
        target_stack = request.data.get('targetStack')

        if target_stack == "django":
            subprocess_django.create_django_project(settings.CONVERTED_PATH)
            
            print('\n-----------------------------------------------------------------------\n')

            