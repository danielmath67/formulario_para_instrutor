import io
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Relatorio
from .pdf import gerar_pdf

DADOS = {
    'nome': 'Ana Souza', 'email': 'ana@example.com', 'telefone': '(89) 99999-1234',
    'data_nascimento': '2000-05-12', 'renach': '123456789', 'categoria': 'B',
    'instrutor': 'Eduardo', 'autoescola': 'CFC Exemplo', 'data_aula': '2026-10-01',
    'horario_inicio': '08:00', 'horario_fim': '08:50', 'aulas_previstas': '20',
    'aulas_realizadas': '5', 'situacao': 'andamento',
    'conteudo': 'Baliza e controle da embreagem.',
    'desempenho': 'Melhorou nas curvas.', 'observacoes': 'Rever <b>baliza</b> & marcha.\nPróxima aula.'
}

class FluxoFormularioTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(username='instrutor', password='Senha-de-teste-123')
        self.client.force_login(self.usuario)

    def enviar(self, alteracoes=None):
        return self.client.post(reverse('index'), {**DADOS, **(alteracoes or {})})

    def test_formulario_simples(self):
        resposta = self.client.get(reverse('index'))
        self.assertContains(resposta, 'csrfmiddlewaretoken')
        self.assertContains(resposta, 'name="categoria"')
        self.assertNotContains(resposta, 'bootstrap')
        self.assertNotContains(resposta, 'name="assunto"')

    def test_fluxo_completo_e_escape_html(self):
        resposta = self.enviar()
        ficha = Relatorio.objects.get()
        self.assertRedirects(resposta, reverse('relatorio', args=[ficha.pk]))
        pagina = self.client.get(resposta.url)
        self.assertContains(pagina, 'Ana Souza')
        self.assertContains(pagina, '&lt;b&gt;baliza&lt;/b&gt;')
        pdf = self.client.get(reverse('relatorio_pdf', args=[ficha.pk]))
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertIn('attachment', pdf['Content-Disposition'])
        conteudo = b''.join(pdf.streaming_content)
        self.assertTrue(conteudo.startswith(b'%PDF'))
        self.assertIn('no-store', pdf['Cache-Control'])

    def test_campos_opcionais(self):
        dados = {k: '' for k in ('email', 'telefone', 'data_nascimento', 'renach', 'autoescola', 'aulas_previstas', 'desempenho', 'observacoes')}
        self.assertEqual(self.enviar(dados).status_code, 302)

    def test_dados_invalidos_nao_salvam(self):
        for alteracoes in ({'nome': ''}, {'categoria': 'X'}, {'horario_fim': '07:30'},
                           {'aulas_realizadas': '21'}, {'aulas_realizadas': '-1'},
                           {'data_nascimento': '2999-01-01'}, {'data_aula': 'inválida'}):
            with self.subTest(alteracoes=alteracoes):
                resposta = self.enviar(alteracoes)
                self.assertEqual(resposta.status_code, 200)
                self.assertContains(resposta, 'errorlist')
        self.assertEqual(Relatorio.objects.count(), 0)

    def test_cadastro_persiste_em_outra_sessao(self):
        self.enviar()
        ficha = Relatorio.objects.get()
        outro = Client()
        outro.force_login(self.usuario)
        for nome in ('relatorio', 'relatorio_pdf'):
            self.assertEqual(outro.get(reverse(nome, args=[ficha.pk])).status_code, 200)

    def test_csrf(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post(reverse('index'), DADOS).status_code, 403)

    def test_pdf_texto_longo(self):
        self.enviar({'observacoes': ('Observação detalhada sobre direção e atenção.\n' * 80)[:4000]})
        self.assertTrue(gerar_pdf(Relatorio.objects.get()).startswith(b'%PDF'))

    def test_lista_vazia(self):
        resposta = self.client.get(reverse('alunos'))
        self.assertContains(resposta, 'Nenhum aluno cadastrado ainda.')
        self.assertContains(resposta, reverse('index'))

    def test_lista_alfabetica_com_links_e_pdf_por_aluno(self):
        for nome in ('Zeca', 'bruno', 'Álvaro', 'Ana'):
            self.enviar({'nome': nome})
        outro = Client()
        outro.force_login(self.usuario)
        resposta = outro.get(reverse('alunos'))
        self.assertEqual([a.nome for a in resposta.context['alunos']], ['Álvaro', 'Ana', 'bruno', 'Zeca'])
        for aluno in Relatorio.objects.all():
            self.assertContains(resposta, reverse('relatorio', args=[aluno.pk]))
            self.assertContains(resposta, reverse('relatorio_pdf', args=[aluno.pk]))
            pagina = outro.get(reverse('relatorio', args=[aluno.pk]))
            self.assertContains(pagina, aluno.nome)
            self.assertContains(pagina, reverse('alunos'))
            self.assertContains(pagina, reverse('index'))

    def test_nomes_iguais_possuem_fichas_distintas(self):
        self.enviar()
        self.enviar({'data_aula': '2026-10-02'})
        resposta = self.client.get(reverse('alunos'))
        self.assertEqual(len(resposta.context['alunos']), 2)
        self.assertContains(resposta, '01/10/2026')
        self.assertContains(resposta, '02/10/2026')

    def test_ficha_inexistente(self):
        import uuid
        for nome in ('relatorio', 'relatorio_pdf'):
            self.assertEqual(self.client.get(reverse(nome, args=[uuid.uuid4()])).status_code, 404)

    def test_links_antigos_continuam_funcionando(self):
        self.enviar()
        ficha = Relatorio.objects.get()
        self.assertEqual(self.client.get(f'/relatorio/{ficha.pk}/').status_code, 200)
        self.assertEqual(self.client.get(f'/relatorio/{ficha.pk}/pdf/').status_code, 200)


class LoginInstrutorTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(username='instrutor', password='Senha-de-teste-123')
        self.client.force_login(self.usuario)
        self.client.post(reverse('index'), DADOS)
        self.ficha = Relatorio.objects.get()
        self.client.logout()

    def test_visitante_nao_acessa_paginas_e_pdf(self):
        urls = [reverse('index'), reverse('alunos'),
                reverse('relatorio', args=[self.ficha.pk]),
                reverse('relatorio_pdf', args=[self.ficha.pk]),
                f'/relatorio/{self.ficha.pk}/', f'/relatorio/{self.ficha.pk}/pdf/']
        for url in urls:
            with self.subTest(url=url):
                resposta = self.client.get(url)
                self.assertEqual(resposta.status_code, 302)
                self.assertTrue(resposta.url.startswith(reverse('login') + '?next='))
        resposta = self.client.post(reverse('index'), DADOS)
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Relatorio.objects.count(), 1)

    def test_login_valido(self):
        resposta = self.client.post(reverse('login'), {'username': 'instrutor', 'password': 'Senha-de-teste-123'})
        self.assertRedirects(resposta, reverse('alunos'))
        self.assertContains(self.client.get(reverse('alunos')), 'Ana Souza')

    def test_login_invalido(self):
        resposta = self.client.post(reverse('login'), {'username': 'instrutor', 'password': 'errada'})
        self.assertContains(resposta, 'Usuário ou senha incorretos.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_preserva_destino(self):
        destino = reverse('relatorio', args=[self.ficha.pk])
        resposta = self.client.post(reverse('login'), {'username': 'instrutor', 'password': 'Senha-de-teste-123', 'next': destino})
        self.assertRedirects(resposta, destino)

    def test_login_recusa_redirecionamento_externo(self):
        resposta = self.client.post(reverse('login'), {'username': 'instrutor', 'password': 'Senha-de-teste-123', 'next': 'https://example.org/'})
        self.assertRedirects(resposta, reverse('alunos'))

    def test_sair(self):
        self.client.force_login(self.usuario)
        pagina = self.client.get(reverse('alunos'))
        self.assertContains(pagina, reverse('logout'))
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('logout')), reverse('login'))
        self.assertEqual(self.client.get(reverse('alunos')).status_code, 302)

    def test_login_tem_csrf(self):
        self.assertContains(self.client.get(reverse('login')), 'csrfmiddlewaretoken')
        self.assertEqual(Client(enforce_csrf_checks=True).post(reverse('login'), {'username': 'instrutor', 'password': 'Senha-de-teste-123'}).status_code, 403)
