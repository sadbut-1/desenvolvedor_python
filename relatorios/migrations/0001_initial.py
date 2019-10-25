# Generated by Django 2.2.6 on 2019-10-23 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_guia_consulta', models.IntegerField()),
                ('cod_medico', models.IntegerField()),
                ('nome_medico', models.CharField(max_length=150)),
                ('data_consulta', models.DateField()),
                ('valor_consulta', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Exame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_exame', models.IntegerField()),
                ('valor_exame', models.FloatField()),
                ('num_guia_consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relatorios.Consulta')),
            ],
        ),
    ]