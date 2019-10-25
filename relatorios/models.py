from django.db import models


class Consulta(models.Model):
    num_guia_consulta = models.IntegerField()
    cod_medico = models.IntegerField()
    nome_medico = models.CharField(max_length=150)
    data_consulta = models.DateField()
    valor_consulta = models.FloatField()

    def __str__(self):
        return str(self.num_guia_consulta)


class Exame(models.Model):
    cod_exame = models.IntegerField()
    num_guia_consulta = models.ForeignKey(Consulta, related_name="exames", on_delete=models.CASCADE)
    valor_exame = models.FloatField()


