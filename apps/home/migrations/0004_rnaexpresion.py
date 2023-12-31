# Generated by Django 4.2.3 on 2023-08-30 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_diffexpranalysisdata_gene_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='RNAExpresion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_id', models.CharField(max_length=50)),
                ('data', models.JSONField()),
                ('studyCase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studycase')),
            ],
            options={
                'db_table': 'rna_expression',
            },
        ),
    ]
