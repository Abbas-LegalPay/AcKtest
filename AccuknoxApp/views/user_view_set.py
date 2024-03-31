from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet

from utility.results_pagination import StandardResultsSetPagination
from ..serializers import *
from ..models import *


class UserViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["email", "first_name", "last_name"]
    filterset_fields = ["email", "first_name", "last_name"]
    pagination_class = StandardResultsSetPagination
    serializer_class = UserSerializer

    def get_queryset(self):
        return AccuKnoxUser.objects.all()

    def create(self, request, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user is not None:
                login(request, user)
                token = Token.objects.get_or_create(user=user)[0].key
                return Response({'message': 'Login successful', 'Token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
