import os
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Libros.models import Libro
from Usuarios.models import Users
from Editoriales.models import Editorial
from django.core.exceptions import ObjectDoesNotExist

def importar_productos(request):
    if request.method == 'POST' and request.FILES['file']:
        # Obtener el archivo subido
        file = request.FILES['file']

        # Crear el directorio 'excels' si no existe
        excel_dir = os.path.join('media', 'excels')
        if not os.path.exists(excel_dir):
            os.makedirs(excel_dir)

        # Guardar el archivo en la carpeta 'media/excels'
        file_path = os.path.join(excel_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Leer el archivo Excel
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            return HttpResponse(f"Error al leer el archivo: {e}")

        # Verifica las primeras filas para asegurarse de que los datos se están leyendo correctamente
        print(df.head())  # Imprime las primeras filas del DataFrame para depurar

        # Procesar los datos del archivo Excel
        for index, row in df.iterrows():
            try:
                # Obtener autor
                username = row['username']
                try:
                    author = Users.objects.get(username=username, rol='author')  # Asegúrate de que el rol sea 'author'
                except ObjectDoesNotExist:
                    print(f"Autor no encontrado o no tiene rol de autor para: {username}")
                    continue  # Saltar si el autor no existe o no es autor

                # Obtener editorial
                editorial_name = row['editorial']
                try:
                    editorial = Editorial.objects.get(name=editorial_name)  # Buscar por nombre
                except ObjectDoesNotExist:
                    print(f"Editorial no encontrada para: {editorial_name}")
                    continue  # Saltar si la editorial no existe

                # Crear el libro
                libro = Libro(
                    title=row['title'],
                    tipo=row['tipo'],
                    tamaño=row['tamaño'],
                    editorial=editorial,
                    author=author,
                    description=row['description']
                )
                
                # Guardar el libro en la base de datos
                libro.save()
                print(f"Libro importado: {row['title']}")

            except Exception as e:
                print(f"Error en la fila {index}: {e}")
                continue  # Saltar fila si ocurre un error

        # Redirigir a la página base después de importar
        return redirect('importar_productos')  # Cambiar 'base' por el nombre de la URL de destino

    return render(request, 'ImportarProductos/importar.html')
