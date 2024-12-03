from django.contrib.auth.views import LoginView
from .forms import FormularioPersonalizado

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # aseguramos de usar la plantilla correcta
    authentication_form = FormularioPersonalizado  # usamos el formulario personalizado para darle diseño a los inputs y mensajes de error