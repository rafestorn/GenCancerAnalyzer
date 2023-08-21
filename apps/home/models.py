from django.db import models

# Create your models here.
class StudyCase(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.CharField(max_length=200)
    data_type = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class MetaData(models.Model):
    studyCase = models.ForeignKey(StudyCase, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    case_id = models.CharField(max_length=200)
    file_name = models.CharField(max_length=200)
    file_id = models.CharField(max_length=36)
    patient = models.CharField(max_length=50)
    sample = models.CharField(max_length=50)
    submitter_id = models.CharField(max_length=50)
    entity_submitter_id = models.CharField(max_length=50)
    sample_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age_at_diagnosis = models.PositiveIntegerField(null=True)
    tumor_stage = models.CharField(max_length=10, null=True)
    tumor_grade = models.CharField(max_length=10, null=True)
    days_to_death = models.PositiveIntegerField(null=True)
    days_to_last_follow_up = models.PositiveIntegerField(null=True)
    vital_status = models.CharField(max_length=20)
    project_id = models.CharField(max_length=50)

    def __str__(self):
        return self.case_id
    
class DiffExprAnalysisData(models.Model):
    studyCase = models.ForeignKey(StudyCase, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    gene_id = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    baseMean = models.FloatField()
    logFC = models.FloatField()
    lfcSE = models.FloatField()
    stat = models.FloatField()
    PValue = models.FloatField()
    FDR = models.FloatField()
    
class EnrichData(models.Model):
    studyCase = models.ForeignKey(StudyCase, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    terms = models.CharField(max_length=255)
    counts = models.IntegerField()
    gene_ratio = models.CharField(max_length=255)
    bg_ratio = models.CharField(max_length=255)
    p_value = models.FloatField()
    fdr = models.FloatField()
    fold_enrichment = models.FloatField()
    gene_ids = models.TextField()
    gene_symbols = models.TextField()
    category = models.CharField(max_length=255)

    def get_gene_ids_list(self):
        return self.gene_ids.split('/')

    def get_gene_symbols_list(self):
        return self.gene_symbols.split('/')