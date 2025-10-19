class LlamkayException(Exception):
    """Excepción base"""
    pass


class InvalidDNIException(LlamkayException):
    """DNI inválido"""
    pass


class InvalidRUCException(LlamkayException):
    """RUC inválido"""
    pass


class APIConnectionException(LlamkayException):
    """Error de API"""
    pass
