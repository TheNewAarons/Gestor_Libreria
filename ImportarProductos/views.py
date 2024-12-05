import os
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from Libros.models import Libro
from Usuarios.models import Users
from Editoriales.models import Editorial
from django.core.exceptions import ObjectDoesNotExist
from .forms import ImportarProductosForm
from django.contrib.auth.hashers import make_password

def importar_productos(request):
    if request.method == 'POST':
        form = ImportarProductosForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['archivo']
                df = pd.read_excel(excel_file)

                exitosos = 0
                fallidos = 0
                errores = []
                autores_creados = 0
                editoriales_creadas = 0

                # Procesar cada fila del Excel
                for index, row in df.iterrows():
                    try:
                        # Validar campos requeridos
                        required_fields = ['title', 'tipo', 'tamaño', 'editorial', 'username', 'description']
                        if not all(field in row for field in required_fields):
                            raise ValueError(f"Faltan campos requeridos en la fila {index + 2}")

                        # Buscar o crear autor
                        try:
                            author = Users.objects.get(username=row['username'])
                            if author.rol != 'author':
                                author.rol = 'author'
                                author.save()
                        except Users.DoesNotExist:
                            # Crear nuevo autor
                            author = Users.objects.create(
                                username=row['username'],
                                email=f"{row['username']}@example.com",
                                password=make_password('Temporal123'),
                                first_name=row.get('first_name', ''),
                                last_name=row.get('last_name', ''),
                                rol='author'
                            )
                            autores_creados += 1
                            messages.info(request, 
                                f"Autor creado: {row['username']} (Contraseña: Temporal123)")

                        # Buscar o crear editorial
                        try:
                            editorial = Editorial.objects.get(name=row['editorial'])
                        except Editorial.DoesNotExist:
                            # Crear nueva editorial
                            editorial = Editorial.objects.create(
                                name=row['editorial'],
                                description=row.get('editorial_description', f'Editorial {row["editorial"]}'),
                                address=row.get('editorial_address', 'Dirección pendiente'),
                                phone=row.get('editorial_phone', '000000000'),
                                email=row.get('editorial_email', f'{row["editorial"].lower().replace(" ", "")}@example.com')
                            )
                            editoriales_creadas += 1
                            messages.info(request, f"Editorial creada: {row['editorial']}")

                        # Crear y guardar el libro
                        libro = Libro.objects.create(
                            title=row['title'],
                            tipo=row['tipo'],
                            tamaño=row['tamaño'],
                            editorial=editorial,
                            author=author,
                            description=row['description'],
                            cantidad=row.get('cantidad', 0)
                        )
                        exitosos += 1

                    except Exception as e:
                        fallidos += 1
                        errores.append(f"Error en fila {index + 2}: {str(e)}")
                        continue

                # Mostrar mensajes de resultado
                if exitosos > 0:
                    messages.success(request, f'Se importaron {exitosos} productos exitosamente.')
                if autores_creados > 0:
                    messages.info(request, f'Se crearon {autores_creados} nuevos autores.')
                if editoriales_creadas > 0:
                    messages.info(request, f'Se crearon {editoriales_creadas} nuevas editoriales.')
                if fallidos > 0:
                    messages.warning(request, f'Fallaron {fallidos} productos.')
                    for error in errores:
                        messages.error(request, error)

                return redirect('productos_list')

            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
    else:
        form = ImportarProductosForm()

    return render(request, 'ImportarProductos/importar.html', {'form': form})
