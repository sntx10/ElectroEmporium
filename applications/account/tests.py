from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

from applications.account import views

User = get_user_model()


class AccountTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setup_user()


    @staticmethod
    def setup_user():
        user = User.objects.create_user(email='test@gmail.com', codeword='test', is_active=True, password='1234567')
        return user

    def test_post_register(self):
        data = {'email': 'test2@gmail.com', 'password': 1234567, 'password_repeat': 1234567,
                'codeword': 'test', 'phone_number': '+996700700700'}
        request = self.factory.post('/api/v1/account/register/', data)
        view = views.RegisterApiView.as_view()
        response = view(request)

        assert response.status_code == 201
        assert response.data['email'] == data.get('email')

    def test_post_register_error(self):
        data = {'email': 'test@gmail.com', 'password': 1234567, 'password_repeat': 1234567,
                'codeword': 'test', 'phone_number': '+996700700700'}
        request = self.factory.post('/api/v1/account/register/', data)
        view = views.RegisterApiView.as_view()
        response = view(request)

        assert response.status_code == 400

    def test_post_login(self):
        data = {'email': 'test@gmail.com', 'password': 1234567}
        request = self.factory.post('/api/v1/account/login/', data)
        view = TokenObtainPairView.as_view()
        response = view(request)

        assert response.status_code == 200

    def test_activate_login(self):
        activation = User.objects.first().activation_code
        request = self.factory.get(f'/api/v1/account/activate/{activation}')
        view = views.ActivationApiView.as_view()
        response = view(request, activation)

        assert response.status_code == 200
        assert response.data == {'msg': 'ваш аккаунт успешно активирован'}

    def test_change_password(self):
        data_change = {'old_password': '1234567', 'new_password': '123456', 'new_password_repeat': '123456'}
        request = self.factory.post('/api/v1/account/change_password/', data_change)
        force_authenticate(request, user=self.user)
        view = views.ChangePasswordApiView.as_view()
        response = view(request)

        assert response.status_code == 201

        data = {'email': 'test@gmail.com', 'password': data_change['old_password']}
        request = self.factory.post('/api/v1/account/login/', data)
        view = TokenObtainPairView.as_view()
        response_login = view(request)

        assert response_login.status_code == 401
        assert response_login.data['detail'] == 'No active account found with the given credentials'

    def test_forgot_password(self):
        data = {'email': 'test@gmail.com'}
        request = self.factory.post('/api/v1/account/forgot_password/', data)
        view = views.ForgotPasswordApiView.as_view()
        response = view(request)

        assert response.status_code == 201
        assert response.data == data

    def test_forgot_password_confirm(self):
        data = {'email': self.user.email, 'code': self.user.activation_code,
                'password': '123456', 'password_repeat': '123456'}
        request = self.factory.post('/api/v1/account/forgot_password_confirm/', data)
        view = views.ForgotPasswordConfirmApiView.as_view()
        response = view(request)

        assert response.status_code == 201
        assert response.data == {'email': 'test@gmail.com'}

    def test_forgot_password_codeword(self):
        data = {'email': self.user.email, 'codeword': self.user.codeword,
                'new_password': '123456', 'new_password_repeat': '123456'}
        request = self.factory.post('api/v1/account/forgot_password_codeword/', data)
        view = views.ForgotPasswordCodewordApiView.as_view()
        response = view(request)

        assert response.status_code == 201
