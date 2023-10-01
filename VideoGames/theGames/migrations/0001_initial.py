# Generated by Django 4.2.5 on 2023-10-01 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('release_date', models.DateTimeField(verbose_name='date published')),
                ('studio', models.CharField(max_length=200)),
            ],
        ),
    ]
