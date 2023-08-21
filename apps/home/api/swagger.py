from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Tu API",
      default_version='v1',
      description="Descripción de tu API",
      terms_of_service="https://www.tusitio.com/terms/",
      contact=openapi.Contact(email="contacto@tusitio.com"),
      license=openapi.License(name="Licencia"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)