# apps/management/commands/seed_test_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from apps.monetizacion.models import Plan
import random

# === IMPORTA TUS MODELOS ===
from apps.users.models import (
    Usuario, Departamento, Provincia, Distrito, Comunidad,
    CategoriaTrabajo, Habilidad, UsuarioHabilidad, UsuarioCategoria,
    Profile, UsuarioEstadisticas, Disponibilidad,
    Verificacion, Certificacion, TrabajosRealizados
)
from apps.jobs.models import (
    OfertaUsuario, OfertaEmpresa, Postulacion, Contrato, Pago, Calificacion, GuardarTrabajo
)
from apps.chats.models import Conversacion, Mensaje
from apps.soporte.models import Denuncia, Notificacion


class Command(BaseCommand):
    help = 'Carga datos de prueba (4+ por tabla, sin duplicados)'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando carga de datos de prueba...")

        # ===================================================================
        # 1. USUARIOS + PERFILES
        # ===================================================================
        users_data = [
            ('juanperez', 'juan@llamkay.com', 'Juan', 'Pérez', '12345678', 'trabajador'),
            ('maria.gomez', 'maria@empresa.com', 'María', 'Gómez', '87654321', 'empleador'),
            ('carlos.lopez', 'carlos@llamkay.com', 'Carlos', 'López', '11223344', 'trabajador'),
            ('ana.rodriguez', 'ana@llamkay.com', 'Ana', 'Rodríguez', '99887766', 'ambos'),
        ]

        usuarios = []
        for username, email, nombres, apellidos, dni, tipo in users_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'is_active': True}
            )
            if not user.check_password('test123'):
                user.set_password('test123')
                user.save()

            usuario, _ = Usuario.objects.get_or_create(
                user=user,
                defaults={
                    'email': email, 'nombres': nombres, 'apellidos': apellidos,
                    'dni': dni, 'tipo_usuario': tipo, 'telefono': '9' + str(random.randint(10000000, 99999999))
                }
            )
            usuarios.append(usuario)

        # ===================================================================
        # 2. UBICACIÓN
        # ===================================================================
        dept_lima, _ = Departamento.objects.get_or_create(nombre='Lima', defaults={'codigo': '15'})
        prov_lima, _ = Provincia.objects.get_or_create(id_departamento=dept_lima, nombre='Lima', defaults={'codigo': '01'})
        dist_miraflores, _ = Distrito.objects.get_or_create(id_provincia=prov_lima, nombre='Miraflores', defaults={'codigo': '18'})
        dist_sanisidro, _ = Distrito.objects.get_or_create(id_provincia=prov_lima, nombre='San Isidro', defaults={'codigo': '30'})

        Comunidad.objects.get_or_create(
            id_distrito=dist_miraflores, nombre='Miraflores Centro',
            defaults={'latitud': -12.1215, 'longitud': -77.0304}
        )
        Comunidad.objects.get_or_create(
            id_distrito=dist_sanisidro, nombre='San Isidro Financiero',
            defaults={'latitud': -12.0970, 'longitud': -77.0330}
        )

        # ===================================================================
        # 3. CATEGORÍAS Y HABILIDADES
        # ===================================================================
        categorias = [
            ('Electricista', 'electricista', 'zap'),
            ('Plomero', 'plomero', 'droplet'),
            ('Albañil', 'albanil', 'hammer'),
            ('Pintor', 'pintor', 'paintbrush'),
        ]
        cats = []
        for nombre, slug, icono in categorias:
            cat, _ = CategoriaTrabajo.objects.get_or_create(nombre=nombre, defaults={'slug': slug, 'icono': icono})
            cats.append(cat)

        habilidades = ['Cableado', 'Tuberías', 'Drywall', 'Pintura', 'Jardinería']
        habs = []
        for nombre in habilidades:
            hab, _ = Habilidad.objects.get_or_create(nombre=nombre)
            habs.append(hab)

        # ===================================================================
        # 4. PERFILES Y ESTADÍSTICAS
        # ===================================================================
        for i, usuario in enumerate(usuarios):
            Profile.objects.get_or_create(
                id_usuario=usuario,
                defaults={
                    'bio': f"Profesional con {i+3} años de experiencia.",
                    'tarifa_hora': Decimal('35.00') if usuario.tipo_usuario in ['trabajador', 'ambos'] else None,
                    'id_distrito': dist_miraflores if i % 2 == 0 else dist_sanisidro
                }
            )
            UsuarioEstadisticas.objects.get_or_create(
                id_usuario=usuario,
                defaults={'rating_promedio': round(random.uniform(3.5, 5.0), 2)}
            )

        # ===================================================================
        # 5. DISPONIBILIDAD (solo trabajadores)
        # ===================================================================
        for usuario in usuarios:
            if usuario.tipo_usuario in ['trabajador', 'ambos']:
                for dia in [1, 2, 3, 4, 5]:
                    Disponibilidad.objects.get_or_create(
                        id_trabajador=usuario, dia_semana=dia,
                        hora_inicio='08:00:00', hora_fin='17:00:00'
                    )

        # ===================================================================
        # 6. OFERTAS
        # ===================================================================
        ofertas_usuario = []
        for i in range(4):
            oferta, _ = OfertaUsuario.objects.get_or_create(
                id_empleador=usuarios[1],  # María
                titulo=f"Instalación eléctrica {i+1}",
                defaults={
                    'id_categoria': cats[0],
                    'descripcion': f"Trabajo de {i+1} días en Miraflores.",
                    'modalidad_pago': 'por_proyecto',
                    'pago': Decimal('600.00'),
                    'id_distrito': dist_miraflores,
                    'estado': 'activa' if i < 2 else 'cerrada'
                }
            )
            ofertas_usuario.append(oferta)

        ofertas_empresa = []
        for i in range(4):
            oferta, _ = OfertaEmpresa.objects.get_or_create(
                id_empleador=usuarios[1],
                titulo_puesto=f"Puesto de plomero {i+1}",
                defaults={
                    'id_categoria': cats[1],
                    'descripcion': f"Contrato mensual en San Isidro.",
                    'modalidad_pago': 'mensual',
                    'pago': Decimal('3000.00'),
                    'id_distrito': dist_sanisidro,
                    'estado': 'activa'
                }
            )
            ofertas_empresa.append(oferta)

        # ===================================================================
        # 7. POSTULACIONES
        # ===================================================================
        for i, oferta in enumerate(ofertas_usuario[:3]):
            Postulacion.objects.get_or_create(
                id_trabajador=usuarios[0],  # Juan
                id_oferta_usuario=oferta,
                defaults={
                    'mensaje': f"Postulación #{i+1}",
                    'pretension_salarial': Decimal('550.00'),
                    'estado': 'aceptada' if i == 0 else 'pendiente'
                }
            )

        # ===================================================================
        # 8. CONTRATOS Y PAGOS
        # ===================================================================
        postulacion_aceptada = Postulacion.objects.filter(estado='aceptada').first()
        if postulacion_aceptada:
            contrato, _ = Contrato.objects.get_or_create(
                id_empleador=usuarios[1],
                id_trabajador=usuarios[0],
                titulo="Instalación eléctrica completa",
                defaults={
                    'id_postulacion': postulacion_aceptada,
                    'precio_acordado': Decimal('550.00'),
                    'estado': 'activo'
                }
            )
            Pago.objects.get_or_create(
                id_contrato=contrato,
                defaults={
                    'monto_total': Decimal('550.00'),
                    'monto_trabajador': Decimal('500.00'),
                    'comision': Decimal('50.00'),
                    'estado': 'completado'
                }
            )

        # ===================================================================
        # 9. CALIFICACIONES
        # ===================================================================
        contrato = Contrato.objects.first()
        if contrato:
            Calificacion.objects.get_or_create(
                id_contrato=contrato, id_autor=usuarios[1], id_receptor=usuarios[0],
                defaults={'puntuacion': 5, 'comentario': 'Excelente trabajo'}
            )
            Calificacion.objects.get_or_create(
                id_contrato=contrato, id_autor=usuarios[0], id_receptor=usuarios[1],
                defaults={'puntuacion': 5, 'comentario': 'Pago puntual'}
            )

        # ===================================================================
        # 10. CHATS Y MENSAJES
        # ===================================================================
        conversacion, _ = Conversacion.objects.get_or_create(
            id_usuario_1=usuarios[0], id_usuario_2=usuarios[1],
            defaults={'id_oferta_usuario': ofertas_usuario[0]}
        )
        mensajes = [
            ("Hola, ¿cuándo puedes empezar?", 'texto', None),
            ("Mañana a las 9am", 'texto', None),
            ("Aquí el plano", 'imagen', '/media/plano.jpg'),
            ("Perfecto, gracias", 'texto', None),
        ]
        for contenido, tipo, archivo in mensajes:
            Mensaje.objects.get_or_create(
                id_conversacion=conversacion,
                id_remitente=usuarios[0] if mensajes.index((contenido, tipo, archivo)) % 2 == 0 else usuarios[1],
                tipo=tipo,
                defaults={'contenido': contenido, 'archivo': archivo, 'leido': True}
            )

        # ===================================================================
        # 11. SOPORTE
        # ===================================================================
        Denuncia.objects.get_or_create(
            id_reportante=usuarios[2], id_denunciado=usuarios[0],
            motivo='spam', descripcion='Envía muchos mensajes',
            defaults={'estado': 'pendiente'}
        )

        Notificacion.objects.get_or_create(
            id_usuario=usuarios[0], tipo='postulacion', titulo='¡Postulación aceptada!',
            defaults={'mensaje': 'María aceptó tu postulación.', 'url': '/postulaciones/1/'}
        )

        # ===================================================================
        # 12. HABILIDADES Y CERTIFICACIONES
        # ===================================================================
        for usuario in usuarios[:3]:
            for hab in habs[:2]:
                UsuarioHabilidad.objects.get_or_create(
                    id_usuario=usuario, id_habilidad=hab,
                    defaults={'nivel': random.choice(['intermedio', 'avanzado']), 'anios_experiencia': random.randint(1, 10)}
                )

        Certificacion.objects.get_or_create(
            id_usuario=usuarios[0], titulo='SENATI Electricidad',
            defaults={'institucion': 'SENATI', 'verificada': True}
        )

        # ===================================================================
        # FINAL
        # ===================================================================
        self.stdout.write(self.style.SUCCESS("¡Datos de prueba cargados con éxito! (4+ por tabla)"))
    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Eliminar planes existentes (opcional)
        Plan.objects.all().delete()
        
        # Crear planes
        planes = [
            {
                'plan_type': 'free',
                'name': 'Básico',
                'description': 'Perfecto para comenzar tu búsqueda de empleo',
                'price': 0,
                'duration_days': 30,
                'max_applications_per_day': 4,
                'can_edit_profile': True,
                'can_create_jobs': False,
                'job_creation_limit': 0,
                'location_restriction': 'same_city',
            },
            {
                'plan_type': 'premium',
                'name': 'Premium',
                'description': 'Para los que buscan oportunidades sin límites',
                'price': 9.99,
                'duration_days': 30,
                'max_applications_per_day': -1,  # Ilimitado
                'can_edit_profile': True,
                'can_create_jobs': False,
                'job_creation_limit': 0,
                'location_restriction': 'all_cities',
            },
            {
                'plan_type': 'empresa',
                'name': 'Empresa',
                'description': 'Solución completa para empresas que contratan',
                'price': 29.99,
                'duration_days': 30,
                'max_applications_per_day': 0,
                'can_edit_profile': True,
                'can_create_jobs': True,
                'job_creation_limit': -1,  # Ilimitado
                'location_restriction': 'all_cities',
            },
        ]
        
        for plan_data in planes:
            plan, created = Plan.objects.get_or_create(
                plan_type=plan_data['plan_type'],
                defaults=plan_data
            )
            status = "✓ Creado" if created else "✗ Ya existe"
            self.stdout.write(
                self.style.SUCCESS(f"{status}: {plan.name}")
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Datos de prueba cargados correctamente')
        )