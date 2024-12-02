from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора регистрации пользователя.
    """
    password = serializers.CharField(label='Пароль', required=True, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        """
        Метод проверки данных пользователя.

        :param data: Данные для регистрации пользователя
        :return: Валидные данные
        :raises ValidationError: Вызывает исключение при невалидных данных
        """
        errors = {}
        try:
            validate_password(password=data['password'], user=User(**data))
        except ValidationError as err:
            errors['password'] = list(err.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super(RegisterUserSerializer, self).validate(data)

    def create(self, validated_data):
        """
        Метод создания пользователя.

        :param validated_data: Валидные данные для создания пользователя
        :return: Экземпляр созданного пользователя
        """
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )


class LoginUserSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора авторизации пользователя.

    *Здесь поле email явно переопределено для исправления бага "Такая почта уже зарегистрирована"
    DRF начинает проверять почту на существование в таблице (если не объявить поле явно, то
    в нём будет UniqueValidator() который и вызывает валидацию, а она выбрасывает исключение).*
    """
    email = serializers.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        """
        Метод проверки данных пользователя.

        :param data: Данные для авторизации пользователя
        :return: Валидные данные
        :raises ValidationError: Вызывает исключение при невалидных данных
        """
        email = data['email']
        password = data['password']
        if email and not User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError({'email': "Такая почта не зарегистрирована"})
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise serializers.ValidationError({'password': "Неверные данные"})
        return super(LoginUserSerializer, self).validate(data)
