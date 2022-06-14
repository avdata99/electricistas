class Matriculado:
    def __init__(
        self,
        nro,
        cuil,
        nombre='',
        categoria='',
        registro='',
        localidad='',
        barrio='',
        contacto=''
    ):
        self.numero = nro
        self.cuil = cuil
        self.nombre = nombre
        self.categoria = categoria
        self.registro = registro
        self.localidad = localidad
        self.barrio = barrio
        self.contacto = contacto

    def __str__(self):
        return f'Matriculado {self.numero} {self.cuil}'

    def __repr__(self):
        return f'<Matriculado {self.numero}>'
