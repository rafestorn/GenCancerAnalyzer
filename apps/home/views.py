from django.shortcuts import render, redirect
from django import template
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from apps.home.RFunctions import downloadRNA
from apps.home.apiGDC import statusGDCApi


# Create your views here.

def index(request):
    """A view that displays the index page"""
    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(dict(), request))

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
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

