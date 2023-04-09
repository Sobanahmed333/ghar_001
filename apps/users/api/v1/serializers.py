from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

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


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, password):
        if not check_password(password, self.context.user.password):
            raise serializers.ValidationError(
                _("Invalid password."))
        return password

    def validate_new_password(self, password):
        if check_password(password, self.context.user.password):
            raise serializers.ValidationError(
                _("New password can't be same as old one."))
        return password
