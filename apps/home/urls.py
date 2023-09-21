from django.urls import path, re_path
from apps.home import views
from apps.home.api import queries
from .api.swagger import schema_view

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('analysis', views.index, name='analysis'),
    path('analyzedProjects', views.analyzedProjects, name='analyzedProjects'),
    path('results/<int:id>/metadata', views.metaData, name='metadata'),
    path('results/<int:id>/diffExpr', views.diffExpr, name='diffExpr'),
    path('results/<int:id>/enrichment', views.enrichment, name='enrichment'),
    path('results/<int:id>/survivalAnalysis', views.survivalAnalysis, name='rnaExpr'),
    
    #API
    path('api/studyCase', queries.StudyCaseViewSet.as_view() ),
    path('api/studyCase/<int:id>', queries.StudyCaseByID.as_view() ),
    path('api/studyCase/<int:studyCase_id>/metadata', queries.MetadataCaseViewSet.as_view() ),
    path('api/studyCase/<int:studyCase_id>/differentialExpression', queries.DiffExprAnalysisCaseViewSet.as_view() ),
    path('api/studyCase/<int:studyCase_id>/enrichAnalysis', queries.EnrichAnalysisCaseViewSet.as_view() ),
    path('api/studyCase/<int:studyCase_id>/rnaExpression', queries.RNAexprCaseViewSet.as_view() ),
    path('api/studyCase/<int:studyCase_id>/rnaExpression/<str:gene_id>', queries.RNAexprCaseByGeneViewSet.as_view()),
    path('api/studyCase/<int:studyCase_id>/survivalAnalysis', queries.SurvivalCaseViewSet.as_view() ),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]