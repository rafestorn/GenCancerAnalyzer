from django.shortcuts import render, redirect
from django import template
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from apps.home.RFunctions import downloadRNA, analysisRNA
from apps.home.apiGDC import statusGDCApi
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px

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

    metamatrix = analysisRNA(project_id, data_type)
    print(metamatrix)
    
    return redirect('home')


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

    # Agrupar el DataFrame por 'group' y 'regulation', y contar los valores en cada categoría
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

def results(request):
    volcanoPlot = volcanoPlotDE()
    barPlot = barplotDE()
    corrPlot = corrPlotDE()

    return render(request, 'home/results.html', {'volcano_plot': volcanoPlot, 'bar_plot': barPlot, 'corr_plot': corrPlot})
    