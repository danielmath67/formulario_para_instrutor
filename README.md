# Formulário para instrutor de trânsito

Aplicação Django: preenche uma ficha de aluno e aula, salva os dados, mostra um resumo e disponibiliza o PDF para download.
HTML escrito especificamente para o projeto, CSS pequeno e próprio, sem Bootstrap, jQuery, tema pronto ou serviços externos.

## Executar no Linux

Abra um terminal dentro desta pasta (a que contém manage.py):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

No `.env`, defina `DJANGO_DEBUG=1` para execução local e `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`.
Depois:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse http://127.0.0.1:8000/, preencha a ficha, clique em **Salvar e preparar PDF** e depois em **Baixar PDF**.
O ReportLab gera o PDF sem depender de WeasyPrint, Pango ou Cairo.

## Campos

- Aluno: nome, nascimento, telefone, e-mail, RENACH e categoria de habilitação.
- Instrutor/aula: instrutor, autoescola/CFC, data, início e término da aula.
- Acompanhamento: aulas previstas/realizadas, situação, conteúdo da aula, desempenho e observações.

Campos opcionais são sinalizados pela ausência de asterisco. Datas de nascimento futuras,
horários invertidos e quantidade de aulas realizadas maior que a prevista são recusados.
O registro descreve uma aula no mesmo dia; aulas atravessando a meia-noite não são aceitas.

## Referência recebida

O arquivo instrutor.zip contém o projeto eduardo e o aplicativo core, com IndexView e CoreConfig.
O core/models.py original está vazio: não há classes de aluno nem campos de domínio nele.
Por isso, os campos acima foram propostos para a finalidade informada. Eles podem ser ajustados
em core/models.py e core/forms.py, seguidos de makemigrations e migrate.

## Páginas e dados salvos

- `/`: formulário de cadastro. Depois de salvar, abre a ficha do aluno.
- `/alunos/`: lista completa, em ordem alfabética, sem distinguir acentos ou maiúsculas.
  Cada nome abre sua ficha e possui um botão para baixar o PDF.
- `/alunos/<id>/`: ficha com dados salvos, download do PDF e link para voltar à lista.

A navegação principal permite alternar entre cadastro e lista em todas as páginas.
Os dados continuam no SQLite mesmo depois de fechar o navegador ou reiniciar o servidor.
Preserve seu db.sqlite3 ao substituir os arquivos do projeto. Este ZIP não inclui banco de dados.
Cada envio cria uma ficha; nomes iguais são mantidos como registros separados e diferenciados
na lista pela categoria e data da aula. Não há edição de cadastro pela interface.
O PDF é gerado a partir dos dados salvos e não tem numeração no rodapé.

## Login do instrutor

Formulário, lista, fichas e PDFs exigem login, incluindo os links antigos.
Crie sua conta no terminal, na pasta que contém manage.py:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Acesse `/login/` com o usuário e senha criados. Após entrar, abre a lista de alunos.
Use o botão Sair para encerrar a sessão. Não há cadastro público de contas.
Qualquer conta ativa criada neste sistema pode consultar todos os cadastros.
O superusuário também pode editar e remover dados pelo `/admin/`.
Nenhuma conta ou senha é incluída no ZIP.

## Atualizar uma instalação existente

Substitua o código e mantenha o db.sqlite3 e o .env da sua instalação. Execute:

```bash
python manage.py migrate
python manage.py runserver
```

Os cadastros já salvos aparecem automaticamente na lista. Esta atualização de navegação não
altera o modelo nem precisa de uma nova migração. Migrações ainda pendentes serão aplicadas.

## Banco já existente

As migrações mantêm a tabela Relatorio e o campo nome. Os antigos campos genéricos assunto
 e mensagem são removidos; faça uma cópia do banco antes de aplicar em instalação existente
caso precise preservar essas informações. Registros antigos recebem campos novos vazios ou
valores iniciais e devem ser revisados antes de uso. O ZIP não inclui banco nem dados pessoais.

## Testar

```bash
python manage.py test core
python manage.py check
```

## Publicação

Desative DJANGO_DEBUG, configure uma DJANGO_SECRET_KEY aleatória e forte, os domínios
DJANGO_ALLOWED_HOSTS e, se necessário, DJANGO_CSRF_TRUSTED_ORIGINS. Use HTTPS.
O .env.example descreve as opções. Execute migrate e collectstatic no servidor.
O Procfile existente usa Gunicorn. Para PostgreSQL, instale psycopg[binary] e configure POSTGRES_*.
