from rest_framework import serializers
from apps.home.models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData, RNAExpresion, SurvivalAnalysisResults

class StudyCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCase
        fields = '__all__'

class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'

class DiffExprAnalysisDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiffExprAnalysisData
        fields = '__all__'

class EnrichDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrichData
        fields = '__all__'

class RNAExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RNAExpresion
        fields = '__all__'

class SurvivalAnalysisResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurvivalAnalysisResults
        fields = '__all__'

