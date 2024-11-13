from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'Libreria/Home.html')

def base(request):
    return render(request, 'Libreria/Base_Modulos.html')
