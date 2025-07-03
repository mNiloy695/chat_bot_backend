from django.shortcuts import render,redirect
from .models import ChatModel
from .serializers import ChatModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission
# Create your views here.

class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user==request.user

class ChatSerializerView(ModelViewSet):
    serializer_class=ChatModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]
    queryset=ChatModel.objects.all()
    def perform_create(self, serializer):
        # Assign the logged-in user as the owner automatically
        serializer.save(user=self.request.user)
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ChatModel.objects.filter(user=user)
        return ChatModel.objects.none()
    
   
        return super().dispatch(request, *args, **kwargs)
    def get_permissions(self):
        user=self.request.user
        if not user.is_authenticated:
             return [permissions.IsAuthenticated()]
        if user.is_authenticated:
            if self.request.method in ['GET','POST']:
                return [IsOwnerPermission()]
            elif self.request.method in ["DELETE"]:
                return [IsOwnerPermission()]
            return [permissions.IsAdminUser()]
                    


        return super().get_permissions()
