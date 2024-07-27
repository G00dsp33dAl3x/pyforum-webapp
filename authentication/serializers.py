from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'surname', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        new_user = self.Meta.model(**validated_data)
        if password is not None:
            new_user.set_password(password)
        new_user.save()
        return new_user

    def update(self, user, validated_data):
        for field in ['email', 'name', 'surname']:
            if field in validated_data:
                setattr(user, field, validated_data[field])

        new_password = validated_data.get('password')
        if new_password:
            user.set_password(new_password)
        user.save()
        return user
