from ninja import Schema
from pydantic import EmailStr, field_validator
import re


# ─── Input Schemas ────────────────────────────────────────────────────────────

class RegisterIn(Schema):
    email: EmailStr
    name: str
    password: str
    phone: str = ""

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O nome não pode ser vazio.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        return v

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: str) -> str:
        if v and not re.match(r"^\+?[\d\s\-\(\)]{8,22}$", v):
            raise ValueError("Formato de telefone inválido. Ex: +55 48 98416-1284")
        return v


class ProfileUpdateIn(Schema):
    name: str | None = None
    phone: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("O nome não pode ser vazio.")
        return v.strip() if v else v

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: str | None) -> str | None:
        if v and not re.match(r"^\+?[\d\s\-\(\)]{8,22}$", v):
            raise ValueError("Formato de telefone inválido. Ex: +55 48 98416-1284")
        return v


class LoginIn(Schema):
    email: EmailStr
    password: str


class ForgotPasswordIn(Schema):
    email: EmailStr


class ChangePasswordIn(Schema):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("A nova senha deve ter pelo menos 8 caracteres.")
        return v


# ─── Output Schemas ───────────────────────────────────────────────────────────

class UserOut(Schema):
    id: str
    email: str
    name: str
    phone: str
    avatar_url: str | None
    created_at: str

    @staticmethod
    def from_user(user) -> "UserOut":
        avatar_url = None
        if user.avatar:
            try:
                avatar_url = user.avatar.url
            except Exception:
                pass
        return UserOut(
            id=str(user.id),
            email=user.email,
            name=user.name,
            phone=user.phone,
            avatar_url=avatar_url,
            created_at=user.created_at.isoformat(),
        )


class TokenPairOut(Schema):
    access: str
    refresh: str


class AccessTokenOut(Schema):
    access: str


class MessageOut(Schema):
    message: str


class ErrorOut(Schema):
    detail: str
