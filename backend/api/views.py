from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import utils
from .additionals.analyzer import analyze_mern

class ProjectUploadView(APIView):
    def post(self, request, *args, **kwargs):
        print('\n-----------------------------------------------------------------------\n')
        github_link = request.data.get('github_link', None)
        media_path = 'media'
        folder_structure = None
        
        if github_link:
            repo_path = utils.handle_github_link(media_path, github_link)
            folder_structure = utils.parse_project_structure(repo_path)
        
        else:
            file = request.FILES['file']
            upload_path = utils.handle_upload(media_path, file)
            folder_structure = utils.parse_project_structure(upload_path)

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
