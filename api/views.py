from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import RegularUser, Moderator, Category, HashTag, Image

from .serializers import (
    RegularUserSerializer, ModeratorSerializer, CategorySerializer, HashTagSerializer, ImageSerializer,
)


# ----------------------------------------------------------------------------------------------------------------------
# Users views

class UserRegistrationAuthorization(ModelViewSet):
    serializer_class = RegularUserSerializer
    queryset = RegularUser.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            return self.__authorisation(
                self.request.GET['username'],
                self.request.GET['password'],
            )
        except KeyError:
            return Response([])

    def create(self, request, *args, **kwargs):
        login, password = self.__encode_password(request)
        response = super(UserRegistrationAuthorization, self).create(request, *args, **kwargs)
        if response.status_code is status.HTTP_201_CREATED:
            return self.__authorisation(login, password)
        return response

    @staticmethod
    def __encode_password(request):
        try:
            password = request.data['profile']['password']
            request.data['profile']['password'] = make_password(password=password)
            return request.data['profile']['username'], password
        except KeyError:
            pass

    def __authorisation(self, login, password):
        user = get_object_or_404(self.queryset, profile__username=login)
        if check_password(password, user.profile.password):
            token, created = Token.objects.get_or_create(user=user.profile)
            return Response({
                "token": token.key
            })
        else:
            return Response({'error': 'Wrong password'}, status=status.HTTP_403_FORBIDDEN)


class ModeratorRegistrationAuthorization(UserRegistrationAuthorization):
    serializer_class = ModeratorSerializer
    queryset = Moderator.objects.all()


# ----------------------------------------------------------------------------------------------------------------------
# Image views

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name',)


class HashTagViewSet(ModelViewSet):
    serializer_class = HashTagSerializer
    queryset = HashTag.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name', 'categories__name',)


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name', 'hash_tags__name', 'hash_tag__categories__name')
