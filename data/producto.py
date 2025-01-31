
class bobina:
    def __init__(self, ancho, diametro, gramaje, peso, bobina_nro, sec, orden_fab, fecha, turno, calidad):
        self.ancho = ancho
        self.diametro = diametro
        self.gramaje = gramaje
        self.peso = peso
        self.bobina_nro = bobina_nro
        self.sec = sec
        self.orden_fab = orden_fab
        self.fecha = fecha
        self.turno = turno
        self.calidad = calidad

    def imprimir_log(self):
        print(f"Parametros ingresados {self.bobina_nro, self.orden_fab}.")
        return