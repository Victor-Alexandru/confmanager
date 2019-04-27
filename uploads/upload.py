from django.http import FileResponse
import os
def upload_response(request, file):
    print(os.getcwd())
    return FileResponse(open('./uploads/' + file,  'rb'), content_type='application/pdf',  as_attachment=True)
