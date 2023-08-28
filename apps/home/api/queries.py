from rest_framework import viewsets
from ..models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData
from .serializers import StudyCaseSerializer, MetaDataSerializer, DiffExprAnalysisDataSerializer, EnrichDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def paginate_queryset(queryset, page, max_items):
    if max_items and int(max_items) > 0:
        start_index = (int(page) - 1) * int(max_items)
        end_index = int(page) * int(max_items)
        pag_queryset = queryset[start_index:end_index]
    else:
        pag_queryset = queryset
    return pag_queryset


class StudyCaseViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="Filter by id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('project', openapi.IN_QUERY, description="Filter by project", type=openapi.TYPE_STRING),
            openapi.Parameter('data_type', openapi.IN_QUERY, description="Filter by data type", type=openapi.TYPE_STRING, enum=['RNAseq', 'miRNAs']),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ]
    )
    def get(self, request):
        sc = request.query_params.get('id')
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')
        project = request.query_params.get('project')
        data_type = request.query_params.get('data_type')

        if page is None:
            page = 1

        queryset = StudyCase.objects.all()

        if sc:
            queryset = queryset.filter(id__icontains=sc)
        
        if project:
            queryset = queryset.filter(project__icontains=project)
        
        if data_type:
            queryset = queryset.filter(data_type__icontains=data_type)

        pag_queryset = paginate_queryset(queryset, page, max_items)

        serializer = StudyCaseSerializer(pag_queryset, many=True)
        response = {
            "page": int(page) if page is not None else 1,
            "items_in_page": pag_queryset.count(),
            "total_items": queryset.count(),
            "total_pages": queryset.count()//int(max_items) + 1 if max_items is not None else 1,
            "next_page": request.build_absolute_uri() + f"&page={int(page)+1}" if max_items is not None and int(page)*int(max_items) < queryset.count() else None,
            "results": serializer.data,
        }
        return Response(response)

class MetadataCaseViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('studyCase', openapi.IN_QUERY, description="Filter by studyCase", type=openapi.TYPE_INTEGER),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ]
    )
    def get(self, request):
        sc = request.query_params.get('studyCase')
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')

        if page is None:
            page = 1

        queryset = MetaData.objects.all()

        if sc:
             queryset = queryset.filter(studyCase__id__icontains=sc)

        pag_queryset = paginate_queryset(queryset, page, max_items)

        serializer = MetaDataSerializer(pag_queryset, many=True)
        response = {
            "page": int(page) if page is not None else 1,
            "items_in_page": pag_queryset.count(),
            "total_items": queryset.count(),
            "total_pages": queryset.count()//int(max_items) + 1 if max_items is not None else 1,
            "next_page": request.build_absolute_uri() + f"&page={int(page)+1}" if max_items is not None and int(page)*int(max_items) < queryset.count() else None,
            "results": serializer.data,
        }
        return Response(response)

class DiffExprAnalysisCaseViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('studyCase', openapi.IN_QUERY, description="Filter by studyCase", type=openapi.TYPE_INTEGER),
            openapi.Parameter('group', openapi.IN_QUERY, description="Filter by group", type=openapi.TYPE_STRING),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ]
    )
    def get(self, request):
        sc = request.query_params.get('studyCase')
        group = request.query_params.get('group')
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')

        if page is None:
            page = 1

        queryset = DiffExprAnalysisData.objects.all()

        if sc:
             queryset = queryset.filter(studyCase__id__icontains=sc)
        
        if group:
            queryset = queryset.filter(group__icontains=group)

        pag_queryset = paginate_queryset(queryset, page, max_items)


        serializer = DiffExprAnalysisDataSerializer(pag_queryset, many=True)
        
        response = {
            "page": int(page) if page is not None else 1,
            "items_in_page": pag_queryset.count(),
            "total_items": queryset.count(),
            "total_pages": queryset.count()//int(max_items) + 1 if max_items is not None else 1,
            "next_page": request.build_absolute_uri() + f"&page={int(page)+1}" if max_items is not None and int(page)*int(max_items) < queryset.count() else None,
            "results": serializer.data,
        }
        return Response(response)

class EnrichAnalysisCaseViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('studyCase', openapi.IN_QUERY, description="Filtro por studyCase", type=openapi.TYPE_INTEGER),
            openapi.Parameter('category', openapi.IN_QUERY, description="Filtro por categoría", type=openapi.TYPE_STRING),
            openapi.Parameter('orderBy', openapi.IN_QUERY, description="Campo por el cual ordenar", type=openapi.TYPE_STRING, enum=['pvalue', '-pvalue', 'fdr', '-fdr', 'fold_enrichment', '-fold_enrichment']),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ]
    )
    def get(self, request):
        sc = request.query_params.get('studyCase')
        category = request.query_params.get('category')
        orderBy = request.query_params.get('orderBy')
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')

        if page is None:
            page = 1

        queryset = EnrichData.objects.all()
        
        if sc:
             queryset = queryset.filter(studyCase__id__icontains=sc)
        
        if category:
            queryset = queryset.filter(category__icontains=category)

        if orderBy:
            queryset = queryset.order_by(orderBy)

        pag_queryset = paginate_queryset(queryset, page, max_items)

        serializer = EnrichDataSerializer(pag_queryset, many=True)
        
        response = {
            "page": int(page) if page is not None else 1,
            "items_in_page": pag_queryset.count(),
            "total_items": queryset.count(),
            "total_pages": queryset.count()//int(max_items) + 1 if max_items is not None else 1,
            "next_page": request.build_absolute_uri() + f"&page={int(page)+1}" if max_items is not None and int(page)*int(max_items) < queryset.count() else None,
            "results": serializer.data,
        }
        return Response(response)