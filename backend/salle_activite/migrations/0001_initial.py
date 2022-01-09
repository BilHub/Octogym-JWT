# Generated by Django 2.2.7 on 2022-01-07 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name="nom de la salle d'activité")),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name="nom d'activité")),
                ('color', models.CharField(blank=True, default='#233774', max_length=50, null=True)),
                ('salle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actvities', to='salle_activite.Salle')),
            ],
        ),
    ]
