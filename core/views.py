import io
import unicodedata

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView

from .forms import RelatorioForm
from .models import Relatorio
from .pdf import gerar_pdf


def chave_nome(aluno):
    nome = unicodedata.normalize('NFKD', aluno.nome.strip().casefold())
    nome = ''.join(letra for letra in nome if not unicodedata.combining(letra))
    return nome, aluno.nome.casefold(), str(aluno.pk)


@method_decorator(never_cache, name='dispatch')
class IndexView(LoginRequiredMixin, CreateView):
    model = Relatorio
    form_class = RelatorioForm
    template_name = 'index.html'

    def get_success_url(self):
        return reverse('relatorio', kwargs={'pk': self.object.pk})


@method_decorator(never_cache, name='dispatch')
class AlunoListaView(LoginRequiredMixin, View):
    def get(self, request):
        alunos = sorted(Relatorio.objects.all(), key=chave_nome)
        return render(request, 'alunos.html', {'alunos': alunos})


@method_decorator(never_cache, name='dispatch')
class RelatorioDetalheView(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)
        return render(request, 'relatorio.html', {
            'relatorio': relatorio,
            'campos': relatorio.campos(),
        })


@method_decorator(never_cache, name='dispatch')
class RelatorioPdfView(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)
        return FileResponse(
            io.BytesIO(gerar_pdf(relatorio)),
            as_attachment=True,
            filename=f'ficha-{slugify(relatorio.nome) or "aluno"}-{relatorio.pk.hex[:8]}.pdf',
            content_type='application/pdf',
        )
