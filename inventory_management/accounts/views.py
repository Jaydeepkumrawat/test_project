# from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from . serializers import CustomTokenObtainPairSerializer

from accounts.models import Account
from . serializers import RegisterSerializer

class RegisterView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer
    # authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'detail': 'Registration successfully done.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'detail': 'Somthing went wrong.', 'error': serializer.errors}, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    