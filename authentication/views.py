from django.contrib.auth.views import PasswordResetConfirmView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser
from .serializers import CustomUserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UsersDetailView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs['id']
        query = CustomUser.objects.filter(id=user_id, is_staff="False")
        return get_object_or_404(query)


class AllUsersDetailView(ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(is_staff='False').order_by('id')



# class CustomPasswordReset(PasswordResetConfirmView):
#     serializer_class = CustomUserSerializer
#     permission_class = [AllowAny]


