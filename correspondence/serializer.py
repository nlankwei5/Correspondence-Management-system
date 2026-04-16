from rest_framework import serializers 
from .models import *



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']



class UserSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=True
    )
    department_details = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username',
            'first_name', 'last_name',
            'department',          
            'department_details'   
        ]



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