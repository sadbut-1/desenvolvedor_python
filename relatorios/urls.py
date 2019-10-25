from django.urls import path

from .views import RelatorioProducaoMedicaView, GraficoProducaoMedicaView, ImportarArquivosCsv

urlpatterns = [
    path('producao_medica/', RelatorioProducaoMedicaView.as_view()),
    path('grafico_producao_medica', GraficoProducaoMedicaView.as_view()),
    path('importar/', ImportarArquivosCsv.as_view()),
]