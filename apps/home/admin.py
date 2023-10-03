from django.contrib import admin
from .models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData, RNAExpresion, SurvivalAnalysisResults
# Register your models here.
admin.site.register(StudyCase)
admin.site.register(MetaData)
admin.site.register(DiffExprAnalysisData)
admin.site.register(EnrichData)
admin.site.register(RNAExpresion)
admin.site.register(SurvivalAnalysisResults)

