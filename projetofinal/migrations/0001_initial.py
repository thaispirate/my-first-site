# Generated by Django 2.0.2 on 2018-03-19 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anamnesia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areaAfetiva', models.CharField(max_length=20, null=True)),
                ('inicio', models.DateTimeField(null=True)),
                ('fim', models.DateTimeField(blank=True, null=True)),
                ('retornos', models.PositiveIntegerField(blank=True, null=True)),
                ('padrao', models.CharField(blank=True, choices=[('adaptativo', 'Adaptativo'), ('reativo', 'Reativo'), ('criativo', 'Criativo')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AreaAfetiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anamnesia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Anamnesia')),
            ],
        ),
        migrations.CreateModel(
            name='Chave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chave', models.CharField(max_length=100)),
                ('padrao', models.CharField(blank=True, choices=[('usada', 'Usada'), ('livre', 'Livre')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(blank=True, max_length=100, null=True)),
                ('sigla', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parente', models.CharField(choices=[('pai', 'Pai'), ('mae', 'Mãe'), ('avoPaterno', 'Avô Paterno'), ('avoPaterna', 'Avó Paterna'), ('avoMaterno', 'Avô Materno'), ('avoMaterna', 'Avó Materna'), ('conjuge', 'Cônjuge')], max_length=10, null=True)),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('nascimento', models.DateField(blank=True, null=True)),
                ('falecimento', models.DateField(blank=True, null=True)),
                ('sexo', models.CharField(blank=True, max_length=10, null=True)),
                ('escolaridade', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrauIndiferenciacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('padrao', models.CharField(choices=[('adaptativo', 'Adaptativo'), ('reativo', 'Reativo'), ('criativo', 'Criativo')], max_length=10, null=True)),
                ('resposta', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrauIndiferenciacaoPaciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anamnesia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Anamnesia')),
            ],
        ),
        migrations.CreateModel(
            name='Interventiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.TextField(null=True)),
                ('anamnesia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Anamnesia')),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municipio', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('nome', models.CharField(max_length=50, null=True)),
                ('nascimento', models.DateField(null=True)),
                ('cpf', models.CharField(max_length=14, null=True)),
                ('telefone', models.CharField(max_length=50, null=True)),
                ('sexo', models.CharField(max_length=10, null=True)),
                ('escolaridade', models.CharField(blank=True, max_length=15, null=True)),
                ('habilitado', models.DateTimeField(blank=True, null=True)),
                ('retornos', models.PositiveIntegerField(blank=True, null=True)),
                ('tempo', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerguntaAreaAfetiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, null=True)),
                ('pergunta', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerguntaInterventiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, null=True)),
                ('pergunta', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerguntaSeletiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, null=True)),
                ('pergunta', models.TextField(null=True)),
                ('tipo', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Psicologo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('nome', models.CharField(max_length=50, null=True)),
                ('telefone', models.CharField(blank=True, max_length=50, null=True)),
                ('celular', models.CharField(blank=True, max_length=50, null=True)),
                ('endereco', models.CharField(max_length=200, null=True)),
                ('numero', models.PositiveIntegerField(blank=True, null=True)),
                ('complemento', models.CharField(max_length=200, null=True)),
                ('bairro', models.CharField(max_length=50, null=True)),
                ('crp', models.CharField(max_length=50, null=True)),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Estado')),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='estado', chained_model_field='estado', null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Municipio')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recomendacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20, null=True)),
                ('intervalo', models.CharField(max_length=10, null=True)),
                ('texto', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Relacionamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parente', models.CharField(choices=[('Pai', 'Pai'), ('Mae', 'Mãe'), ('AvoPaterno', 'Avô Paterno'), ('AvoPaterna', 'Avó Paterna'), ('AvoMaterno', 'Avô Materno'), ('AvoMaterna', 'Avó Materna'), ('Paciente', 'Paciente'), ('Conjuge', 'Cônjuge')], max_length=10, null=True)),
                ('relacao', models.CharField(max_length=20, null=True)),
                ('filhos', models.PositiveIntegerField(null=True)),
                ('filhas', models.PositiveIntegerField(null=True)),
                ('relacaoAntes', models.CharField(max_length=20, null=True)),
                ('filhosAntes', models.PositiveIntegerField(blank=True, null=True)),
                ('filhasAntes', models.PositiveIntegerField(blank=True, null=True)),
                ('filhosDepois', models.PositiveIntegerField(blank=True, null=True)),
                ('filhasDepois', models.PositiveIntegerField(blank=True, null=True)),
                ('anamnesia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Anamnesia')),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='RespostaAreaAfetiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letra', models.CharField(max_length=1, null=True)),
                ('resposta', models.TextField(null=True)),
                ('valor', models.FloatField(null=True)),
                ('nivel1', models.FloatField(blank=True, null=True)),
                ('nivel2', models.FloatField(blank=True, null=True)),
                ('nivel3', models.FloatField(blank=True, null=True)),
                ('nivel4', models.FloatField(blank=True, null=True)),
                ('nivel5', models.FloatField(blank=True, null=True)),
                ('pergunta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.PerguntaAreaAfetiva')),
            ],
        ),
        migrations.CreateModel(
            name='RespostaSeletiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letra', models.CharField(max_length=1, null=True)),
                ('resposta', models.TextField(null=True)),
                ('tipo', models.CharField(blank=True, max_length=10, null=True)),
                ('nivel0', models.FloatField(blank=True, null=True)),
                ('nivel1', models.FloatField(blank=True, null=True)),
                ('nivel2', models.FloatField(blank=True, null=True)),
                ('nivel3', models.FloatField(blank=True, null=True)),
                ('nivel4', models.FloatField(blank=True, null=True)),
                ('nivel5', models.FloatField(blank=True, null=True)),
                ('nivel6', models.FloatField(blank=True, null=True)),
                ('pergunta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.PerguntaSeletiva')),
            ],
        ),
        migrations.CreateModel(
            name='Seletiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anamnesia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Anamnesia')),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Paciente')),
                ('resposta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.RespostaSeletiva')),
            ],
        ),
        migrations.AddField(
            model_name='paciente',
            name='psicologo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Psicologo'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='interventiva',
            name='paciente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Paciente'),
        ),
        migrations.AddField(
            model_name='interventiva',
            name='pergunta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.PerguntaInterventiva'),
        ),
        migrations.AddField(
            model_name='grauindiferenciacaopaciente',
            name='paciente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Paciente'),
        ),
        migrations.AddField(
            model_name='grauindiferenciacaopaciente',
            name='resposta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.GrauIndiferenciacao'),
        ),
        migrations.AddField(
            model_name='familia',
            name='paciente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Paciente'),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='paciente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Paciente'),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='resposta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.RespostaAreaAfetiva'),
        ),
        migrations.AddField(
            model_name='anamnesia',
            name='paciente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetofinal.Paciente'),
        ),
    ]
