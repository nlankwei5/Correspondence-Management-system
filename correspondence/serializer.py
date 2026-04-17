from rest_framework import serializers 
from .models import *



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'type']



class UserSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True,
        read_only=True, 
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
    class Meta:
        model = IncomingCorrespondence
        fields = ['id', 'subject', 'source', 'source_external', 'received_date', 'filed', 'file', 'created_by']
        read_only_fields = ['created_by']

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise  serializers.ValidationError("Only PDF files are allowed.")

        return value
        

class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = ['id', 'subject', 'destination', 'dispatch_date', 'filed', 'approval', 'created_by']
        read_only_fields = ['created_by']





class LettersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letters
        fields = ['id', 'subject', 'reference_number', 'receipient', 'date_sent', 'file', 'created_by']
        read_only_fields = ['created_by']

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise  serializers.ValidationError("Only PDF files are allowed.")

        return value