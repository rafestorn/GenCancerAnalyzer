from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="GenCancerAnalyzerAPI",
      default_version='v1',
      description="Get access to the GenCancerAnalyzer stored data and results.",
      terms_of_service="https://www.tusitio.com/terms/",
      contact=openapi.Contact(email="rafaestrada3@gmail.com"),
      license=openapi.License(name="Licencia"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),

)