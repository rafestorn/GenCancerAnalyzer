from rest_framework import viewsets
from ..models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData
from .serializers import StudyCaseSerializer, MetaDataSerializer, DiffExprAnalysisDataSerializer, EnrichDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

class StudyCaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudyCase.objects.all()
    serializer_class = StudyCaseSerializer

class MetadataCaseViewSet(APIView):
    def get(self, request):
        sc = request.query_params.get('studyCase')

        queryset = MetaData.objects.all()

        if sc:
             queryset = queryset.filter(studyCase__id__icontains=sc)

        serializer = MetaDataSerializer(queryset, many=True)
        return Response(serializer.data)

class DiffExprAnalysisCaseViewSet(APIView):
    def get(self, request):
        sc = request.query_params.get('studyCase')
        group = request.query_params.get('group')

        queryset = DiffExprAnalysisData.objects.all()

        if sc:
             queryset = queryset.filter(studyCase__id__icontains=sc)
        
        if group:
            queryset = queryset.filter(group__icontains=group)

        serializer = DiffExprAnalysisDataSerializer(queryset, many=True)
        return Response(serializer.data)
    
class MetadataBySC(generics.ListAPIView):
    serializer_class = MetaDataSerializer

    def get_queryset(self):
        study_case_id = self.kwargs['id']
        return MetaData.objects.filter(studyCase=study_case_id)
    
class DiffExprAnalysisBySC(generics.ListAPIView):
    serializer_class = DiffExprAnalysisDataSerializer

    def get_queryset(self):
        study_case_id = self.kwargs['id']
        return DiffExprAnalysisData.objects.filter(studyCase=study_case_id)

class EnrichAnalysisBySC(generics.ListAPIView):
    serializer_class = EnrichDataSerializer

    def get_queryset(self):
        study_case_id = self.kwargs['id']
        return EnrichData.objects.filter(studyCase=study_case_id)