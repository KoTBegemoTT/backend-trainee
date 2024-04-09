from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'token'

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if token is None:
            return None
        return self.authenticate_credentials(token)
