from django.shortcuts import render
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework import permissions
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import login,logout,authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework.views import APIView
class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id==request.user.id

class RegistrationView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()
    # permission_classes=[permissions.IsAuthenticated]

    def get_permissions(self):
        user=self.request.user
        method=self.request.method

        if not user.is_authenticated:
            if method in ["GET","POST"]:
                return [permissions.AllowAny()]
            return [permissions.IsAuthenticated()]
        

        #set permission for non admin user 


        if user.is_authenticated and not user.is_staff:
            if method in ['GET','PUT','DELETE','PATCH']:
                return [IsOwnerPermission()]
            else:
                return [permissions.IsAdminUser()]
        
        return [permissions.IsAdminUser()]
    def create(self, request, *args, **kwargs):
         if self.request.user.is_authenticated and not self.request.user.is_staff:
            raise PermissionDenied("Only unauthenticated users can register.")
         
         return super().create(request, *args, **kwargs)



# class for login

class LoginView(APIView):
    def post(self,request):
        if request.user.is_authenticated:
            return Response({'error':"only unauthenticated user can access"})

        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get('username')
            password=serializer.validated_data.get('password')
          
            user=authenticate(username=username,password=password)
            if user:
                login(request, user)
                refresh=RefreshToken.for_user(user)
               
                return Response({'refresh': str(refresh),
        'access': str(refresh.access_token),'id':user.id,'is_staff':user.is_staff},status=status.HTTP_200_OK)
            return Response({"error":"Invalid User"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        logout(request)
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
       
        return Response({'detail':"Successfully logout"})