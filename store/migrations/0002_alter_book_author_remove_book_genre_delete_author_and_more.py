# Generated by Django 5.0.6 on 2024-10-23 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100),
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(default='story', max_length=50),
        ),
    ]