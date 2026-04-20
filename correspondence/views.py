from django.shortcuts import render
from .serializer import * 
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import FileResponse 



class IncomingViewSet(viewsets.ModelViewSet):
    queryset = IncomingCorrespondence.objects.all()
    serializer_class = IncomingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['received_date', 'filed', 'source']
    search_fields = ['subject']
    ordering_fields = ['received_date'] 
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)


class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['dispatch_date', 'approval', 'filed']
    search_fields = ['subject']
    ordering_fields = ['dispatch_date'] 
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)

class LettersViewSet(viewsets.ModelViewSet):
    queryset = Letters.objects.all()
    serializer_class = LettersSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['date_sent']
    search_fields = ['subject']
    ordering_fields = ['date_sent'] 
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]