from rest_framework import serializers 
from .models import contratos, fotos, horariospermitidos, interacciones, usuarios
 
class contratosserializer(serializers.ModelSerializer):
 
    class Meta:
        model= contratos
        fields = ['nombre']

class usuariosserializer(serializers.ModelSerializer):
 
    class Meta:
        model = usuarios
        fields = ['cedula', 'nombre', 'contrato']

class horariosserializer(serializers.ModelSerializer):
 
    class Meta:
        model = horariospermitidos
        fields = ['id', 'cedula', 'dia', 'entrada', 'salida']

class interaccionesserializer(serializers.ModelSerializer):

    class Meta:
        model= interacciones
        fields = ['cedula','nombre','fecha','hora','razon','contrato']

class fotosserializer(serializers.ModelSerializer):

    class Meta:
        model = fotos
        fields = ['id','cedula', 'foto', 'estado']

class filtrosserializer(serializers.Serializer):
    cedula = serializers.IntegerField()
    contrato = serializers.CharField()
    fechadesde = serializers.DateField()
    fechahasta = serializers.DateField()
    horadesde = serializers.TimeField()
    horahasta = serializers.TimeField()



# class stringserializer(serializers.Serializer):
#     string = serializers.CharField(max_length=200)

