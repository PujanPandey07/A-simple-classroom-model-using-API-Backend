from rest_framework import generics
from .models import CustomUser
from .Serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
