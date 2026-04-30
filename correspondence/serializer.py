from rest_framework import serializers 
from .models import *
from cloudinary.utils import cloudinary_url
import cloudinary


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'type']


class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username']


class UserSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True,
    )
    department_details = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username',
            'first_name', 'last_name',
            'is_active',
            'department',          
            'department_details'   
        ]
        read_only_fields = ['is_active']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 
                    'department', 'password', 're_password']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('re_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class IncomingSerializer(serializers.ModelSerializer):
    user_details = CreatedBySerializer(source='created_by', read_only=True)
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, obj):
        if obj.file and obj.file.public_id:
            public_id_with_ext = obj.file.public_id
            if not public_id_with_ext.endswith('.pdf'):
                public_id_with_ext += '.pdf'

            
            url, options = cloudinary_url(
                public_id_with_ext,
                resource_type='raw',          
                flags='attachment',           
                sign_url=True,                
                secure=True
            )
            return url
        return None
    class Meta:
        model = IncomingCorrespondence
        fields = ['id', 'subject', 'source', 'source_external', 'received_date', 'filed', 'file', 'created_by', 'user_details', 'file_url',]
        read_only_fields = ['created_by', 'file_url',]

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise  serializers.ValidationError("Only PDF files are allowed.")

        return value
        

class DispatchSerializer(serializers.ModelSerializer):

    user_details = CreatedBySerializer(source='created_by', read_only=True)
    file_url = serializers.SerializerMethodField()
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        many=True
    )
    filed = serializers.BooleanField(required=False, default=False)
    approval = serializers.BooleanField(required=False, default=False)
    

    def get_file_url(self, obj):
        if obj.file and obj.file.public_id:
            public_id_with_ext = obj.file.public_id
            if not public_id_with_ext.endswith('.pdf'):
                public_id_with_ext += '.pdf'

            
            url, options = cloudinary_url(
                public_id_with_ext,
                resource_type='raw',          
                flags='attachment',           
                sign_url=True,                
                secure=True
            )
            return url
        return None
    class Meta:
        model = Dispatch
        fields = ['id', 'subject', 'destination', 'dispatch_date', 'filed', 'approval', 'created_by','file', 'user_details','file_url']
        read_only_fields = ['created_by', 'file_url']





class LettersSerializer(serializers.ModelSerializer):

    user_details = CreatedBySerializer(source='created_by', read_only=True)
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, obj):
        if obj.file and obj.file.public_id:
            public_id_with_ext = obj.file.public_id
            if not public_id_with_ext.endswith('.pdf'):
                public_id_with_ext += '.pdf'

            
            url, options = cloudinary_url(
                public_id_with_ext,
                resource_type='raw',          
                flags='attachment',           
                sign_url=True,                
                secure=True
            )
            return url
        return None
    class Meta:
        model = Letters
        fields = ['id', 'subject', 'reference_number', 'receipient', 'date_sent', 'file', 'created_by', 'user_details', 'file_url']
        read_only_fields = ['created_by', 'file_url']

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise  serializers.ValidationError("Only PDF files are allowed.")

        return value