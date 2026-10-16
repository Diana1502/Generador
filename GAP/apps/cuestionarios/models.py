import uuid

from traits.trait_types import self

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

# Clase principal - encargada de registrar los avisos de privacidad creados
class Cuestionario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname =  models.CharField(max_length=100, null=True, blank=True)
    sujetoObligado = models.CharField(max_length=100, null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    completado = models.BooleanField(default=False)

    seccion_actual = models.PositiveSmallIntegerField(
        default=1,
        validators=[MaxValueValidator(12)] # Número de secciones
    )

    fecha_finalizado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.id}"

# Clases auxiliares
class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    # Municipio
class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="municipios")

    def __str__(self):
        return f"{self.nombre} ({self.estado.nombre})"

########Clases de Secciones
# Secc 1
class SecResponsable(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    # sujetoObligado = models.CharField(max_length=100)
    unidadAdmin = models.CharField(max_length=100)
    acronSujetoObligado = models.CharField(max_length=100)
    acronUnidadAdmin = models.CharField(max_length=100)

    # Direccion
    calle_responsable = models.CharField(max_length=50)
    numExt_responsable = models.CharField(max_length=10)
    numInt_responsable = models.CharField(max_length=10, blank=True, null=True)
    colonia_responsable = models.CharField(max_length=50)
    municipio_responsable = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    entidadFed_responsable = models.ForeignKey(Estado, on_delete=models.CASCADE)
    codigoPost_responsable = models.CharField(max_length=5)

    def direccion_texto(self):
        direccion = (
            f"{self.calle_responsable} "
            f"No. {self.numExt_responsable}"
        )

        if self.numInt_responsable:
            direccion += f", Int. {self.numInt_responsable}"

        direccion += (
            f", Col. {self.colonia_responsable}"
            f", {self.municipio_responsable.nombre}"
            f", {self.entidadFed_responsable.nombre}"
            f", C.P. {self.codigoPost_responsable}"
        )

        return direccion

    def __str__(self):
        return f"{self.acronSujetoObligado}"

# Secc 2
class SecTratamiento(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    nombreTratamiento = models.CharField(max_length=100)
    descTratamiento = models.TextField()
    objTratamiento = models.TextField()

    def __str__(self):
        return f"{self.nombreTratamiento}"

class SecDatoPersonal(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cuestionario}"

class DatoPersonal(models.Model):
    seccion = models.ForeignKey(SecDatoPersonal, on_delete=models.CASCADE, related_name="datospersonales")

    dato = models.CharField(max_length=100)
    datosSensibles = models.BooleanField(default=False)

    TIPO_OBTENCION = [
        ('T', 'Directamente del titular'),
        ('E', 'Representante legal'),
        ('A', 'Otra autoridad'),
        ('D', 'Otra dependencia'),
        ('P', 'Fuente pública'),
        ('W', 'Plataforma electrónica'),
        ('R', 'Tercero autorizado'),
        ('O', 'Otro '),
    ]
    obtencionDatos = MultiSelectField(max_length=8, choices=TIPO_OBTENCION,  blank=True)
    obtencionDatos_otro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Otra fuente de info")

    TIPO_MEDIO = [
        ('', 'Seleccione una opción'),
        ('F', 'Formulario'),
        ('E', 'Ventanilla'),
        ('C', 'Correo electrónico'),
        ('S', 'Sistema'),
        ('A', 'Aplicación'),
        ('W', 'Portal web'),
        ('L', 'Llamada telefónica'),
        ('V', 'Videollamada'),
        ('D', 'Documento físico'),
        ('O', 'Otro '),
    ]
    medioObtencion = models.CharField(max_length=1, choices=TIPO_MEDIO,  blank=True, null=True)
    medioObtencion_otro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Otro medio de obtención")

    def __str__(self):
        return f"{self.dato}{' - sensible' if self.datosSensibles else ''}"

# Secc 3
class SecFundamento(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cuestionario}"

class Fundamento(models.Model):
    seccion = models.ForeignKey(SecFundamento, on_delete=models.CASCADE, related_name="fundamentos")

    ley = models.CharField(max_length=100)
    especificacion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ley}"

# Secc 4
class SecFinalidad(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cuestionario}"

class Finalidad(models.Model):
    seccion = models.ForeignKey(SecFinalidad, on_delete=models.CASCADE, related_name="finalidades")

    finalidad = models.CharField(max_length=500)
    necesaria = models.BooleanField(default=False)
    reqConsentimiento = models.BooleanField(default=False)
    finPrincipal = models.BooleanField(default=False)
    TIPO_CONSENTIMIENTO = [
        ('', 'Seleccione una opción'),
        ('T', 'Tácito'),
        ('E', 'Expreso'),
    ]
    tipoConsentimiento = models.CharField(max_length=1, choices=TIPO_CONSENTIMIENTO, blank=True, null=True)
    tipoConsentimiento_otro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Otro tipo de consentimiento")

    def __str__(self):
        return f"{self.finalidad}{' - Principal' if self.finPrincipal else ''}"

# Secc 5
class SecEjercicioARCO(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    procARCO = models.TextField()
    MEDIO_PRESENTACION = [
        ('P', 'Plataforma'),
        ('C', 'Correo'),
        ('F', 'Presencial'),
        ('E', 'Escrito Libre'),
        ('I', 'Sistema institucional'),
        ('W', 'Otro'),
    ]
    medPresentacion = MultiSelectField(max_length=11, choices=MEDIO_PRESENTACION, blank=True)
    # Para calcular el max_length es 2*n - 1
    medPresentacion_otro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Otro medio")

    unidadResp = models.CharField(max_length=100)
    # Direccion
    calle_unidadresp = models.CharField(max_length=50)
    numExt_unidadresp = models.CharField(max_length=10)
    numInt_unidadresp = models.CharField(max_length=10, blank=True, null=True)
    colonia_unidadresp = models.CharField(max_length=50)
    municipio_unidadresp = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    entidadFed_unidadresp = models.ForeignKey(Estado, on_delete=models.CASCADE)
    codigoPost_unidadresp = models.CharField(max_length=5)

    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    extension = models.CharField(max_length=20)

    def direccion_texto(self):
        direccion = (
            f"{self.calle_unidadresp} "
            f"No. {self.numExt_unidadresp}"
        )

        if self.numInt_unidadresp:
            direccion += f", Int. {self.numInt_unidadresp}"

        direccion += (
            f", Col. {self.colonia_unidadresp}"
            f", {self.municipio_unidadresp.nombre}"
            f", {self.entidadFed_unidadresp.nombre}"
            f", C.P. {self.codigoPost_unidadresp}"
        )

        return direccion
    def telefono_texto(self):
        telefono_formateado = self.telefono[:2] + " " + self.telefono[2:6] + " " + self.telefono[6:]
        return telefono_formateado

    def __str__(self):
        return f"{self.procARCO}"

# Secc 6
class SecUT(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    telefono = models.CharField(max_length=10)
    extension = models.CharField(max_length=20)
    correo = models.CharField(max_length=100)
    horarioInicio = models.TimeField()
    horarioFin = models.TimeField()
    paginaWeb = models.URLField(max_length=200, blank=True, null=True)

    # Direccion
    calle_ut = models.CharField(max_length=50)
    numExt_ut = models.CharField(max_length=10)
    numInt_ut = models.CharField(max_length=10, blank=True, null=True)
    colonia_ut = models.CharField(max_length=50)
    municipio_ut = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    entidadFed_ut = models.ForeignKey(Estado, on_delete=models.CASCADE)
    codigoPost_ut = models.CharField(max_length=5)

    def direccion_texto(self):
        direccion = (
            f"{self.calle_ut} "
            f"No. {self.numExt_ut}"
        )

        if self.numInt_ut:
            direccion += f", Int. {self.numInt_ut}"

        direccion += (
            f", Col. {self.colonia_ut}"
            f", {self.municipio_ut.nombre}"
            f", {self.entidadFed_ut.nombre}"
            f", C.P. {self.codigoPost_ut}"
        )

        return direccion
    def telefono_texto(self):
        telefono_formateado = self.telefono[:2] + " " + self.telefono[2:6] + " " + self.telefono[6:]
        return telefono_formateado

    def __str__(self):
        return f"{self.paginaWeb}"

# Secc 7
class SecTransferencias(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    transferencias = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transferencias}"

class Destinatario(models.Model):
    seccion = models.ForeignKey(SecTransferencias, on_delete=models.CASCADE, related_name='destinatarios')

    TIPO_TRANSFERENCIA = [
        ('', 'Seleccione una opción'),
        ('A', 'Entidad o Dependencia de la APF'),
        ('F', 'Entidad federativa'),
        ('M', 'Municipio'),
        ('G', 'Organismo autónomo'),
        ('P', 'Particular'),
    ]
    finalidad = models.ManyToManyField(Finalidad)
    destinatario = models.CharField(max_length=100)
    tipoConsentimiento = models.CharField(max_length=1, choices=TIPO_TRANSFERENCIA, blank=True, null=True)
    consentimiento = models.BooleanField(default=False)

    def finalidades_formateadas(self):
        finalidades = list(
            self.finalidad.values_list("finalidad", flat=True)
        )

        if not finalidades:
            return ""

        if len(finalidades) == 1:
            return finalidades[0] + "."

        return ", ".join(finalidades[:-1]) + " y " + finalidades[-1] + "."

    def __str__(self):
        return f"{self.destinatario}"

# Secc 8
class SecManifNegativa(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    manifestacion = models.TextField()

# Secc 9
class SecCambiosAvP(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    PUBLICA_MODIFICACIONES = [
        ('W', 'Portal Institucional'),
        ('E', 'Estrados'),
        ('M', 'Micrositio'),
        ('O', 'Otro'),
    ]
    modificaciones = MultiSelectField(max_length=7, choices=PUBLICA_MODIFICACIONES, blank=True)
    modificaciones_otro = models.CharField(max_length=255,blank=True, null=True, verbose_name="Otro medio")

    url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.url}"

    def clean(self):
        super().clean()

        if "O" in (self.modificaciones or []) and not self.modificaciones_otro:
            raise ValidationError({
                "modificaciones_otro": "Debe especificar cuál es la otra modificación."
            })

# Sec - portabilidad
class SecPortabilidad(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    portabilidad = models.TextField(blank=True, null=True)

# Secc 10
class SecInfoCompl(models.Model):
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)

    desicNotHuman = models.BooleanField(default=False)
    usoNube = models.BooleanField(default=False)
    encargadosTrat = models.BooleanField(default=False)
    remisiones = models.BooleanField(default=False)
    menorEdad = models.BooleanField(default=False)
    biometricos = models.BooleanField(default=False)
    evalImpacto = models.BooleanField(default=False)
    observaciones = models.CharField(blank=True, null=True)