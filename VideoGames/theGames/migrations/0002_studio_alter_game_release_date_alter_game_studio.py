# Generated by Django 4.2.5 on 2023-10-10 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theGames', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('country', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='release_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='studio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theGames.studio'),
        ),
    ]
