# Generated by Django 4.2.3 on 2023-08-20 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studycase',
            name='data_type',
            field=models.CharField(default='hola', max_length=200),
            preserve_default=False,
        ),
    ]
