// Script mejorado para proteger campos readonly
    document.addEventListener('DOMContentLoaded', function() {
      
      // Función para proteger un campo
      function protegerCampo(field) {
        if (!field) return;
        
        // Agregar atributos de protección
        field.setAttribute('readonly', 'readonly');
        field.setAttribute('tabindex', '-1');
        field.classList.add('readonly-field');
        
        // Valor autorizado actual
        let valorAutorizado = field.value || '';
        
        // Método seguro para actualizar el valor
        field.actualizarValor = function(nuevoValor) {
          valorAutorizado = nuevoValor;
          this.value = nuevoValor;
          // Disparar evento change para compatibilidad
          this.dispatchEvent(new Event('change', { bubbles: true }));
        };
        
        // Prevenir eventos de modificación manual
        const eventos = ['keydown', 'keypress', 'keyup', 'input', 'paste', 'cut', 'drop', 'dragover'];
        eventos.forEach(evento => {
          field.addEventListener(evento, function(e) {
            // Permitir solo navegación con teclas
            if (evento === 'keydown' && ['Tab', 'ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) {
              return;
            }
            e.preventDefault();
            e.stopPropagation();
            return false;
          });
        });
        
        // Monitorear cambios no autorizados en el valor
        setInterval(function() {
          if (field.value !== valorAutorizado) {
            field.value = valorAutorizado;
          }
        }, 100);
        
        // Prevenir que se quite el atributo readonly
        const observer = new MutationObserver(function(mutations) {
          mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes') {
              if (mutation.attributeName === 'readonly' && !field.hasAttribute('readonly')) {
                field.setAttribute('readonly', 'readonly');
              }
              if (mutation.attributeName === 'class' && !field.classList.contains('readonly-field')) {
                field.classList.add('readonly-field');
              }
            }
          });
        });
        
        observer.observe(field, { 
          attributes: true, 
          attributeFilter: ['readonly', 'class'] 
        });
      }
      
      // Proteger campos después de un pequeño delay para asegurar que estén disponibles
      setTimeout(function() {
        const camposProtegidos = [
          'id_nombre', 'id_apellido', 'id_razon_social'
        ];
        
        camposProtegidos.forEach(id => {
          const campo = document.getElementById(id);
          if (campo) {
            protegerCampo(campo);
          }
        });
      }, 100);
    });