from select import select
from django import forms
from .models import contratos, fotos, usuarios, horariospermitidos

class clienteform(forms.ModelForm):

    class Meta:
        model = usuarios
        fields = ['cedula', 'nombre', 'contrato']

class clienteformhorarios(forms.ModelForm):

    class Meta:
        model = horariospermitidos
        fields = ['cedula', 'dia', 'entrada', 'salida']
        widgets = {
            'entrada': forms.TimeInput(attrs={'placeholder':'hora:minuto', 'type': 'time'}),
            'salida': forms.TimeInput(attrs={'placeholder':'hora:minuto', 'type': 'time'}),
            }

class contratosform(forms.ModelForm):

    class Meta:
        model= contratos
        fields = ['nombre']

class elegircontrato(forms.Form):
    contrato=forms.ModelChoiceField(queryset=contratos.objects.all(), widget=forms.Select)

class filtrarinteracciones(forms.Form):
    #cedula=forms.ModelChoiceField(queryset=usuarios.objects.values_list('cedula', flat=True).distinct(), widget=forms.Select, required=False)
    cedula=forms.IntegerField(required=False)
    fechadesde=forms.DateField(required=False, label="Desde(Fecha)",widget=forms.DateInput(attrs={'type': 'date'})) #aaaa-mm-dd
    fechahasta=forms.DateField(required=False, label="Hasta(Fecha)",widget=forms.DateInput(attrs={'type': 'date'})) #aaaa-mm-dd
    horadesde=forms.TimeField(required=False, label="Desde(Hora)", widget=forms.TimeInput(attrs={'type': 'time'})) #hh:mm
    horahasta=forms.TimeField(required=False, label="Hasta(Hora)", widget=forms.TimeInput(attrs={'type': 'time'})) #hh:mm

    # fechadesde=forms.DateField(required=False, label="Desde(Fecha)",widget=forms.DateInput(attrs={'type': 'date'})) #aaaa-mm-dd
    # fechahasta=forms.DateField(required=False, label="Hasta(Fecha)",widget=forms.DateInput(attrs={'type': 'date'})) #aaaa-mm-dd
    # horadesde=forms.TimeField(required=False, label="Desde(Hora)", widget=forms.TimeInput(attrs={'placeholder':'hora:minuto'})) #hh:mm
    # horahasta=forms.TimeField(required=False, label="Hasta(Hora)", widget=forms.TimeInput(attrs={'placeholder':'hora:minuto'}))
    
class filtrarusuarios(forms.Form):
    cedulaf=forms.IntegerField(required=False, label="Buscar por cedula")

class subirfoto(forms.ModelForm):
    class Meta:
        model = fotos
        fields = ['cedula', 'foto']
