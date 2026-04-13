from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    RegisterSerializer,
    ProfileUpdateSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data["email"].lower()
        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "Já existe uma conta com este email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            email=email,
            name=data["name"],
            password=data["password"],
            phone=data.get("phone", ""),
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "refresh_token é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Token inválido ou já expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "Logout realizado com sucesso."})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        if data.get("name") is not None:
            user.name = data["name"]
        if data.get("phone") is not None:
            user.phone = data["phone"]
        user.save(update_fields=["name", "phone", "updated_at"])
        return Response(UserSerializer(user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        if not user.check_password(data["current_password"]):
            return Response(
                {"detail": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(data["new_password"])
        user.save(update_fields=["password", "updated_at"])
        return Response({"message": "Senha alterada com sucesso."})


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: gerar token de reset e enviar e-mail quando o serviço de e-mail estiver configurado
        return Response(
            {"message": "Se este e-mail estiver cadastrado, você receberá as instruções em breve."}
        )


class AvatarUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        avatar = request.FILES.get("avatar")
        if not avatar:
            return Response(
                {"detail": "Nenhum arquivo enviado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        allowed = {"image/jpeg", "image/png", "image/webp"}
        if avatar.content_type not in allowed:
            return Response(
                {"detail": "Formato inválido. Use JPEG, PNG ou WebP."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if avatar.size > 5 * 1024 * 1024:
            return Response(
                {"detail": "Imagem muito grande. Máximo 5 MB."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        if user.avatar:
            user.avatar.delete(save=False)
        user.avatar.save(avatar.name, avatar, save=True)
        return Response(UserSerializer(user).data)
