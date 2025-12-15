from django.contrib.auth import authenticate
from rest_framework import serializers

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Authenticate using the custom backend or manual lookup
            # Since standard authenticate() usually expects 'username', we need a backend that supports it OR manual check here.
            # Let's try to find user by email first, then check password.
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = 'No se puede iniciar sesión con las credenciales proporcionadas.'
                raise serializers.ValidationError(msg, code='authorization')
            
            if not user.check_password(password):
                msg = 'No se puede iniciar sesión con las credenciales proporcionadas.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Debe incluir "email" y "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
