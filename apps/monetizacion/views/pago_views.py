from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from ..models import Plan, Subscription, Payment
from ..services.pago_service import YapePlinPaymentService
import uuid

@login_required
def planes_list(request):
    """Vista que muestra todos los planes disponibles"""
    planes = Plan.objects.all().order_by('price')
    suscripcion_actual = getattr(request.user, 'subscription', None)
    
    context = {
        'planes': planes,
        'suscripcion_actual': suscripcion_actual,
    }
    return render(request, 'monetizacion/planes_list.html', context)


@login_required
def plan_detail(request, plan_id):
    """Detalle del plan con opción de compra"""
    plan = get_object_or_404(Plan, id=plan_id)
    suscripcion_actual = getattr(request.user, 'subscription', None)
    
    context = {
        'plan': plan,
        'suscripcion_actual': suscripcion_actual,
    }
    return render(request, 'monetizacion/plan_detail.html', context)


@login_required
def elegir_metodo_pago(request, plan_id):
    """Mostrar opciones de método de pago"""
    plan = get_object_or_404(Plan, id=plan_id)
    
    if plan.price == 0:
        # Si es plan gratuito, procesar directamente
        return crear_pago_gratis(request, plan_id)
    
    context = {
        'plan': plan,
        'metodos_pago': [
            {'codigo': 'yape', 'nombre': 'Yape', 'icono': '📱'},
            {'codigo': 'plin', 'nombre': 'Plin', 'icono': '📲'},
        ]
    }
    return render(request, 'monetizacion/elegir_metodo_pago.html', context)


@login_required
def crear_pago_gratis(request, plan_id):
    """Crear suscripción para plan gratuito"""
    plan = get_object_or_404(Plan, id=plan_id)
    
    if plan.price != 0:
        return redirect('monetizacion:plan_detail', plan_id=plan.id)
    
    suscripcion, creada = Subscription.objects.get_or_create(
        user=request.user,
        defaults={
            'plan': plan,
            'status': 'active',
            'end_date': timezone.now() + timezone.timedelta(days=plan.duration_days),
        }
    )
    
    if not creada:
        suscripcion.plan = plan
        suscripcion.status = 'active'
        suscripcion.end_date = timezone.now() + timezone.timedelta(days=plan.duration_days)
        suscripcion.save()
    
    Payment.objects.create(
        user=request.user,
        plan=plan,
        subscription=suscripcion,
        amount=0,
        status='completed',
        payment_method='manual',
        transaction_id=f"free-{uuid.uuid4()}",
        completed_at=timezone.now(),
    )
    
    messages.success(request, f"¡Bienvenido al plan {plan.name}!")
    return redirect('monetizacion:suscripcion_exitosa')


@login_required
@require_http_methods(["POST"])
def procesar_pago_yape_plin(request, plan_id):
    """Procesar pago con Yape o Plin"""
    plan = get_object_or_404(Plan, id=plan_id)
    metodo_pago = request.POST.get('metodo_pago')
    
    if metodo_pago not in ['yape', 'plin']:
        messages.error(request, "Método de pago no válido")
        return redirect('monetizacion:elegir_metodo_pago', plan_id=plan.id)
    
    # Crear registro de pago
    transaction_id = f"{metodo_pago}-{uuid.uuid4()}"
    
    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=plan.price,
        status='pending',
        payment_method=metodo_pago,
        transaction_id=transaction_id,
        reference_number=YapePlinPaymentService.generate_payment_reference(transaction_id),
        expires_at=timezone.now() + timezone.timedelta(minutes=15)
    )
    
    # Generar código QR
    qr_code_file = YapePlinPaymentService.generate_qr_code(
        payment.reference_number,
        plan.price,
        metodo_pago
    )
    payment.qr_code.save(f"{transaction_id}.png", qr_code_file, save=True)
    
    context = {
        'payment': payment,
        'plan': plan,
        'metodo_pago': metodo_pago,
        'metodo_nombre': 'Yape' if metodo_pago == 'yape' else 'Plin',
    }
    return render(request, 'monetizacion/confirmar_pago_qr.html', context)


@login_required
def verificar_pago(request, payment_id):
    """Verifica si el pago fue completado"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    if payment.is_expired():
        return JsonResponse({
            'status': 'expired',
            'message': 'El tiempo para realizar el pago ha expirado'
        })
    
    # En producción, aquí iría verificación real con APIs de Yape/Plin
    # Por ahora, el usuario debe confirmar manualmente
    
    return JsonResponse({
        'status': payment.status,
        'time_remaining': payment.time_remaining(),
    })


@login_required
@require_http_methods(["POST"])
def confirmar_pago_manual(request, payment_id):
    """Confirmar que el usuario realizó el pago (método manual)"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    if payment.status != 'pending':
        messages.error(request, "Este pago ya fue procesado")
        return redirect('monetizacion:planes_list')
    
    if payment.is_expired():
        payment.status = 'failed'
        payment.save()
        messages.error(request, "El tiempo para realizar el pago expiró")
        return redirect('monetizacion:planes_list')
    
    # Marcar como completado (en producción verificarías con la API real)
    payment.status = 'completed'
    payment.completed_at = timezone.now()
    payment.save()
    
    # Crear suscripción
    suscripcion, _ = Subscription.objects.get_or_create(
        user=request.user,
        defaults={
            'plan': payment.plan,
            'status': 'active',
            'end_date': timezone.now() + timezone.timedelta(days=payment.plan.duration_days),
        }
    )
    
    if suscripcion.subscription:
        suscripcion.subscription = payment
    suscripcion.save()
    payment.subscription = suscripcion
    payment.save()
    
    messages.success(request, "¡Pago confirmado! Tu suscripción está activa")
    return redirect('monetizacion:suscripcion_exitosa')


@login_required
def pago_exitoso(request):
    """Página de éxito del pago"""
    return render(request, 'monetizacion/pago_exitoso.html')


@login_required
def pago_cancelado(request):
    """Página de cancelación del pago"""
    return render(request, 'monetizacion/pago_cancelado.html')


@login_required
def suscripcion_detalle(request):
    """Ver detalles de la suscripción actual"""
    suscripcion = getattr(request.user, 'subscription', None)
    
    if not suscripcion:
        return redirect('monetizacion:planes_list')
    
    context = {
        'suscripcion': suscripcion,
        'esta_activa': suscripcion.is_active(),
        'dias_restantes': suscripcion.days_remaining(),
    }
    return render(request, 'monetizacion/suscripcion_detalle.html', context)


@login_required
def suscripcion_exitosa(request):
    """Página de éxito de suscripción"""
    suscripcion = getattr(request.user, 'subscription', None)
    context = {'suscripcion': suscripcion}
    return render(request, 'monetizacion/suscripcion_exitosa.html', context)