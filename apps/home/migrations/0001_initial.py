# Generated by Django 4.2.3 on 2023-08-20 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudyCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('project', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='metaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('case_id', models.CharField(max_length=200)),
                ('file_name', models.CharField(max_length=200)),
                ('file_id', models.CharField(max_length=36)),
                ('patient', models.CharField(max_length=50)),
                ('sample', models.CharField(max_length=50)),
                ('submitter_id', models.CharField(max_length=50)),
                ('entity_submitter_id', models.CharField(max_length=50)),
                ('sample_type', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('age_at_diagnosis', models.PositiveIntegerField(null=True)),
                ('tumor_stage', models.CharField(max_length=10, null=True)),
                ('tumor_grade', models.CharField(max_length=10, null=True)),
                ('days_to_death', models.PositiveIntegerField(null=True)),
                ('days_to_last_follow_up', models.PositiveIntegerField(null=True)),
                ('vital_status', models.CharField(max_length=20)),
                ('project_id', models.CharField(max_length=50)),
                ('studyCase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studycase')),
            ],
        ),
        migrations.CreateModel(
            name='enrichData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('terms', models.CharField(max_length=255)),
                ('counts', models.IntegerField()),
                ('gene_ratio', models.CharField(max_length=255)),
                ('bg_ratio', models.CharField(max_length=255)),
                ('p_value', models.FloatField()),
                ('fdr', models.FloatField()),
                ('fold_enrichment', models.FloatField()),
                ('gene_ids', models.TextField()),
                ('gene_symbols', models.TextField()),
                ('category', models.CharField(max_length=255)),
                ('studyCase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studycase')),
            ],
        ),
        migrations.CreateModel(
            name='diffExprAnalysisData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('symbol', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=50)),
                ('baseMean', models.FloatField()),
                ('logFC', models.FloatField()),
                ('lfcSE', models.FloatField()),
                ('stat', models.FloatField()),
                ('PValue', models.FloatField()),
                ('FDR', models.FloatField()),
                ('studyCase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studycase')),
            ],
        ),
    ]