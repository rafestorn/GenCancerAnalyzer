from django.urls import path, re_path, include
from apps.home import views
from apps.home.api import queries
from .api.swagger import schema_view

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('create', views.download, name='download'),
    path('analysis', views.index, name='analysis'),
    path('results/<int:id>', views.analysisResults, name='results'),
    
    #API
    path('api/metadata', queries.MetadataCaseViewSet.as_view() ),
    path('api/differentialExpression', queries.DiffExprAnalysisCaseViewSet.as_view() ),
    path('api/enrichAnalysis', queries.EnrichAnalysisCaseViewSet.as_view() ),
    path('api/studyCase', queries.StudyCaseViewSet.as_view() ),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]