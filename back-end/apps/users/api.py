from django.contrib.auth import get_user_model
from ninja import Router, File, UploadedFile
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth

from .schemas import (
    RegisterIn,
    ProfileUpdateIn,
    ForgotPasswordIn,
    ChangePasswordIn,
    UserOut,
    TokenPairOut,
    MessageOut,
    ErrorOut,
)

User = get_user_model()
router = Router()


@router.post("/register", response={201: UserOut, 400: ErrorOut}, auth=None)
def register(request, payload: RegisterIn):
    """Cadastra um novo usuário e retorna seus dados."""
    email = payload.email.lower()
    if User.objects.filter(email=email).exists():
        raise HttpError(400, "Já existe uma conta com este email.")

    user = User.objects.create_user(
        email=email,
        name=payload.name,
        password=payload.password,
        phone=payload.phone,
    )
    return 201, UserOut.from_user(user)


@router.post("/logout", response={200: MessageOut}, auth=JWTAuth())
def logout(request, refresh_token: str):
    """Invalida o refresh token (blacklist)."""
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        raise HttpError(400, "Token inválido ou já expirado.")
    return 200, {"message": "Logout realizado com sucesso."}


@router.get("/me", response={200: UserOut}, auth=JWTAuth())
def me(request):
    """Retorna os dados do usuário autenticado."""
    return 200, UserOut.from_user(request.auth)


@router.patch("/profile", response={200: UserOut, 400: ErrorOut}, auth=JWTAuth())
def update_profile(request, payload: ProfileUpdateIn):
    """Atualiza nome e telefone do usuário autenticado."""
    user = request.auth
    if payload.name is not None:
        user.name = payload.name
    if payload.phone is not None:
        user.phone = payload.phone
    user.save(update_fields=["name", "phone", "updated_at"])
    return 200, UserOut.from_user(user)


@router.post("/change-password", response={200: MessageOut, 400: ErrorOut}, auth=JWTAuth())
def change_password(request, payload: ChangePasswordIn):
    """Altera a senha do usuário autenticado."""
    user = request.auth
    if not user.check_password(payload.current_password):
        raise HttpError(400, "Senha atual incorreta.")
    user.set_password(payload.new_password)
    user.save(update_fields=["password", "updated_at"])
    return 200, {"message": "Senha alterada com sucesso."}


@router.post("/forgot-password", response={200: MessageOut}, auth=None)
def forgot_password(request, payload: ForgotPasswordIn):
    """Inicia o fluxo de recuperação de senha.
    Sempre retorna 200 para não vazar se o e-mail existe.
    Por enquanto não envia e-mail — placeholder para integração futura.
    """
    # TODO: gerar token de reset e enviar e-mail quando o serviço de e-mail estiver configurado
    return 200, {"message": "Se este e-mail estiver cadastrado, você receberá as instruções em breve."}


@router.post("/avatar", response={200: UserOut, 400: ErrorOut}, auth=JWTAuth())
def update_avatar(request, avatar: UploadedFile = File(...)):
    """Faz upload de uma nova foto de perfil."""
    allowed = {"image/jpeg", "image/png", "image/webp"}
    if avatar.content_type not in allowed:
        raise HttpError(400, "Formato inválido. Use JPEG, PNG ou WebP.")
    if avatar.size > 5 * 1024 * 1024:
        raise HttpError(400, "Imagem muito grande. Máximo 5 MB.")
    user = request.auth
    if user.avatar:
        user.avatar.delete(save=False)
    user.avatar.save(avatar.name, avatar, save=True)
    return 200, UserOut.from_user(user)
