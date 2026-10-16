from django.db import models

# Create your models here.
class Sujeto(models.Model):
    nombre = models.CharField(max_length=255)

    padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='hijos'
    )

    class Meta:
        verbose_name = "Elemento de Catálogo"
        verbose_name_plural = "Elementos de Catálogo"

    def __str__(self):
        return self.nombre

    # Método útil para saber si es un elemento "hoja" (el último nivel de su rama)
    @property
    def es_hoja(self):
        return not self.hijos.exists()