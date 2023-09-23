from celery import shared_task
import os
from .models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData, RNAExpresion, SurvivalAnalysisResults
from .RFunctions import downloadRNA, analysisRNA
from .apiGDC import statusGDCApi
from django.shortcuts import redirect
from django.http import HttpResponse
import csv

@shared_task
def analisis(project_id, data_type, sc_id):
    sc = StudyCase.objects.get(id=sc_id)
    base_dir = 'DATA/' + project_id +'/'+ data_type
    if not os.path.exists(base_dir +'/data'):
        downloadRNA(project_id, data_type)
    if not os.path.exists(base_dir + '/results'):
        analysisRNA(project_id, data_type)

    process_rna_expr_csv('DATA/' + project_id +'/'+ data_type+'/results/RNA_EXPR.csv', sc)
    process_metadata_csv('DATA/' + project_id +'/'+ data_type +'/results/metaMatrix_RNA.csv', sc)
    process_diff_expr_csv('DATA/' + project_id +'/'+ data_type +'/results/DEGALL_CHOL.csv', sc)
    process_survival_csv('DATA/' + project_id +'/'+ data_type +'/results/survival_results.csv', sc)

    if data_type == "RNAseq":
        process_enrich_csv('DATA/' + project_id +'/'+ data_type +'/results/ENRICH_ANALYSIS.csv', sc)

    # actualizar sc state
    sc.state = "DONE"
    sc.save()

    # remove_data(project_id, data_type)

def download(request):
    if statusGDCApi() == False:
        return HttpResponse("El servicio de GDC no está disponible en este momento. Intente más tarde.")
    else:   
        project_id = "TCGA-CHOL"  # Reemplaza con el ID correcto de tu proyecto
        data_type = "RNAseq"    # Reemplaza con el tipo de datos adecuado

        downloadRNA(project_id, data_type)

        return redirect('home')

def process_csv_file(file_path, model_class, field_mapping, additional_fields=None):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            data = {
                field_name: None if row.get(csv_field, "NA") == "NA" else row.get(csv_field, None)
                for field_name, csv_field in field_mapping.items()
            }
            
            if additional_fields:
                data.update(additional_fields)
            
            obj = model_class(**data)
            obj.save()

def process_metadata_csv(file_path, sc_id):
    field_mapping = {
        'case_id': '',
        'file_name': 'file_name',
        'file_id': 'file_id',
        'patient': 'patient',
        'sample': 'sample',
        'submitter_id': 'submitter_id',
        'entity_submitter_id': 'entity_submitter_id',
        'sample_type': 'sample_type',
        'gender': 'gender',
        'age_at_diagnosis': 'age_at_diagnosis',
        'tumor_stage': 'tumor_stage',
        'tumor_grade': 'tumor_grade',
        'days_to_death': 'days_to_death',
        'days_to_last_follow_up': 'days_to_last_follow_up',
        'vital_status': 'vital_status',
        'project_id': 'project_id',
    }
    additional_fields = {'studyCase': sc_id}
    process_csv_file(file_path, MetaData, field_mapping, additional_fields)

def process_diff_expr_csv(file_path, sc):
    field_mapping = {
        'gene_id': '',
        'symbol': 'symbol',
        'group': 'group',
        'baseMean': 'baseMean',
        'logFC': 'logFC',
        'lfcSE': 'lfcSE',
        'stat': 'stat',
        'PValue': 'PValue',
        'FDR': 'FDR',
    }
    additional_fields = {'studyCase': sc}
    process_csv_file(file_path, DiffExprAnalysisData, field_mapping, additional_fields)

def process_enrich_csv(file_path, sc):
    field_mapping= {
        "terms": "Terms",
        "counts": "Counts",
        "gene_ratio": "GeneRatio",
        "bg_ratio": "BgRatio",
        "p_value": "pValue",
        "fdr": "FDR",
        "fold_enrichment": "foldEnrichment",
        "gene_ids": "geneID",
        "gene_symbols": "geneSymbol",
        "category": "Category"
    }
    additional_fields = {'studyCase': sc}
    process_csv_file(file_path, EnrichData, field_mapping, additional_fields)

def process_survival_csv(file_path, sc):
    field_mapping = {
        'gene_id': '',
        'symbol': 'symbol',
        'hr': 'HR',
        'lower95': 'lower95',
        'upper95': 'upper95',
        'p_value': 'pValue'
    }
    additional_fields = {'studyCase': sc}
    process_csv_file(file_path, SurvivalAnalysisResults, field_mapping, additional_fields)

def process_rna_expr_csv(file_path, sc):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {}
            gene_id = row[""]
            for key, value in row.items():
                if key != "":
                    data[key] = float(value)
            RNAExpresion(studyCase=sc, gene_id=gene_id, data=data).save()

def remove_data(project_id, datatype):
    carpeta_descarga = 'DATA/' + project_id +'/'+ datatype +'/data'
    try:
        os.rmdir(carpeta_descarga)  # Intenta eliminar la carpeta
    except OSError as e:
        # Si no se puede eliminar como carpeta, intenta eliminar como archivo
        if os.path.isdir(carpeta_descarga):
            for archivo in os.listdir(carpeta_descarga):
                archivo_completo = os.path.join(carpeta_descarga, archivo)
                try:
                    os.remove(archivo_completo)  # Elimina cada archivo
                except Exception as e:
                    print(f"No se pudo eliminar {archivo_completo}: {str(e)}")
            try:
                os.rmdir(carpeta_descarga)  # Intenta eliminar la carpeta nuevamente
            except OSError as e:
                print(f"No se pudo eliminar la carpeta {carpeta_descarga}: {str(e)}")
        else:
            print(f"No se pudo eliminar la carpeta {carpeta_descarga}: {str(e)}")
