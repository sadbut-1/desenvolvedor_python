import csv, io
from django.test import TestCase, Client

from datetime import datetime
from .models import Consulta, Exame


class ConsultaTest(TestCase):

    def load_data(self):
        client = Client()
        with open('storage/consulta.csv') as csv_file:
            client.post('/relatorios/importar/', {'opcao': 'consulta', 'file': csv_file})
        with open('storage/exame.csv') as csv_file:
            client.post('/relatorios/importar/', {'opcao': 'exame', 'file': csv_file})
        return client

    def test_insert_consulta_on_db(self):
        consulta = Consulta.objects.create(
            num_guia_consulta=12345,
            cod_medico=12,
            nome_medico='João da Silva',
            data_consulta=datetime.strptime('04/02/17', '%d/%m/%y'),
            valor_consulta=90.00
        )
        self.assertEquals('João da Silva', consulta.nome_medico)
        self.assertEquals(12, consulta.cod_medico)
        self.assertEquals(12345, consulta.num_guia_consulta)
        self.assertEquals(90.0, consulta.valor_consulta)

    def test_import_csv_consulta_and_save_on_db(self):
        client = Client()
        with open('storage/consulta.csv') as csv_file:
            response = client.post('/relatorios/importar/', {'opcao': 'consulta', 'file': csv_file})
        self.assertEquals(200, response.status_code)
        consulta = Consulta.objects.all().first()
        self.assertIsNotNone(consulta)
        self.assertEquals('João da Silva', consulta.nome_medico)

    def test_query_producao_medica(self):
        client = self.load_data()
        response = client.get('/relatorios/producao_medica/')
        self.assertEquals(200, response.status_code)
        self.assertIn('Mariana Torres', str(response.content))

    def test_query_producao_medica_with_medico_filter(self):
        client = self.load_data()
        response = client.post('/relatorios/producao_medica/', {'medico': 'Getúlio Miranda'})
        self.assertEquals(200, response.status_code)
        self.assertNotIn('03/03/2017', str(response.content))

    def test_query_producao_medica_with_date_filter(self):
        client = self.load_data()
        response = client.post('/relatorios/producao_medica/', {'data_inicio': '2017-03-03', 'data_fim': '2017-03-03'})
        self.assertEquals(200, response.status_code)
        self.assertNotIn('04/01/2018', str(response.content))

    def test_gerar_grafico_endpoint(self):
        client = self.load_data()
        response = client.get('/relatorios/grafico_producao_medica')
        self.assertEquals(200, response.status_code)
        self.assertIn('01/2018', str(response.content))

class ExameTest(TestCase):

    def test_insert_exame_on_db(self):
        consulta = Consulta.objects.create(
            num_guia_consulta=12345,
            cod_medico=12,
            nome_medico='João da Silva',
            data_consulta=datetime.strptime('04/02/17', '%d/%m/%y'),
            valor_consulta=90.00
        )
        exame = Exame.objects.create(
            cod_exame=1,
            num_guia_consulta=consulta,
            valor_exame=10.00
        )
        self.assertEquals(1, exame.cod_exame)
        self.assertEquals(10.0, exame.valor_exame)

    def test_import_csv_exame_and_save_on_db(self):
        client = Client()
        with open('storage/consulta.csv') as csv_file:
            client.post('/relatorios/importar/', {'opcao': 'consulta', 'file': csv_file})
        with open('storage/exame.csv') as csv_file:
            response = client.post('/relatorios/importar/', {'opcao': 'exame', 'file': csv_file})
        self.assertEquals(200, response.status_code)
        exame = Exame.objects.all().first()
        self.assertIsNotNone(exame)
        self.assertEquals(2222, exame.cod_exame)
