from rest_framework import viewsets
from ..models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData, RNAExpresion, SurvivalAnalysisResults
from .serializers import StudyCaseSerializer, MetaDataSerializer, DiffExprAnalysisDataSerializer, EnrichDataSerializer, RNAExpressionSerializer, SurvivalAnalysisResultsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404

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
            queryset = queryset.filter(id=sc)
        
        if project:
            queryset = queryset.filter(project=project)
        
        if data_type:
            queryset = queryset.filter(data_type=data_type)

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

class StudyCaseByID(APIView):
    @swagger_auto_schema(
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, id):
        try:
            queryset = StudyCase.objects.get(id=id)
        except StudyCase.DoesNotExist:
            raise Http404("Study case with ID: " + str(id) +" not found")
        serializer = StudyCaseSerializer(queryset)
        return Response(serializer.data)

class MetadataCaseViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ],
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, studyCase_id):
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')

        if page is None:
            page = 1

        
        queryset = MetaData.objects.filter(studyCase__id=studyCase_id)
        
        if not queryset.exists():  # Verifica si no hay resultados
            raise Http404("No se encontraron resultados para esta consulta.")

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
            openapi.Parameter('orderBy', openapi.IN_QUERY, description="Sort by field", type=openapi.TYPE_STRING, enum=['baseMean', '-baseMean','logFC', '-logFC', 'lfcSE', '-lfcSE', 'stat', '-stat', 'PValue', '-PValue', 'FDR', '-FDR']),
            openapi.Parameter('group', openapi.IN_QUERY, description="Filter by group", type=openapi.TYPE_STRING),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ],
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, studyCase_id):
        orderBy = request.query_params.get('orderBy')
        group = request.query_params.get('group')
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')

        if page is None:
            page = 1

        queryset = DiffExprAnalysisData.objects.filter(studyCase__id=studyCase_id)
        
        if group:
            queryset = queryset.filter(group=group)

        if orderBy:
            queryset = queryset.order_by(orderBy)

        if not queryset.exists():
            raise Http404("No se encontraron resultados para esta consulta.")

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
            openapi.Parameter('category', openapi.IN_QUERY, description="Category filter", type=openapi.TYPE_STRING),
            openapi.Parameter('orderBy', openapi.IN_QUERY, description="Sort by field", type=openapi.TYPE_STRING, enum=['counts', '-counts', 'pvalue', '-pvalue', 'fdr', '-fdr', 'fold_enrichment', '-fold_enrichment']),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ],
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, studyCase_id):
        category = request.query_params.get('category')
        orderBy = request.query_params.get('orderBy')
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')

        if page is None:
            page = 1
        
        queryset = EnrichData.objects.filter(studyCase__id=studyCase_id)
        
        if category:
            queryset = queryset.filter(category=category)

        if orderBy:
            queryset = queryset.order_by(orderBy)

        if not queryset.exists():  # Verifica si no hay resultados
            raise Http404("No se encontraron resultados para esta consulta.")

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
    
class RNAexprCaseViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('genes_ids', openapi.IN_QUERY, description="Comma-separated gene IDs to filter", type=openapi.TYPE_STRING),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ],
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, studyCase_id):
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')
        genes_ids = request.query_params.get('genes_ids')

        if page is None:
            page = 1

        queryset = RNAExpresion.objects.filter(studyCase__id=studyCase_id)
        
        if genes_ids:
            gene_ids_list = genes_ids.split(',')
            queryset = queryset.filter(gene_id__in=gene_ids_list)

        if not queryset.exists():  # Verifica si no hay resultados
            raise Http404("No se encontraron resultados para esta consulta.")


        pag_queryset = paginate_queryset(queryset, page, max_items)

        serializer = RNAExpressionSerializer(pag_queryset, many=True)
        
        response = {
            "page": int(page) if page is not None else 1,
            "items_in_page": pag_queryset.count(),
            "total_items": queryset.count(),
            "total_pages": queryset.count()//int(max_items) + 1 if max_items is not None else 1,
            "next_page": request.build_absolute_uri() + f"&page={int(page)+1}" if max_items is not None and int(page)*int(max_items) < queryset.count() else None,
            "results": serializer.data,
        }
        return Response(response)

class SurvivalCaseViewSet(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('orderBy', openapi.IN_QUERY, description="Sort by field", type=openapi.TYPE_STRING, enum=['hr', '-hr','lower95', '-lower95', 'upper95', '-upper95', 'p_value', '-p_value']),
            openapi.Parameter('maxItems', openapi.IN_QUERY, description="Max number of items in a query", type=openapi.TYPE_INTEGER, minimum=1),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER, minimum=1),
        ],
        responses={
            200: 'OK',
            404: 'Not Found',
        }
    )
    def get(self, request, studyCase_id):
        max_items = request.query_params.get('maxItems')
        page = request.query_params.get('page')
        orderBy = request.query_params.get('orderBy')

        if page is None:
            page = 1

        queryset = SurvivalAnalysisResults.objects.filter(studyCase__id=studyCase_id)

        if orderBy:
            queryset = queryset.order_by(orderBy)
        
        if not queryset.exists():
            raise Http404("No se encontraron resultados para esta consulta.")
        
        pag_queryset = paginate_queryset(queryset, page, max_items)

        serializer = SurvivalAnalysisResultsSerializer(pag_queryset, many=True)
        
        response = {
            "page": int(page) if page is not None else 1,
            "items_in_page": pag_queryset.count(),
            "total_items": queryset.count(),
            "total_pages": queryset.count()//int(max_items) + 1 if max_items is not None else 1,
            "next_page": request.build_absolute_uri() + f"&page={int(page)+1}" if max_items is not None and int(page)*int(max_items) < queryset.count() else None,
            "results": serializer.data,
        }
        return Response(response)
        