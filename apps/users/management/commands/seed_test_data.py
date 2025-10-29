# apps/management/commands/seed_test_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta

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
            ('pedro.silva', 'pedro@llamkay.com', 'Pedro', 'Silva', '55556666', 'trabajador'),
            ('laura.martin', 'laura@empresa.com', 'Laura', 'Martín', '77778888', 'empleador'),
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

            telefono = '9' + ''.join(random.choices('0123456789', k=8))
            usuario, _ = Usuario.objects.get_or_create(
                user=user,
                defaults={
                    'email': email, 'nombres': nombres, 'apellidos': apellidos,
                    'dni': dni, 'tipo_usuario': tipo, 'telefono': telefono
                }
            )
            usuarios.append(usuario)

        # ===================================================================
        # 2. UBICACIÓN (4+ por tabla)
        # ===================================================================
        dept_lima, _ = Departamento.objects.get_or_create(nombre='Lima', defaults={'codigo': '15'})
        dept_arequipa, _ = Departamento.objects.get_or_create(nombre='Arequipa', defaults={'codigo': '04'})
        dept_cusco, _ = Departamento.objects.get_or_create(nombre='Cusco', defaults={'codigo': '08'})
        dept_piura, _ = Departamento.objects.get_or_create(nombre='Piura', defaults={'codigo': '20'})

        prov_lima, _ = Provincia.objects.get_or_create(id_departamento=dept_lima, nombre='Lima', defaults={'codigo': '01'})
        prov_arequipa, _ = Provincia.objects.get_or_create(id_departamento=dept_arequipa, nombre='Arequipa', defaults={'codigo': '01'})
        prov_cusco, _ = Provincia.objects.get_or_create(id_departamento=dept_cusco, nombre='Cusco', defaults={'codigo': '01'})
        prov_piura, _ = Provincia.objects.get_or_create(id_departamento=dept_piura, nombre='Piura', defaults={'codigo': '01'})

        dist_miraflores, _ = Distrito.objects.get_or_create(id_provincia=prov_lima, nombre='Miraflores', defaults={'codigo': '18'})
        dist_sanisidro, _ = Distrito.objects.get_or_create(id_provincia=prov_lima, nombre='San Isidro', defaults={'codigo': '30'})
        dist_arequipa, _ = Distrito.objects.get_or_create(id_provincia=prov_arequipa, nombre='Arequipa', defaults={'codigo': '01'})
        dist_cusco, _ = Distrito.objects.get_or_create(id_provincia=prov_cusco, nombre='Cusco', defaults={'codigo': '01'})

        Comunidad.objects.get_or_create(
            id_distrito=dist_miraflores, nombre='Miraflores Centro',
            defaults={'latitud': -12.1215, 'longitud': -77.0304}
        )
        Comunidad.objects.get_or_create(
            id_distrito=dist_sanisidro, nombre='San Isidro Financiero',
            defaults={'latitud': -12.0970, 'longitud': -77.0330}
        )
        Comunidad.objects.get_or_create(
            id_distrito=dist_arequipa, nombre='Cayma',
            defaults={'latitud': -16.3887, 'longitud': -71.5350}
        )
        Comunidad.objects.get_or_create(
            id_distrito=dist_cusco, nombre='Centro Histórico',
            defaults={'latitud': -13.5171, 'longitud': -71.9781}
        )

        # ===================================================================
        # 3. CATEGORÍAS Y HABILIDADES (4+)
        # ===================================================================
        categorias = [
            ('Electricista', 'electricista', 'zap'),
            ('Plomero', 'plomero', 'droplet'),
            ('Albañil', 'albanil', 'hammer'),
            ('Pintor', 'pintor', 'paintbrush'),
            ('Jardinero', 'jardinero', 'leaf'),
            ('Carpintero', 'carpintero', 'tool'),
        ]
        cats = []
        for nombre, slug, icono in categorias:
            cat, _ = CategoriaTrabajo.objects.get_or_create(nombre=nombre, defaults={'slug': slug, 'icono': icono})
            cats.append(cat)

        habilidades = ['Cableado', 'Tuberías', 'Drywall', 'Pintura', 'Jardinería', 'Madera', 'Soldadura', 'Instalación']
        habs = []
        for nombre in habilidades:
            hab, _ = Habilidad.objects.get_or_create(nombre=nombre)
            habs.append(hab)

        # ===================================================================
        # 4. PERFILES Y ESTADÍSTICAS (4+)
        # ===================================================================
        distritos = [dist_miraflores, dist_sanisidro, dist_arequipa, dist_cusco]
        for i, usuario in enumerate(usuarios):
            Profile.objects.get_or_create(
                id_usuario=usuario,
                defaults={
                    'bio': f"Profesional con {i+3} años de experiencia en {random.choice(categorias)[0]}.",
                    'ocupacion': random.choice(categorias)[0],
                    'experiencia_anios': i + 2,
                    'tarifa_hora': Decimal('30.00') + Decimal(str(i * 5)) if usuario.tipo_usuario in ['trabajador', 'ambos'] else None,
                    'foto_url': f"/media/fotos/{usuario.user.username}.jpg",
                    'portafolio_url': f"https://portafolio-{usuario.user.username}.com",
                    'id_departamento': dept_lima if i < 4 else dept_arequipa,
                    'id_provincia': prov_lima if i < 4 else prov_arequipa,
                    'id_distrito': random.choice(distritos),
                    'perfil_publico': True,
                    'mostrar_email': i % 2 == 0,
                    'mostrar_telefono': i % 3 == 0,
                }
            )
            UsuarioEstadisticas.objects.get_or_create(
                id_usuario=usuario,
                defaults={
                    'rating_promedio': round(random.uniform(3.5, 5.0), 2),
                    'total_calificaciones': random.randint(0, 50),
                    'trabajos_completados': random.randint(0, 30),
                    'trabajos_activos': random.randint(0, 5),
                    'trabajos_cancelados': random.randint(0, 3),
                    'ingresos_totales': Decimal(str(round(random.uniform(500, 10000), 2))),
                }
            )

        # ===================================================================
        # 5. DISPONIBILIDAD (solo trabajadores, 4+ por usuario)
        # ===================================================================
        dias_trabajo = [1, 2, 3, 4, 5]
        for usuario in usuarios:
            if usuario.tipo_usuario in ['trabajador', 'ambos']:
                for dia in dias_trabajo:
                    Disponibilidad.objects.get_or_create(
                        id_trabajador=usuario, dia_semana=dia,
                        hora_inicio='08:00:00', hora_fin='17:00:00'
                    )
                # Agregar fin de semana para algunos
                if random.choice([True, False]):
                    Disponibilidad.objects.get_or_create(
                        id_trabajador=usuario, dia_semana=6,
                        hora_inicio='09:00:00', hora_fin='13:00:00'
                    )

        # ===================================================================
        # 6. OFERTAS (4+ por tipo)
        # ===================================================================
        ofertas_usuario = []
        for i in range(5):
            oferta, _ = OfertaUsuario.objects.get_or_create(
                id_empleador=usuarios[1],  # María
                titulo=f"Instalación eléctrica {i+1}",
                defaults={
                    'id_categoria': cats[0],
                    'descripcion': f"Trabajo de {i+1} días en Miraflores. Urgente." if i < 2 else f"Trabajo en {distritos[i%4].nombre}.",
                    'modalidad_pago': random.choice(['por_proyecto', 'por_hora', 'por_dia']),
                    'pago': Decimal('500.00') + Decimal(str(i * 100)),
                    'id_distrito': distritos[i % 4],
                    'estado': 'activa' if i < 3 else 'cerrada',
                    'urgente': i < 2,
                }
            )
            ofertas_usuario.append(oferta)

        ofertas_empresa = []
        for i in range(5):
            oferta, _ = OfertaEmpresa.objects.get_or_create(
                id_empleador=usuarios[1],
                titulo_puesto=f"Puesto de {cats[i%4].nombre} {i+1}",
                defaults={
                    'id_categoria': cats[i % 4],
                    'descripcion': f"Contrato mensual en {distritos[i%4].nombre}.",
                    'modalidad_pago': 'mensual',
                    'pago': Decimal('2800.00') + Decimal(str(i * 200)),
                    'id_distrito': distritos[i % 4],
                    'estado': 'activa',
                    'experiencia_requerida': f"{i+1} años",
                    'vacantes': random.randint(1, 3),
                }
            )
            ofertas_empresa.append(oferta)

        # ===================================================================
        # 7. POSTULACIONES (4+)
        # ===================================================================
        for i, oferta in enumerate(ofertas_usuario[:4]):
            Postulacion.objects.get_or_create(
                id_trabajador=usuarios[0],  # Juan
                id_oferta_usuario=oferta,
                defaults={
                    'mensaje': f"Postulación #{i+1} - Disponible de inmediato.",
                    'pretension_salarial': Decimal('450.00') + Decimal(str(i * 50)),
                    'estado': 'aceptada' if i == 0 else 'pendiente',
                    'disponibilidad_inmediata': i % 2 == 0,
                }
            )

        for i, oferta in enumerate(ofertas_empresa[:4]):
            Postulacion.objects.get_or_create(
                id_trabajador=usuarios[2],  # Carlos
                id_oferta_empresa=oferta,
                defaults={
                    'mensaje': f"Me interesa el puesto #{i+1}",
                    'pretension_salarial': Decimal('3000.00'),
                    'estado': 'en_revision' if i == 0 else 'pendiente',
                }
            )

        # ===================================================================
        # 8. CONTRATOS Y PAGOS (4+)
        # ===================================================================
        postulacion_aceptada = Postulacion.objects.filter(estado='aceptada').first()
        if postulacion_aceptada:
            contratos = []
            for i in range(4):
                contrato, _ = Contrato.objects.get_or_create(
                    id_empleador=usuarios[1],
                    id_trabajador=usuarios[0],
                    titulo=f"Instalación eléctrica completa #{i+1}",
                    defaults={
                        'id_postulacion': postulacion_aceptada if i == 0 else None,
                        'precio_acordado': Decimal('550.00') + Decimal(str(i * 100)),
                        'estado': 'completado' if i < 2 else 'activo',
                        'fecha_inicio': timezone.now().date() - timedelta(days=10 - i),
                    }
                )
                contratos.append(contrato)

            for i, contrato in enumerate(contratos):
                Pago.objects.get_or_create(
                    id_contrato=contrato,
                    defaults={
                        'monto_total': contrato.precio_acordado,
                        'monto_trabajador': contrato.precio_acordado * Decimal('0.9'),
                        'comision': contrato.precio_acordado * Decimal('0.1'),
                        'estado': 'completado' if i < 2 else 'pendiente',
                    }
                )

        # ===================================================================
        # 9. CALIFICACIONES (4+)
        # ===================================================================
        for contrato in Contrato.objects.all()[:4]:
            Calificacion.objects.get_or_create(
                id_contrato=contrato, id_autor=usuarios[1], id_receptor=usuarios[0],
                defaults={'puntuacion': random.choice([4, 5]), 'comentario': 'Excelente trabajo'}
            )
            Calificacion.objects.get_or_create(
                id_contrato=contrato, id_autor=usuarios[0], id_receptor=usuarios[1],
                defaults={'puntuacion': random.choice([4, 5]), 'comentario': 'Pago puntual'}
            )

        # ===================================================================
        # 10. CHATS Y MENSAJES (4+ mensajes)
        # ===================================================================
        conversacion, _ = Conversacion.objects.get_or_create(
            id_usuario_1=usuarios[0], id_usuario_2=usuarios[1],
            defaults={'id_oferta_usuario': ofertas_usuario[0]}
        )
        mensajes_data = [
            ("Hola, ¿cuándo puedes empezar?", 'texto', None),
            ("Mañana a las 9am", 'texto', None),
            ("Aquí el plano", 'imagen', '/media/plano.jpg'),
            ("Perfecto, gracias", 'texto', None),
            ("¿Traes herramientas?", 'texto', None),
            ("Sí, todo completo", 'texto', None),
        ]
        for contenido, tipo, archivo in mensajes_data:
            Mensaje.objects.get_or_create(
                id_conversacion=conversacion,
                id_remitente=usuarios[0] if mensajes_data.index((contenido, tipo, archivo)) % 2 == 0 else usuarios[1],
                tipo=tipo,
                defaults={'contenido': contenido, 'archivo': archivo, 'leido': True}
            )

        # ===================================================================
        # 11. SOPORTE (4+ denuncias y notificaciones)
        # ===================================================================
        Denuncia.objects.get_or_create(
            id_reportante=usuarios[2], id_denunciado=usuarios[0],
            motivo='spam', descripcion='Envía muchos mensajes',
            defaults={'estado': 'pendiente'}
        )
        Denuncia.objects.get_or_create(
            id_reportante=usuarios[4], id_denunciado=usuarios[1],
            motivo='acoso', descripcion='Insistencia excesiva',
            defaults={'estado': 'en_revision'}
        )
        Denuncia.objects.get_or_create(
            id_reportante=usuarios[3], id_denunciado=usuarios[5],
            motivo='fraude', descripcion='No pagó',
            defaults={'estado': 'resuelta'}
        )
        Denuncia.objects.get_or_create(
            id_reportante=usuarios[0], id_denunciado=usuarios[2],
            motivo='otro', descripcion='Mal comportamiento',
            defaults={'estado': 'cerrada'}
        )

        Notificacion.objects.get_or_create(
            id_usuario=usuarios[0], tipo='postulacion', titulo='¡Postulación aceptada!',
            defaults={'mensaje': 'María aceptó tu postulación.', 'url': '/postulaciones/1/'}
        )
        Notificacion.objects.get_or_create(
            id_usuario=usuarios[1], tipo='mensaje', titulo='Nuevo mensaje',
            defaults={'mensaje': 'Juan te escribió.', 'url': '/chat/1/'}
        )
        Notificacion.objects.get_or_create(
            id_usuario=usuarios[0], tipo='pago', titulo='Pago recibido',
            defaults={'mensaje': 'Recibiste S/500.00', 'url': '/pagos/1/'}
        )
        Notificacion.objects.get_or_create(
            id_usuario=usuarios[2], tipo='sistema', titulo='Bienvenido',
            defaults={'mensaje': 'Gracias por unirte a Llamkay.', 'url': '/perfil/'}
        )

        # ===================================================================
        # 12. HABILIDADES Y CERTIFICACIONES (4+)
        # ===================================================================
        for usuario in usuarios[:4]:
            for hab in habs[:3]:
                UsuarioHabilidad.objects.get_or_create(
                    id_usuario=usuario, id_habilidad=hab,
                    defaults={'nivel': random.choice(['intermedio', 'avanzado', 'experto']), 'anios_experiencia': random.randint(1, 12)}
                )

        Certificacion.objects.get_or_create(
            id_usuario=usuarios[0], titulo='SENATI Electricidad',
            defaults={'institucion': 'SENATI', 'verificada': True, 'fecha_obtencion': timezone.now().date() - timedelta(days=365)}
        )
        Certificacion.objects.get_or_create(
            id_usuario=usuarios[0], titulo='Certificación OSHA',
            defaults={'institucion': 'OSHA', 'verificada': True}
        )
        Certificacion.objects.get_or_create(
            id_usuario=usuarios[2], titulo='Curso de Albañilería',
            defaults={'institucion': 'SENCICO', 'verificada': False}
        )
        Certificacion.objects.get_or_create(
            id_usuario=usuarios[4], titulo='Jardinería Profesional',
            defaults={'institucion': 'INIA', 'verificada': True}
        )

        # ===================================================================
        # 13. TRABAJOS GUARDADOS (4+)
        # ===================================================================
        for i, usuario in enumerate(usuarios[:4]):
            GuardarTrabajo.objects.get_or_create(
                id_usuario=usuario,
                id_oferta_usuario=ofertas_usuario[i % len(ofertas_usuario)]
            )
            GuardarTrabajo.objects.get_or_create(
                id_usuario=usuario,
                id_oferta_empresa=ofertas_empresa[i % len(ofertas_empresa)]
            )

        # ===================================================================
        # FINAL
        # ===================================================================
        self.stdout.write(self.style.SUCCESS("¡Datos de prueba cargados con éxito! (4+ por tabla)"))