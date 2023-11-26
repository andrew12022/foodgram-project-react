from api.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
