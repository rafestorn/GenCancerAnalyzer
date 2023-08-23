from rest_framework import serializers
from apps.home.models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData

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
        exclude = ['gene_ids','gene_symbols']
