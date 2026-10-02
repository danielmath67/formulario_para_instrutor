import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('nome', models.CharField(max_length=120, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('assunto', models.CharField(max_length=150, verbose_name='Assunto')),
                ('mensagem', models.TextField(max_length=2000, verbose_name='Mensagem')),
            ],
            options={
                'verbose_name': 'Relatório',
                'verbose_name_plural': 'Relatórios',
                'ordering': ['-criado_em'],
            },
        ),
    ]
