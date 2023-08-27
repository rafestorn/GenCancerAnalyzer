from django import forms
from .apiGDC import getProjectsName

class AnalyzeForm(forms.Form):
    projects_list = getProjectsName()
    projects = forms.ChoiceField(choices=[(p["id"], p["id"] + ": "+ p["name"]) for p in projects_list], widget=forms.Select(attrs={'class': 'form-select'}))
    data_type = forms.ChoiceField(choices=[('RNAseq', 'RNAseq'), ('miRNAs', 'miRNAs')], widget=forms.Select(attrs={'class': 'form-select'}))

