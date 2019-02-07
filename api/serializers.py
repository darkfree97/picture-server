from rest_framework import serializers

from core.models import User, RegularUser, Moderator, Image, Category, HashTag
from core.constants import STATUS


# ----------------------------------------------------------------------------------------------------------------------
# Users serializers

class ProfileSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True,)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password',)


class RegularUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    status = serializers.ChoiceField(choices=STATUS.choices)

    class Meta:
        model = RegularUser
        fields = ('id', 'profile', 'status',)

    def create(self, validated_data):
        profile = User.objects.create(**validated_data['profile'])
        regular_user = RegularUser.objects.create(profile=profile, status=validated_data['status'])
        return regular_user


class ModeratorSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    status = serializers.ChoiceField(choices=STATUS.choices)

    class Meta:
        model = Moderator
        fields = ('id', 'profile', 'status',)

    def create(self, validated_data):
        profile = User.objects.create(**validated_data['profile'])
        moderator = Moderator.objects.create(profile=profile, status=validated_data['status'])
        return moderator


# ----------------------------------------------------------------------------------------------------------------------
# Image serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class HashTagSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all(), write_only=True)
    categories_detailed = serializers.SerializerMethodField()

    class Meta:
        model = HashTag
        fields = ('id', 'name', 'categories', 'categories_detailed',)

    @staticmethod
    def get_categories_detailed(obj):
        return CategorySerializer(obj.categories, many=True).data


class ImageSerializer(serializers.ModelSerializer):

    hash_tags = serializers.PrimaryKeyRelatedField(many=True, queryset=HashTag.objects.all(), write_only=True)
    hash_tags_detailed = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'title', 'image', 'hash_tags', 'hash_tags_detailed',)

    @staticmethod
    def get_hash_tags_detailed(obj):
        return HashTagSerializer(obj.hash_tags, many=True).data
