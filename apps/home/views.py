from django.shortcuts import render, redirect
from django import template
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import StudyCase
from .forms import AnalyzeForm
from .tasks import analisis
from .apiGDC import statusGDCApi

def index(request):
    if request.method == 'POST':
        form = AnalyzeForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data['projects']
            data_type = form.cleaned_data['data_type']
            if StudyCase.objects.filter(project=project_id, data_type=data_type).exists():
                sc = StudyCase.objects.get(project=project_id, data_type=data_type)
                if sc.state == "DONE":
                    return redirect('metadata', id = StudyCase.objects.get(project=project_id, data_type=data_type).id)
                else:
                    return redirect('/analyzedProjects?project='+project_id+'&data_type='+data_type)
            else:
                try:
                    if statusGDCApi():
                        sc = StudyCase(project=project_id, data_type=data_type)
                        sc.save()
                        tarea = analisis.delay(project_id, data_type, sc.id)
                        return redirect('/analyzedProjects?project='+project_id+'&data_type='+data_type)
                    else:
                        html_template = loader.get_template('home/page-500.html')
                        HttpResponse(html_template.render({}, request))
                except:
                    html_template = loader.get_template('home/page-500.html')
                    return HttpResponse(html_template.render({}, request))
            
    else:
        context = {'form': AnalyzeForm()}
        html_template = loader.get_template("home/index.html")
        return HttpResponse(html_template.render(context, request))

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

def metaData(request, id):
    return render(request, 'home/results-metadata.html', {'id': id})

def diffExpr(request, id):
    return render(request, 'home/results-difexpr.html', {'id': id})

def enrichment(request, id):
    return render(request, 'home/results-enrich.html', {'id': id})

def survivalAnalysis(request, id):
    return render(request, 'home/results-survival.html', {'id': id})

def analyzedProjects(request):

    project = request.GET.get('project')
    data_type = request.GET.get('data_type')

    # Filtra los objetos de tu modelo en función de los parámetros
    queryset = StudyCase.objects.all()

    if project:
        queryset = queryset.filter(project=project)
    else:
        project = ""

    if data_type:
        queryset = queryset.filter(data_type=data_type)
    else:
        data_type = ""
    

    context = {
        'data': queryset,
        'projects': queryset.values_list('project', flat=True).distinct(),
        'numAnalized':queryset.filter(state="DONE").count(),
        'project': project,
        'data_type': data_type
    }

    return render(request, 'home/analyzed_projects.html', context)

def webinfo(request):
    return render(request, 'home/web-info.html')

def aboutApi(request):
    return render(request, 'home/api-info.html')