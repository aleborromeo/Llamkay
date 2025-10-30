from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid

class Plan(models.Model):
    PLAN_TYPES = (
        ('free', 'Gratis'),
        ('premium', 'Premium'),
        ('empresa', 'Empresa'),
    )
    
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration_days = models.IntegerField(default=30)
    
    # Características del plan
    max_applications_per_day = models.IntegerField(default=4)
    can_edit_profile = models.BooleanField(default=True)
    can_create_jobs = models.BooleanField(default=False)
    job_creation_limit = models.IntegerField(default=0)
    location_restriction = models.CharField(
        max_length=50, 
        default='same_city',
        choices=[('same_city', 'Misma ciudad'), ('all_cities', 'Todas las ciudades')]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'soporte'
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('cancelled', 'Cancelado'),
        ('expired', 'Expirado'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    renewal_date = models.DateTimeField(null=True, blank=True)
    
    applications_used_today = models.IntegerField(default=0)
    last_reset = models.DateField(auto_now_add=True)
    
    jobs_created = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'soporte'
        verbose_name = 'Suscripción'
        verbose_name_plural = 'Suscripciones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    def is_active(self):
        return self.status == 'active' and timezone.now() < self.end_date
    
    def is_expired(self):
        if timezone.now() > self.end_date:
            self.status = 'expired'
            self.save()
            return True
        return False
    
    def days_remaining(self):
        if self.is_active():
            return (self.end_date - timezone.now()).days
        return 0
    
    def reset_daily_counter(self):
        today = timezone.now().date()
        if self.last_reset < today:
            self.applications_used_today = 0
            self.last_reset = today
            self.save()
    
    def can_apply_for_job(self):
        if not self.is_active():
            return False
        self.reset_daily_counter()
        if self.plan.max_applications_per_day == -1:
            return True
        return self.applications_used_today < self.plan.max_applications_per_day
    
    def increment_application_count(self):
        if self.can_apply_for_job():
            self.reset_daily_counter()
            self.applications_used_today += 1
            self.save()
            return True
        return False
    
    def can_create_job(self):
        if not self.is_active() or not self.plan.can_create_jobs:
            return False
        if self.plan.job_creation_limit == -1:
            return True
        return self.jobs_created < self.plan.job_creation_limit


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    )
    
    PAYMENT_METHOD = (
        ('yape', 'Yape'),
        ('plin', 'Plin'),
        ('manual', 'Transferencia Manual'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    
    transaction_id = models.CharField(max_length=255, unique=True, db_index=True)
    reference_number = models.CharField(max_length=100, blank=True, help_text="Número de referencia Yape/Plin")
    
    # Para QR dinámicos
    qr_code = models.ImageField(upload_to='payments/qr/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Tiempo de expiración del pago")
    
    notes = models.TextField(blank=True)
    
    class Meta:
        app_label = 'soporte'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pago {self.transaction_id} - {self.user.username} - ${self.amount}"
    
    def is_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            self.status = 'failed'
            self.save()
            return True
        return False
    
    def time_remaining(self):
        """Retorna tiempo restante en minutos"""
        if self.expires_at:
            remaining = (self.expires_at - timezone.now()).total_seconds() / 60
            return max(0, int(remaining))
        return 0