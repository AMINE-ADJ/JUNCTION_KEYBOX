# Generated by Django 4.2.1 on 2023-10-06 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cubaapp', '0008_etudiant_formations'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapiterResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('chapiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubaapp.chapiter')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cubaapp.etudiant')),
            ],
        ),
    ]
