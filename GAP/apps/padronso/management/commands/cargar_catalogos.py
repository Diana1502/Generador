import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.cuestionarios.models import Estado, Municipio
from apps.padronso.models import Sujeto


class Command(BaseCommand):
    help = "Carga los catálogos iniciales de estados, municipios y sujetos obligados."

    def handle(self, *args, **options):
        carpeta_datos = Path(settings.BASE_DIR) / "data"

        archivo_estados = carpeta_datos / "EdosMunicipios.json"
        archivo_sujetos = carpeta_datos / "PadronSO.json"

        # Validar que existan ambos archivos antes de comenzar.
        for archivo in (archivo_estados, archivo_sujetos):
            if not archivo.is_file():
                raise CommandError(
                    f"No se encontró el archivo: {archivo}"
                )

        try:
            with archivo_estados.open("r", encoding="utf-8") as f:
                datos_estados = json.load(f)

            with archivo_sujetos.open("r", encoding="utf-8") as f:
                datos_sujetos = json.load(f)

        except (OSError, json.JSONDecodeError) as e:
            raise CommandError(f"Error al leer los JSON: {e}") from e

        if not isinstance(datos_estados, dict):
            raise CommandError(
                "EdosMunicipios.json debe contener un objeto JSON."
            )

        if not isinstance(datos_sujetos, list):
            raise CommandError(
                "PadronSO.json debe contener una lista de elementos."
            )

        try:
            with transaction.atomic():
                self.stdout.write("Cargando estados y municipios...")

                estados_creados = 0
                municipios_creados = 0

                for estado_nombre, municipios in datos_estados.items():
                    estado, creado = Estado.objects.get_or_create(
                        nombre=estado_nombre
                    )

                    if creado:
                        estados_creados += 1

                    for municipio_nombre in municipios:
                        _, creado = Municipio.objects.get_or_create(
                            nombre=municipio_nombre,
                            estado=estado
                        )

                        if creado:
                            municipios_creados += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Estados nuevos: {estados_creados}. "
                        f"Municipios nuevos: {municipios_creados}."
                    )
                )

                self.stdout.write("Cargando sujetos obligados...")

                sujetos_creados = self.guardar_elementos(
                    datos_sujetos
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Sujetos nuevos: {sujetos_creados}."
                    )
                )

        except Exception as e:
            raise CommandError(
                f"No se pudieron cargar los catálogos: {e}"
            ) from e

        self.stdout.write(
            self.style.SUCCESS(
                "Carga de catálogos finalizada correctamente."
            )
        )

    def guardar_elementos(self, lista_elementos, padre=None):
        total_creados = 0

        for item in lista_elementos:
            nombre = item.get("nombre")

            if not nombre:
                continue

            elemento, creado = Sujeto.objects.get_or_create(
                nombre=nombre,
                padre=padre
            )

            if creado:
                total_creados += 1

            hijos = item.get("hijos", [])

            if hijos:
                total_creados += self.guardar_elementos(
                    hijos,
                    padre=elemento
                )

        return total_creados