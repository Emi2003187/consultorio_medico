from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('medico', 'Médico'),
        ('asistente', 'Asistente'),
    )

    rol = models.CharField(max_length=20, choices=ROLES)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    cedula_profesional = models.CharField(max_length=20, blank=True, null=True)
    institucion_cedula = models.CharField(max_length=100, blank=True, null=True)

    # Nuevo campo:
    consultorio = models.ForeignKey(
        'Consultorio',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_asignados'
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.rol})"




# PACIENTE
 
class Paciente(models.Model):
    SEXO_CHOICES = (('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro'))

    nombre_completo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.TextField()
    historial_clinico = models.TextField(blank=True, null=True)
    consultorio_asignado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='pacientes_asignados')  

    def __str__(self):
        return self.nombre_completo



class Consulta(models.Model):
    ESTADO_OPCIONES = [
        ('espera', 'En Espera'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='espera')

    asistente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_asistente')
    medico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_medico')

    observaciones_finales = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consulta de {self.paciente} ({self.fecha.strftime('%d/%m/%Y')})"


 
# SIGNOS VITALES + SÍNTOMAS
 
class SignosVitales(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='signos_vitales')
    tension_arterial = models.CharField(max_length=10, blank=True, null=True)
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True)
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
    talla = models.FloatField(blank=True, null=True)
    circunferencia_abdominal = models.FloatField(blank=True, null=True)
    imc = models.FloatField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    sintomas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Signos de {self.consulta.paciente}"


 
# RECETA MÉDICA
class Receta(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='receta')
    medico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='recetas_emitidas')
    fecha_emision = models.DateField(auto_now_add=True)
    direccion = models.TextField(blank=True, null=True)

    medicamentos = models.TextField(help_text="Lista de medicamentos: nombre, dosis, frecuencia, duración")
    indicaciones_adicionales = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receta para {self.consulta.paciente}"

class Consultorio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ubicacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre



# (Opcional) AUDITORÍA
##ESTA MADRE SE LLENA CON UN TRIGGER
class Auditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion[:40]}"