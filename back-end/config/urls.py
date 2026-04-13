from django.contrib import admin
from django.urls import path
from apps.users.api import router as users_router
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaExtraAPI(
    title="Wolliz API",
    version="1.0.0",
    description="API do marketplace imobiliário Wolliz",
    urls_namespace="api",
)

api.add_router("/auth", users_router, tags=["Auth"])
api.register_controllers(NinjaJWTDefaultController)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
