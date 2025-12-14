import qrcode
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings

class YapePlinPaymentService:
    """Servicio para gestionar pagos con Yape y Plin"""
    
    # Datos de merchant (reemplaza con tus datos reales)
    YAPE_MERCHANT_ID = getattr(settings, 'YAPE_MERCHANT_ID', 'tu_merchant_id_yape')
    PLIN_MERCHANT_ID = getattr(settings, 'PLIN_MERCHANT_ID', 'tu_merchant_id_plin')
    
    # Números para recibir pagos
    YAPE_NUMBER = getattr(settings, 'YAPE_NUMBER', '+51987654321')
    PLIN_NUMBER = getattr(settings, 'PLIN_NUMBER', '+51987654321')
    
    @staticmethod
    def generate_qr_code(transaction_id, amount, payment_method):
        """Genera código QR para Yape o Plin"""
        
        if payment_method == 'yape':
            # Formato Yape: yape://send?phone=XXXXXXXXX&amount=XXX
            qr_data = f"yape://send?phone={YapePlinPaymentService.YAPE_NUMBER}&amount={amount}&id={transaction_id}"
        else:  # plin
            # Formato Plin: plin://transfer?phone=XXXXXXXXX&amount=XXX
            qr_data = f"plin://transfer?phone={YapePlinPaymentService.PLIN_NUMBER}&amount={amount}&id={transaction_id}"
        
        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar en memoria
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return ContentFile(buffer.read(), name=f"{transaction_id}.png")
    
    @staticmethod
    def generate_payment_reference(transaction_id):
        """Genera un número de referencia único para el pago"""
        return transaction_id.replace('-', '')[:15].upper()
    
    @staticmethod
    def verify_payment(payment):
        """
        Verifica si el pago fue completado.
        En producción, integraría con APIs reales de Yape/Plin
        """
        # Aquí iría la integración real con APIs de Yape y Plin
        # Por ahora retornamos False, el usuario debe confirmar manualmente
        return False
