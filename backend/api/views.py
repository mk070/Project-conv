import os
import zipfile
import shutil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .utils import handle_github_link, parse_project_structure, validate_project_structure

class ProjectUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        upload_dir = os.path.join('media', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        github_link = request.data.get('github_link', None)
        if github_link:
            repo_path = handle_github_link(github_link)
            folder_structure = parse_project_structure(repo_path)
        else:
            file = request.FILES['file']
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            extract_path = os.path.join(upload_dir, os.path.splitext(file.name)[0])
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            # Remove the zip file after extraction
            os.remove(file_path)

            folder_structure = parse_project_structure(extract_path)

        # Get the source stack from the request (e.g., 'mern', 'django')
        source_stack = request.data.get('sourceStack')

        # Validate the project structure
        is_valid, errors = validate_project_structure(folder_structure, source_stack)

        if not is_valid:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'folderStructure': folder_structure}, status=status.HTTP_200_OK)
