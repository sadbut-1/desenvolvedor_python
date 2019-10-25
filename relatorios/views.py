import csv, io, json
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from datetime import datetime
from .models import Consulta, Exame
from django.db.models import F
from django.db.models.functions import TruncMonth
from django.db.models import Count


class RelatorioProducaoMedicaView(TemplateView):
    template_name = "relatorios/relatorio_producao_medica.html"

    def get(self, request, *args, **kwargs):
        context = self.get_consultas()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        filter_result = {
            'medico': request.POST.get('medico'),
            'data_inicio': request.POST.get('data_inicio'),
            'data_fim': request.POST.get('data_fim')
        }

        context = self.get_consultas(filter_result)
        return render(request, self.template_name, context)

    @staticmethod
    def get_consultas(filter_result={}):
        historico = {}
        medicos = Consulta.objects.values_list('nome_medico', flat=True).order_by('nome_medico').distinct()
        qs = Consulta.objects \
            .annotate(gasto_consulta=Sum('exames__valor_exame')) \
            .order_by(F('gasto_consulta').desc(nulls_last=True)).all()

        if filter_result.get('medico'):
            historico['medico'] = filter_result['medico']
            qs = qs.filter(nome_medico=filter_result['medico'])

        if (filter_result.get('data_inicio')) and (filter_result.get('data_fim')):
            historico['data_inicio'] = filter_result['data_inicio']
            historico['data_fim'] = filter_result['data_fim']
            qs = qs.filter(data_consulta__range=(filter_result['data_inicio'], filter_result['data_fim']))

        return {'medicos': medicos, 'consultas': qs, 'historico': historico }


class GraficoProducaoMedicaView(TemplateView):
    template_name = "relatorios/grafico_producao_medica.html"

    def get(self, request, *args, **kwargs):
        context = self.get_consultas()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        filter_result = {'medico': request.POST.get('medico')}
        context = self.get_consultas(filter_result)
        print(context)
        return render(request, self.template_name, context)

    @staticmethod
    def get_consultas(filter_result={}):
        historico = {}
        medicos = Consulta.objects.values_list('nome_medico', flat=True).order_by('nome_medico').distinct()

        qs = Consulta.objects \
            .annotate(mes=TruncMonth('data_consulta')) \
            .values('mes') \
            .annotate(total=Count('mes'))

        if filter_result.get('medico'):
            historico['medico'] = filter_result['medico']
            qs = qs.filter(nome_medico=filter_result['medico'])

        for date in qs:
            date['mes'] = date['mes'].strftime("%m/%Y")

        return {'consultas': json.dumps(list(qs)), 'medicos': medicos, 'historico': historico}


class ImportarArquivosCsv(TemplateView):
    template_name = 'relatorios/importar_csv.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['file']
        option = request.POST.get('opcao')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Este não é um arquivo CSV')

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        if option == 'consulta':
            for column in csv.reader(io_string, delimiter=';', quotechar="|"):
                _, created = Consulta.objects.update_or_create(
                    num_guia_consulta=column[0],
                    cod_medico=column[1],
                    nome_medico=column[2],
                    data_consulta=datetime.strptime(column[3], '%d/%m/%y'),
                    valor_consulta=column[4]
                )
        if option == 'exame':
            for column in csv.reader(io_string, delimiter=';', quotechar="|"):
                consulta = Consulta.objects.only('num_guia_consulta').filter(num_guia_consulta=column[1]).first()
                if consulta:
                    _, created = Exame.objects.update_or_create(
                        cod_exame=column[0],
                        num_guia_consulta=consulta,
                        valor_exame=column[2],
                    )

        context = {}
        return render(request, self.template_name, context)
