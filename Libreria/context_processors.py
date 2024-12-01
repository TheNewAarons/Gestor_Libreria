#Se reviso que este metodo es de buen uso cuando se quiere usar parametros y mantenerlos en las demas plantillas que heredan de la app
def usuario_context(request):
    context = {} #Se crea un diccionario vacio para almacenar los datos del contexto que queremos manejar
    if request.user.is_authenticated:
        context['username'] = request.user.username # al contexto de username se le pasa mediante la requeste a nuestro usuario el username, para manejarlo 
        context['rol'] = request.user.rol  # aqui decimos que nuestro contexto de rol, le pasamos el request de nuestro usuario con su rol otorgado
    return context
