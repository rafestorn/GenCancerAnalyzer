from django.shortcuts import render, redirect
from django import template
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from apps.home.RFunctions import downloadRNA, analysisRNA
from apps.home.apiGDC import statusGDCApi
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
from .models import StudyCase, MetaData, DiffExprAnalysisData, EnrichData
import csv
import os

def index(request):
    """A view that displays the index page"""
    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(dict(), request))

def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def download(request):
    # Llamar a la función de R desde Python
    if statusGDCApi() == False:
        return HttpResponse("El servicio de GDC no está disponible en este momento. Intente más tarde.")
    else:   
        project_id = "TCGA-CHOL"  # Reemplaza con el ID correcto de tu proyecto
        data_type = "RNAseq"    # Reemplaza con el tipo de datos adecuado

        downloadRNA(project_id, data_type)

        return redirect('home')
    
def analysis(request):
    project_id = "TCGA-CHOL"  # Reemplaza con el ID correcto de tu proyecto
    data_type = "RNAseq"    # Reemplaza con el tipo de datos adecuado

    sc = StudyCase(project=project_id, title='Caso de prueba número 2', description='Hola buenas tardes', data_type=data_type)
    sc.save()
    sc_id = sc.id

    if not os.path.exists(project_id + '/metaMatrix_RNA.csv') or not os.path.exists(project_id + '/DEGALL_CHOL.csv') or not os.path.exists(project_id + '/ENRICH_ANALYSIS.csv'):
        analysisRNA(project_id, data_type)

    process_metadata_csv(project_id + '/metaMatrix_RNA.csv', sc)
    process_diff_expr_csv(project_id + '/DEGALL_CHOL.csv', sc)
    process_enrich_csv(project_id + '/ENRICH_ANALYSIS.csv', sc)

    return redirect('home')

def process_csv_file(file_path, model_class, field_mapping, additional_fields=None):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            data = {
                field_name: row[csv_field] if row[csv_field] != "NA" else None
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


def volcanoPlotDE():
    df = pd.read_csv('TCGA-CHOL/DEGALL_CHOL.csv')

    fig = px.scatter(df, x=df['logFC'], y=-1 * np.log10(df['PValue']), title='Volcano Plot')

    threshold_pvalue = 0.05
    threshold_logfc = 2

    significant_genes = df[(df['PValue'] < threshold_pvalue) & (abs(df['logFC']) > threshold_logfc)]

    trace_significant = go.Scatter(
        x=significant_genes['logFC'],
        y=-1 * significant_genes['PValue'],
        text=significant_genes['symbol'],
        mode='markers+text',
        marker=dict(color='red', symbol='x'),
        name='Genes Significativos'
    )
    fig.add_trace(trace_significant) 

    fig.update_layout(
        xaxis_title='Fold Change (logFC)',
        yaxis_title='-log10(FDR corrected - PValue)',
        legend_title='Genes Significativos',
        xaxis=dict(showline=True, showgrid=False),
        yaxis=dict(showline=True, showgrid=False)
    )

    fig.add_shape(dict(type='line', x0=-threshold_logfc, y0=0, x1=-threshold_logfc, y1=30, line=dict(color='gray', dash='dash')))
    fig.add_shape(dict(type='line', x0=threshold_logfc, y0=0, x1=threshold_logfc, y1=30, line=dict(color='gray', dash='dash')))
    fig.add_shape(dict(type='line', x0=-10, y0=-1 * -threshold_pvalue, x1=10, y1=-1 * -threshold_pvalue, line=dict(color='gray', dash='dash')))

    graph = fig.to_html(full_html=False)

    return graph

def barplotDE():
    df = pd.read_csv('TCGA-CHOL/DEGALL_CHOL.csv')

    # Agregar una columna 'regulation' basada en el valor de logFC
    df["regulation"] = df["logFC"].apply(lambda x: "upregulated" if x > 0 else "downregulated")

    grouped_df = df.groupby(['group', 'regulation']).size().reset_index(name='count').sort_values(by=['count'], ascending=False)

    fig = px.bar(grouped_df, x="group", y="count", color="regulation")    

    fig.update_layout(
        xaxis_title="Protein Coding",
        yaxis_title="Nº of diferentially expressed genes"
    )
    graph = fig.to_html(full_html=False)
    
    return graph

def corrPlotDE():
    df = pd.read_csv('TCGA-CHOL/RNA_EXPR.csv')
    df_transposed = df.set_index('Unnamed: 0').T

    genes = ["ENSG00000103569", "ENSG00000118271"]

    fig = px.scatter(df_transposed, x=genes[0], y=genes[1], trendline='ols', title='Correlation Plot')

    graph = fig.to_html(full_html=False)
    
    return graph

def enrichBarData():
    df = pd.read_csv('TCGA-CHOL/ENRICH_ANALYSIS.csv')

    category = 'KEGG'
    filtered_df = df[df['Category'] == category].sort_values(by='FDR', ascending=False)
    return filtered_df.to_dict('records')

def results(request):
    volcanoPlot = volcanoPlotDE()
    barPlot = barplotDE()
    corrPlot = corrPlotDE()
    enrichDict = enrichBarData()
    df = pd.read_csv('TCGA-CHOL/DEGALL_CHOL.csv')
    dict = df.to_dict('records')
    return render(request, 'home/results.html', {'volcano_plot': volcanoPlot, 'bar_plot': barPlot, 'corr_plot': corrPlot, 'data': dict, 'enrichData': enrichDict})