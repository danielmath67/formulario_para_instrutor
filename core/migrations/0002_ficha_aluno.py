

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relatorio',
            name='assunto',
        ),
        migrations.RemoveField(
            model_name='relatorio',
            name='mensagem',
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='nome',
            field=models.CharField(max_length=120, verbose_name='Nome completo do aluno'),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='E-mail do aluno'),
        ),
        migrations.AddField(
            model_name='relatorio',
            name='telefone',
            field=models.CharField(blank=True, default='', max_length=25, verbose_name='Telefone do aluno'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True, verbose_name='Data de nascimento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='renach',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='Número do RENACH'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='categoria',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('ACC', 'ACC')], default='', max_length=3, verbose_name='Categoria da habilitação'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='instrutor',
            field=models.CharField(default='', max_length=120, verbose_name='Nome do instrutor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='autoescola',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Autoescola / CFC'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='data_aula',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Data da aula'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='horario_inicio',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='Horário de início'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='horario_fim',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='Horário de término'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='aulas_previstas',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Quantidade de aulas previstas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='aulas_realizadas',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Quantidade de aulas realizadas'),
        ),
        migrations.AddField(
            model_name='relatorio',
            name='situacao',
            field=models.CharField(choices=[('andamento', 'Em andamento'), ('concluido', 'Concluído')], default='andamento', max_length=15, verbose_name='Situação do aluno'),
        ),
        migrations.AddField(
            model_name='relatorio',
            name='conteudo',
            field=models.TextField(default='', max_length=4000, verbose_name='Conteúdo / atividades da aula'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='desempenho',
            field=models.TextField(blank=True, default='', max_length=4000, verbose_name='Desempenho e dificuldades do aluno'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatorio',
            name='observacoes',
            field=models.TextField(blank=True, default='', max_length=4000, verbose_name='Observações do instrutor'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='relatorio',
            options={'ordering': ['-criado_em'], 'verbose_name': 'Ficha do aluno', 'verbose_name_plural': 'Fichas dos alunos'},
        ),
    ]
