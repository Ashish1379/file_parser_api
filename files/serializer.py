from rest_framework.serializers import ModelSerializer
from .models import Files

class FilesSerializer(ModelSerializer):
    class Meta:
        model = Files
        fields = "__all__"
        

class FilesListSerializer(ModelSerializer):
    class Meta:
        model = Files
        fields = ["id" , 'filename' , "status" , "created_at"]

        
