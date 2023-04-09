from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def create(self, validated_data):
        data = {'email': validated_data.get('email', None)}
        user = User(**data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()
