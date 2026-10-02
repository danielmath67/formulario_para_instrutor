from django.contrib import admin

from .models import Relatorio


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instrutor', 'categoria', 'data_aula', 'criado_em')
    search_fields = ('nome', 'instrutor', 'renach')
    list_filter = ('categoria', 'situacao')
    readonly_fields = ('id', 'criado_em')
