from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

import threading 
from .process_files import process_file
from .models import Files
from .serializer import FilesSerializer, FilesListSerializer




def home(request):
    return HttpResponse("<h1>This is Home</h1>")

@api_view(['POST'])
def files_progress(request , file_id):
    file_object = get_object_or_404(Files , id = file_id)
    data = {
        "file_id": file_object.id,
        "status": file_object.status,
        "progress": file_object.progress
    }
    if(file_object.progress < 100):
        return Response(data , status=status.HTTP_202_ACCEPTED)
    else:
        return Response(data , status=status.HTTP_200_OK)


@api_view(['POST','GET'])
def files_operations(request):
    if request.method == 'GET':
        file_objec = Files.objects.all().order_by("created_at")
        if not file_objec:
            return Response({"message" : "nothing to show"}, status= status.HTTP_200_OK)
        serializer = FilesListSerializer(file_objec , many = True)
        return Response(serializer.data , status= status.HTTP_200_OK)
    

    if request.method == 'POST':
        file = request.FILES.get("file")
        if not file:
            data = {
                "error" : "No file detected"
            }
            return Response(data , status = status.HTTP_400_BAD_REQUEST)
        
        file_ins = Files( file= file ,filename = file.name,  status = "uploading" , progress = 0 )
        file_ins.save()

        threading.Thread(target = process_file , args = (file_ins.id , )).start()
        serializer = FilesSerializer(file_ins)
        return Response(serializer.data , status= status.HTTP_201_CREATED)


@api_view(['GET','DELETE'])
def files_CRUD(request , file_id):
    file_obj = get_object_or_404(Files , id = file_id)
    if request.method == 'GET':
        if file_obj.status == "uploading" or  file_obj.status == "processing":
            data = {
            "message": "File upload or processing in progress. Please try again later."
            }
            return Response(data , status = status.HTTP_425_TOO_EARLY)
        
        if file_obj.status == "failed":
            return Response({"message" : "File type not supported"} , status= status.HTTP_200_OK)
        return Response(file_obj.parsed_content , status= status.HTTP_200_OK)

    if request.method == 'DELETE':
        file_obj.delete()
        data = {
            "message": "File and its data deleted"
        }
        return Response(data , status=status.HTTP_200_OK)
    





