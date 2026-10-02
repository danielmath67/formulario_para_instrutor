from django import forms
from .models import Relatorio


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['nome', 'data_nascimento', 'telefone', 'email', 'renach', 'categoria',
                  'instrutor', 'autoescola', 'data_aula', 'horario_inicio', 'horario_fim',
                  'aulas_previstas', 'aulas_realizadas', 'situacao', 'conteudo',
                  'desempenho', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_aula': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'horario_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'horario_fim': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'telefone': forms.TextInput(attrs={'type': 'tel'}),
            'conteudo': forms.Textarea(attrs={'rows': 4}),
            'desempenho': forms.Textarea(attrs={'rows': 4}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nome in ('data_nascimento', 'data_aula'):
            self.fields[nome].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
