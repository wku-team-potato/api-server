from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Doument",
        default_version="v1",
        description="API Document for the project",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("user_api.urls")),
    path("api/v1/community/", include("community_api.urls")),
    path("api/v1/nutrition/", include("nutrition_api.urls")),
    path("api/v1/swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("api/v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]
