from django.contrib import admin

from .models import Consulta, Exame


class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['num_guia_consulta', 'cod_medico', 'nome_medico', 'data_consulta', 'valor_consulta']


class ExameAdmin(admin.ModelAdmin):
    list_display = ['cod_exame', 'num_guia_consulta', 'valor_exame']


admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Exame, ExameAdmin)
