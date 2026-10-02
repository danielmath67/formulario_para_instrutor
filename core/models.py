import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.formats import localize


class Relatorio(models.Model):
    CATEGORIAS = [(v, v) for v in ('A', 'B', 'AB', 'C', 'D', 'E', 'ACC')]
    SITUACOES = [('andamento', 'Em andamento'), ('concluido', 'Concluído')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    nome = models.CharField('Nome completo do aluno', max_length=120)
    email = models.EmailField('E-mail do aluno', blank=True)
    telefone = models.CharField('Telefone do aluno', max_length=25, blank=True)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    renach = models.CharField('Número do RENACH', max_length=30, blank=True)
    categoria = models.CharField('Categoria da habilitação', max_length=3, choices=CATEGORIAS)
    instrutor = models.CharField('Nome do instrutor', max_length=120)
    autoescola = models.CharField('Autoescola / CFC', max_length=150, blank=True)
    data_aula = models.DateField('Data da aula')
    horario_inicio = models.TimeField('Horário de início')
    horario_fim = models.TimeField('Horário de término')
    aulas_previstas = models.PositiveSmallIntegerField('Quantidade de aulas previstas', null=True, blank=True)
    aulas_realizadas = models.PositiveSmallIntegerField('Quantidade de aulas realizadas', default=0)
    situacao = models.CharField('Situação do aluno', max_length=15, choices=SITUACOES, default='andamento')
    conteudo = models.TextField('Conteúdo / atividades da aula', max_length=4000)
    desempenho = models.TextField('Desempenho e dificuldades do aluno', max_length=4000, blank=True)
    observacoes = models.TextField('Observações do instrutor', max_length=4000, blank=True)

    class Meta:
        verbose_name = 'Ficha do aluno'
        verbose_name_plural = 'Fichas dos alunos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        erros = {}
        if self.data_nascimento and self.data_nascimento > timezone.localdate():
            erros['data_nascimento'] = 'A data de nascimento não pode estar no futuro.'
        if self.horario_inicio and self.horario_fim and self.horario_fim <= self.horario_inicio:
            erros['horario_fim'] = 'O término deve ser posterior ao início, no mesmo dia.'
        if self.aulas_previstas is not None and self.aulas_realizadas is not None and self.aulas_realizadas > self.aulas_previstas:
            erros['aulas_realizadas'] = 'A quantidade realizada não pode superar a prevista.'
        if erros:
            raise ValidationError(erros)

    def campos(self):
        itens = []
        for campo in self._meta.fields:
            if campo.name in ('id', 'criado_em'):
                continue
            valor = getattr(self, f'get_{campo.name}_display')() if campo.choices else getattr(self, campo.name)
            if valor in (None, ''):
                valor = 'Não informado'
            elif isinstance(campo, models.DateField):
                valor = valor.strftime('%d/%m/%Y')
            elif isinstance(campo, models.TimeField):
                valor = valor.strftime('%H:%M')
            else:
                valor = localize(valor)
            itens.append((str(campo.verbose_name), str(valor)))
        return itens
