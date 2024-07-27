from rest_framework import serializers
from profiles.models import ProfilesImage, SavedCompany

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilesImage
        fields = ['name', 'path']

class MainPageSerializer(serializers.ModelSerializer):
    image = ProfileImageSerializer()

    class Meta:
        model = SavedCompany
        fields = ['company', 'added_at', 'image']

class MainApiResponse(serializers.Serializer):
    clients = MainPageSerializer(many=True)
    partners = ProfileImageSerializer(many=True)

