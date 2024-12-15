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
import logging

logger = logging.getLogger(__name__)

def importar_productos(request):
    if request.method == 'POST':
        form = ImportarProductosForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['archivo']
                
                # Verificar la extensión del archivo
                file_ext = os.path.splitext(excel_file.name)[1]
                if file_ext not in ['.xlsx', '.xls']:
                    messages.error(request, 'El archivo debe ser un Excel (.xlsx o .xls)')
                    return render(request, 'ImportarProductos/importar.html', {'form': form})

                try:
                    df = pd.read_excel(excel_file)
                except Exception as e:
                    logger.error(f"Error al leer el archivo Excel: {str(e)}")
                    messages.error(request, f'Error al leer el archivo Excel: {str(e)}')
                    return render(request, 'ImportarProductos/importar.html', {'form': form})

                if df.empty:
                    messages.error(request, 'El archivo Excel está vacío')
                    return render(request, 'ImportarProductos/importar.html', {'form': form})

                # Verificar campos requeridos
                required_fields = ['title', 'tipo', 'tamaño', 'editorial', 'username', 'description']
                missing_fields = [field for field in required_fields if field not in df.columns]
                if missing_fields:
                    messages.error(request, f'Faltan las siguientes columnas requeridas: {", ".join(missing_fields)}')
                    return render(request, 'ImportarProductos/importar.html', {'form': form})

                exitosos = 0
                fallidos = 0
                errores = []
                autores_creados = 0
                editoriales_creadas = 0

                for index, row in df.iterrows():
                    try:
                        # Validar campos vacíos
                        empty_fields = [field for field in required_fields if pd.isna(row[field])]
                        if empty_fields:
                            raise ValueError(f"Campos vacíos: {', '.join(empty_fields)}")

                        # Validar el tipo de libro según las opciones permitidas
                        if row['tipo'] not in ['Libro', 'Revista', 'Enciclopedias']:
                            raise ValueError("El tipo debe ser 'Libro', 'Revista' o 'Enciclopedias'")

                        # Validar que el tamaño sea un número positivo
                        try:
                            tamaño = int(row['tamaño'])
                            if tamaño <= 0:
                                raise ValueError
                        except:
                            raise ValueError("El tamaño debe ser un número positivo")

                        # Buscar o crear autor
                        try:
                            author = Users.objects.get(username=row['username'])
                            if author.rol != 'author':
                                author.rol = 'author'
                                author.save()
                        except Users.DoesNotExist:
                            author = Users.objects.create(
                                username=row['username'],
                                email=f"{row['username']}@example.com",
                                password=make_password('Temporal123'),
                                first_name=str(row.get('first_name', '')),
                                last_name=str(row.get('last_name', '')),
                                rol='author'
                            )
                            autores_creados += 1
                            messages.info(request, f"Autor creado: {row['username']}")

                        # Buscar o crear editorial
                        try:
                            editorial = Editorial.objects.get(name=row['editorial'])
                        except Editorial.DoesNotExist:
                            editorial = Editorial.objects.create(
                                name=str(row['editorial']),
                                address=str(row.get('editorial_address', f'Dirección de {row["editorial"]}')),
                                phone=int(row.get('editorial_phone', '900000000'))
                            )
                            editoriales_creadas += 1
                            messages.info(request, f"Editorial creada: {row['editorial']}")

                        # Crear libro
                        cantidad = int(row.get('cantidad', 0))
                        libro = Libro.objects.create(
                            title=str(row['title']),
                            tipo=str(row['tipo']),
                            tamaño=int(row['tamaño']),
                            editorial=editorial,
                            author=author,
                            description=str(row['description']),
                            cantidad=cantidad,
                            estadoLibro='Revision'  # Estado por defecto
                        )
                        exitosos += 1

                    except Exception as e:
                        logger.error(f"Error en fila {index + 2}: {str(e)}")
                        fallidos += 1
                        errores.append(f"Error en fila {index + 2}: {str(e)}")
                        continue
                return redirect('base')

            except Exception as e:
                logger.error(f"Error general: {str(e)}")
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')

    else:
        form = ImportarProductosForm()

    return render(request, 'ImportarProductos/importar.html', {'form': form})