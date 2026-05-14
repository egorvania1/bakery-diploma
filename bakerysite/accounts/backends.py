class AuthenticationBackend(backends.ModelBackend):
    def authenticate(self, request,  username=None, password=None, **kwargs):
        usermodel = get_user_model()
        print(usermodel)

        try:
            user = usermodel.objects.get(Q(username__iexact=username) | Q(
                email__iexact=username) | Q(profile__phonenumber__iexact=username))
            if user.check_password(password):
                return user
        except user.DoesNotExist:
            pass
