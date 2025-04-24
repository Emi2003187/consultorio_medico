import os
import django
import random
import datetime

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultorio_medico.settings')
django.setup()

from django.contrib.auth import get_user_model
from consultorio_API.models import Consultorio, Usuario, Paciente, Consulta, SignosVitales, Receta

User = get_user_model()

def run():
    # Crear admin
    if not User.objects.filter(username='Emiliong').exists():
        admin = User.objects.create_user(
            username='Emiliong',
            email='Emiliong@gmail.com',
            password='Shec!d1357',
            first_name='Emilio',
            last_name='González',
            rol='admin',
            is_superuser=True,
            is_staff=True
        )
        print("✅ Administrador creado.")
    else:
        admin = User.objects.get(username='Emiliong')
        print("ℹ️ Administrador ya existe.")

    # Crear consultorios
    consultorios = []
    for nombre in ['Consultorio Norte', 'Consultorio Centro', 'Consultorio Sur']:
        c, _ = Consultorio.objects.get_or_create(nombre=nombre, ubicacion=f"{nombre} - Planta 1")
        consultorios.append(c)
    print("✅ Consultorios creados.")

    # Crear médicos y asistentes sin consultorio asignado
    for i in range(3):
        User.objects.get_or_create(
            username=f'medico{i}',
            defaults={
                'email': f'medico{i}@clinic.com',
                'password': 'Medico123',
                'rol': 'medico',
                'first_name': f'Medico{i}',
                'last_name': 'Apellido',
                'is_staff': False,
            }
        )

        User.objects.get_or_create(
            username=f'asistente{i}',
            defaults={
                'email': f'asistente{i}@clinic.com',
                'password': 'Asistente123',
                'rol': 'asistente',
                'first_name': f'Asistente{i}',
                'last_name': 'Apellido',
                'is_staff': False,
            }
        )

    print("✅ Médicos y asistentes creados (sin consultorio asignado).")

    # Crear pacientes asignados a admin temporalmente
    medico_ref = User.objects.filter(rol='medico').first()
    asistente_ref = User.objects.filter(rol='asistente').first()

    pacientes = []
    for i in range(5):
        p = Paciente.objects.create(
            nombre_completo=f'Paciente {i} Pérez',
            fecha_nacimiento=datetime.date(1990+i, 5, 12),
            sexo=random.choice(['M', 'F']),
            telefono=f'66412345{i}',
            correo=f'paciente{i}@mail.com',
            direccion='Calle Falsa 123',
            historial_clinico='Sin antecedentes graves.',
            consultorio_asignado=admin
        )
        pacientes.append(p)

    print("✅ Pacientes creados.")

    # Crear consultas con signos vitales y recetas
    for paciente in pacientes:
        consulta = Consulta.objects.create(
            paciente=paciente,
            estado='finalizada',
            medico=medico_ref,
            asistente=asistente_ref,
            observaciones_finales='El paciente respondió bien al tratamiento.'
        )

        SignosVitales.objects.create(
            consulta=consulta,
            tension_arterial='120/80',
            frecuencia_cardiaca=72,
            frecuencia_respiratoria=18,
            temperatura=36.7,
            peso=70.0 + random.uniform(-5, 5),
            talla=1.70 + random.uniform(-0.1, 0.1),
            circunferencia_abdominal=85 + random.uniform(-5, 5),
            imc=24.2,
            alergias='Ninguna conocida',
            sintomas='Dolor de cabeza y fatiga'
        )

        Receta.objects.create(
            consulta=consulta,
            medico=medico_ref,
            direccion=paciente.direccion,
            medicamentos="Paracetamol 500mg cada 8 hrs por 5 días.\nIbuprofeno 400mg cada 12 hrs por 3 días.",
            indicaciones_adicionales='Tomar mucha agua y reposo.'
        )

    print("✅ Consultas completas generadas con signos y recetas.")


if __name__ == '__main__':
    run()
