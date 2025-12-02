from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    """Widget personalizado para subir múltiples archivos"""
    allow_multiple_selected = True
    
    def value_from_datadict(self, data, files, name):
        """Maneja múltiples archivos"""
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)