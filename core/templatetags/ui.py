from django import template

register = template.Library()


@register.filter
def bs(field):
    """Dibuja un campo de formulario con las clases de Bootstrap."""
    widget = field.field.widget
    tipo = getattr(widget, 'input_type', '')
    if tipo == 'checkbox':
        nueva = 'form-check-input'
    elif tipo == 'select':
        nueva = 'form-select'
    else:
        nueva = 'form-control'
    if field.errors:
        nueva += ' is-invalid'
    previa = widget.attrs.get('class', '')
    return field.as_widget(attrs={'class': f'{previa} {nueva}'.strip()})