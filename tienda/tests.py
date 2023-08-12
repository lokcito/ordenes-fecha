from django.test import TestCase
from tienda.models import Orden
from datetime import datetime
from django.utils import timezone
import zoneinfo
# Create your tests here.
class TiendaViewsTests(TestCase):

    def test_v_index(self):
        '''
            Debe entregar todos los registros
            si no existen filtros
        '''
        respuesta = self.client.get("/")
        ords = respuesta.context["ordenes"]
        self.assertEqual(0, len(ords))

        no = Orden()
        no.cliente = "Jaimito"
        no.fecha = "2023-12-12"
        no.fecha_envio = "2023-12-12"
        no.direccion = "Av. Libertad"
        no.save()

        respuesta = self.client.get("/")
        ords = respuesta.context["ordenes"]
        self.assertEqual(1, len(ords))
    
    def test_v_index_filtros(self):
        '''
            Entrega los registros con filtros de fecha
        '''
        no = Orden()
        no.cliente = "Pedrito"
        no.fecha = "2022-12-12"
        no.fecha_envio = datetime(2022, 12, 12).\
            astimezone(zoneinfo.ZoneInfo('America/Santiago'))
        no.direccion = "Av. Libertad"
        no.save()

        no = Orden()
        no.cliente = "Albertito"
        no.fecha = "2023-12-12"
        no.fecha_envio = datetime(2023, 12, 12).\
            astimezone(zoneinfo.ZoneInfo('America/Santiago'))
        no.direccion = "Av. Libertad"
        no.save()

        res = self.client.get("/?fecha_inicio=%s&fecha_fin=%s" % (
            '2023-11-01',
            '2023-12-25',
        ))

        ords = res.context["ordenes"]
        self.assertEqual(1, len(ords))



        