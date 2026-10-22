from django import forms
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe #Negritas en label

from .models import Municipio, Estado
from .models import Cuestionario
from .models import (SecResponsable, SecTratamiento, SecFundamento, SecFinalidad, SecEjercicioARCO, SecUT, SecTransferencias, SecManifNegativa, SecCambiosAvP,
 SecInfoCompl, SecDatoPersonal, SecPortabilidad)

solo_numeros = RegexValidator(
    regex=r'^\d+$',
    message='Este campo solo acepta números'
)

class CuestionarioForm(forms.ModelForm):
    class Meta:
        model = Cuestionario
        fields = ['nickname']
        widgets = {
            # Le agregamos la clase de Bootstrap y un placeholder para que se vea
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el nombre aquí...',
                'required': True
            })
        }

# Secc 1
class SecResponsableForm(forms.ModelForm):

    acronSujetoObligado = forms.CharField(
        label=mark_safe
            ("¿Cuáles son las <strong>siglas</strong> que usa?"),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    unidadAdmin = forms.CharField(
        label=mark_safe
            ("¿Cuál es el nombre de la <strong>unidad administrativa</strong> responsable del tratamiento de los datos personales?"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    acronUnidadAdmin = forms.CharField(
        label=mark_safe
            ("¿Cuáles son las <strong>siglas</strong> del responsable del tratamiento de los datos personales?"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    # Dirección
    calle_responsable = forms.CharField(
        label="Calle o avenida",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    numExt_responsable = forms.CharField(
        label="Numero Exterior",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    numInt_responsable = forms.CharField(
        label="Numero Interior",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    colonia_responsable = forms.CharField(
        label="Colonia",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    municipio_responsable = forms.ModelChoiceField(
        queryset=Municipio.objects.none(),
        label="Alcaldía / Municipio",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    entidadFed_responsable = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Entidad Federativa",
        widget = forms.Select(attrs={
            'class': 'form-select'
        })
    )

    codigoPost_responsable = forms.CharField(
        label="Código Postal",
        max_length=5,
        validators=[solo_numeros],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    class Meta:
        model = SecResponsable
        fields = [
            'unidadAdmin',
            'acronSujetoObligado',
            'acronUnidadAdmin',
            'calle_responsable',
            'numExt_responsable',
            'numInt_responsable',
            'colonia_responsable',
            'municipio_responsable',
            'entidadFed_responsable',
            'codigoPost_responsable',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay estado seleccionado (POST o edición)
        if 'entidadFed_responsable' in self.data:
            try:
                estado_id = int(self.data.get('entidadFed_responsable'))
                self.fields['municipio_responsable'].queryset = (
                    Municipio.objects.filter(estado_id=estado_id)
                )
            except (ValueError, TypeError):
                pass

        # Si es edición (instance ya guardada)
        elif self.instance.pk:
            self.fields['municipio_responsable'].queryset = (
                Municipio.objects.filter(
                    estado=self.instance.entidadFed_responsable
                )
            )

    def clean(self):
        cleaned_data = super().clean()

# Secc 2
class SecTratamientoForm(forms.ModelForm):
    nombreTratamiento = forms.CharField(
        label=mark_safe
        ("¿Cuál es el <strong>nombre del tratamiento</strong>?"),
        max_length=200,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,  # número de filas visibles
        })
    )
    descTratamiento = forms.CharField(
        label=mark_safe
        ("Describa brevemente el tratamiento."),
        max_length=300,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,  # número de filas visibles
        })
    )
    objTratamiento = forms.CharField(
        label=mark_safe
        ("¿Cuál es el objetivo del tratamiento?"),
        max_length=300,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,  # número de filas visibles
        })
    )

    class Meta:
        model = SecTratamiento
        fields = [
            'nombreTratamiento',
            'descTratamiento',
            'objTratamiento'
        ]

# Secc 2
class SecDatoPersonalForm(forms.ModelForm):

    class Meta:
        model = SecDatoPersonal
        fields = []

# Secc 3
class SecFundamentoForm(forms.ModelForm):

    class Meta:
        model = SecFundamento
        fields = []

# Secc 4
class SecFinalidadesForm(forms.ModelForm):

    class Meta:
        model = SecFinalidad
        fields = []

# Secc 5
class SecEjercicioARCOForm(forms.ModelForm):
    procARCO = forms.CharField(
        label=mark_safe("Describa el <strong>procedimiento<strong> para la </strong>solicitud de derechos ARCO</strong>."),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,  # número de filas visibles
        })
    )

    unidadResp = forms.CharField(
        label=mark_safe("Nombre de la unidad responsable"),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    correo = forms.CharField(
        label=mark_safe("Correo electrónico"),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    telefono = forms.CharField(
        label=mark_safe("Teléfono"),
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    extension = forms.CharField(
        label=mark_safe("Extension(es)"),
        max_length=20,
        # validators=[solo_numeros],
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    # Dirección
    calle_unidadresp = forms.CharField(
        label="Calle o avenida",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    numExt_unidadresp = forms.CharField(
        label="Numero Exterior",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    numInt_unidadresp = forms.CharField(
        label="Numero Interior",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    colonia_unidadresp = forms.CharField(
        label="Colonia",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    municipio_unidadresp = forms.ModelChoiceField(
        queryset=Municipio.objects.none(),
        label="Alcaldía / Municipio",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    entidadFed_unidadresp = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Entidad Federativa",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    codigoPost_unidadresp = forms.CharField(
        label="Código Postal",
        max_length=5,
        validators=[solo_numeros],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    class Meta:
        model = SecEjercicioARCO
        fields = [
            'procARCO',
            'medPresentacion',
            'unidadResp',
            'calle_unidadresp',
            'numExt_unidadresp',
            'numInt_unidadresp',
            'colonia_unidadresp',
            'municipio_unidadresp',
            'entidadFed_unidadresp',
            'codigoPost_unidadresp',
            'correo',
            'telefono',
            'extension'
        ]

        # widgets = {
        #     'medPresentacion': forms.CheckboxSelectMultiple(
        #         attrs={
        #             'class': 'form-check-input'
        #         }
        #     ),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay estado seleccionado (POST o edición)
        if 'entidadFed_unidadresp' in self.data:
            try:
                estado_id = int(self.data.get('entidadFed_unidadresp'))
                self.fields['municipio_unidadresp'].queryset = (
                    Municipio.objects.filter(estado_id=estado_id)
                )
            except (ValueError, TypeError):
                pass

        # Si es edición (instance ya guardada)
        elif self.instance.pk:
            self.fields['municipio_unidadresp'].queryset = (
                Municipio.objects.filter(
                    estado=self.instance.entidadFed_unidadresp
                )
            )

    def clean(self):
        cleaned_data = super().clean()

# Secc 6
class SecUTForm(forms.ModelForm):
    correo = forms.CharField(
        label=mark_safe("Correo electrónico"),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    telefono = forms.CharField(
        label=mark_safe("Teléfono"),
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    extension = forms.CharField(
        label=mark_safe("Extension(es)"),
        max_length=20,
        # validators=[solo_numeros],
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    paginaWeb = forms.URLField(
        label=mark_safe("Página web"),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    horarioInicio =  forms.TimeField(
        label=mark_safe("Hora de inicio:"),
    )
    horarioFin =  forms.TimeField(
        label=mark_safe("Hora de fin:"),
    )
    # Dirección
    calle_ut = forms.CharField(
        label="Calle o avenida",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    numExt_ut = forms.CharField(
        label="Numero Exterior",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    numInt_ut = forms.CharField(
        label="Numero Interior",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    colonia_ut = forms.CharField(
        label="Colonia",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    municipio_ut = forms.ModelChoiceField(
        queryset=Municipio.objects.none(),
        label="Alcaldía / Municipio",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    entidadFed_ut = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Entidad Federativa",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    codigoPost_ut = forms.CharField(
        label="Código Postal",
        max_length=5,
        validators=[solo_numeros],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. 01234'
        })
    )

    class Meta:
        model = SecUT
        fields = [
            'telefono',
            'correo',
            'extension',
            'horarioInicio',
            'horarioFin',
            'paginaWeb',
            'calle_ut',
            'numExt_ut',
            'numInt_ut',
            'colonia_ut',
            'municipio_ut',
            'entidadFed_ut',
            'codigoPost_ut'
        ]
        widgets = {
            'horarioInicio': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',  # Activa el selector de hora nativo del navegador
                    'class': 'form-control',  # Tu clase CSS (p. ej. Bootstrap/Tailwind)
                }
            ),
            'horarioFin': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay estado seleccionado (POST o edición)
        if 'entidadFed_ut' in self.data:
            try:
                estado_id = int(self.data.get('entidadFed_ut'))
                self.fields['municipio_ut'].queryset = (
                    Municipio.objects.filter(estado_id=estado_id)
                )
            except (ValueError, TypeError):
                pass

        # Si es edición (instance ya guardada)
        elif self.instance.pk:
            self.fields['municipio_ut'].queryset = (
                Municipio.objects.filter(
                    estado=self.instance.entidadFed_ut
                )
            )

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('horarioInicio')
        fin = cleaned_data.get('horarioFin')

        if inicio and fin and fin <= inicio:
            self.add_error('horarioFin', 'La hora de fin debe ser posterior a la hora de inicio.')

        return cleaned_data

# Secc 7
class SecTransferenciasForm(forms.ModelForm):
    transferencias = forms.BooleanField(
        label=mark_safe("¿Se realizarán <strong>transferencias</strong> de datos personales que requieran consentimiento?"),
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'id_transferencias',
            }
        ),
        required=False
    )

    class Meta:
        model = SecTransferencias
        fields = [
            'transferencias'
        ]

# Secc 8
class SecManifNegaForm(forms.ModelForm):
    manifestacion = forms.CharField(
        label=mark_safe("¿Cómo puede manifestar el titular su negativa a finalidades que requieren el consentimiento?."),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,  # número de filas visibles
        })
    )

    class Meta:
        model = SecManifNegativa
        fields = [
            'manifestacion'
        ]

    def clean(self):
        cleaned_data = super().clean()

# Secc 9
class SecCambiosAvPForm(forms.ModelForm):
    modificaciones_otro = forms.CharField(
        label=mark_safe("Especifique que otros medios"),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=False
    )
    url = forms.URLField(
        label=mark_safe("URL para consultar los cambios al aviso de privacidad"),
        assume_scheme='https',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
    )

    class Meta:
        model = SecCambiosAvP
        fields = [
            'modificaciones',
            'modificaciones_otro',
            'url'
        ]

    def clean(self):
        cleaned_data = super().clean()

# Secc - portabilidad
class SecPortabilidadForm(forms.ModelForm):
    portabilidad = forms.CharField(
        label=mark_safe("¿Cómo se puede ejercer el derecho a la portabilidad de datos personales?."),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,  # número de filas visibles
        }),
        required=False
    )

    class Meta:
        model = SecPortabilidad
        fields = [
            'portabilidad'
        ]

    def clean(self):
        cleaned_data = super().clean()


# Secc 10
class SecInfoComplForm(forms.ModelForm):
    desicNotHuman = forms.BooleanField(
        label=mark_safe("¿Se utilizan <strong>sistemas automatizados</strong>?"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    usoNube = forms.BooleanField(
        label=mark_safe("¿Se utilizan <strong>servicios en la nube</strong>?"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    encargadosTrat = forms.BooleanField(
        label=mark_safe("¿Existen <strong>encargados del tratamiento</strong>?"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    remisiones = forms.BooleanField(
        label=mark_safe("¿Existen <strong>remisiones</strong> de datos?"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    menorEdad = forms.BooleanField(
        label=mark_safe("¿El tratamiento involucra <strong>menores de edad</strong>?"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    biometricos = forms.BooleanField(
        label=mark_safe("¿Se recaban datos <strong>biométricos</strong>?"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    evalImpacto = forms.BooleanField(
        label=mark_safe("¿Existe <strong>evaluación de impacto</strong> en protección de datos personales?"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    observaciones = forms.CharField(
        label=mark_safe("Observaciones adicionales"),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Escribe las observaciones aquí...'
        }),
        required=False
    )

    class Meta:
        model = SecInfoCompl
        fields = [
            'desicNotHuman',
            'usoNube',
            'encargadosTrat',
            'remisiones',
            'menorEdad',
            'biometricos',
            'evalImpacto',
            'observaciones'
        ]

    def clean(self):
        cleaned_data = super().clean()
