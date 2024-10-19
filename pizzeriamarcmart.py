import flet as ft

def main(page: ft.Page):
    # Configuración de la ventana
    page.scroll = True
    page.title = "Pizzeria MarcMart"
    page.window_center()
    page.window_width = 600
    page.window_height = 400
    page.horizontal_alignment = 'CENTER'
    
    # Establecer el color de fondo de la ventana
    page.bgcolor = ft.colors.BROWN_900

    # Lista de tareas (rows que contienen los checkboxes y botones)
    tasks = []

    # Función para manejar el cambio en el campo de texto
    def text_changed(e):
        # Si el campo de texto tiene contenido, se limpia el mensaje de error
        if new_task.value.strip():
            new_task.error_text = None
            new_task.update()

    # Función para añadir una nueva tarea
    def add_clicked(e):
        # Verificar que el campo no esté vacío
        if not new_task.value.strip():
            new_task.error_text = "¡Debes ingresar un sabor antes de agregarlo!"
            new_task.update()
            return
        
        # Crear un nuevo checkbox con opciones de editar y eliminar
        checkbox = ft.Checkbox(label=new_task.value, on_change=lambda e: task_changed(checkbox, edit_button, delete_button))
        edit_button = ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar",icon_color=ft.colors.GREEN,  disabled=True, on_click=lambda e, cb=checkbox: edit_task(cb))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar",icon_color=ft.colors.RED, disabled=True, on_click=lambda e, row=None: delete_task(row))
        
        # Fila que contiene el checkbox y los botones
        task_row = ft.Row([checkbox, edit_button, delete_button], alignment="spaceBetween")

        # Pasar la fila (task_row) como referencia al botón eliminar
        delete_button.on_click = lambda e: delete_task(task_row)

        # Añadir la fila a la lista de tareas y a la página
        tasks.append(task_row)
        page.add(task_row)

        # Limpiar el campo de texto
        new_task.value = ""
        new_task.focus()
        new_task.update()

    # Función para manejar el cambio en el estado del checkbox (seleccionado/no seleccionado)
    def task_changed(checkbox, edit_button, delete_button):
        # Habilitar o deshabilitar los botones de editar y eliminar según el estado del checkbox
        if checkbox.value:  # Si está marcado
            edit_button.disabled = False
            delete_button.disabled = False
        else:
            edit_button.disabled = True
            delete_button.disabled = True
        page.update()

    # Función para editar una tarea
    def edit_task(checkbox):
        def save_task(e):
            checkbox.label = edit_field.value
            edit_dialog.open = False
            page.update()
        
        edit_field = ft.TextField(value=checkbox.label, expand=True)
        save_button = ft.TextButton("Guardar", on_click=save_task)
        edit_dialog = ft.AlertDialog(
            title=ft.Text("Editar tarea"),
            content=edit_field,
            actions=[save_button],
            on_dismiss=lambda e: print("Dialog cerrado")
        )
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    # Función para eliminar una tarea
    def delete_task(row):
        tasks.remove(row)
        page.controls.remove(row)  # Eliminar la fila (task_row) de la página
        page.update()

    # Campo de texto para agregar nuevas tareas, con `on_change` para detectar cambios
    new_task = ft.TextField(
        hint_text="Qué sabor deseas?", 
        width=300,
        on_change=text_changed  # Cada vez que el usuario escribe, esta función se llama
    )

    # Cabecera con logo e imagen
    logo = ft.Image(src="./MarcMart.png", height=200)
    header_text = ft.Text("Bienvenidos a la APP Pizzería MarcMart", size=20, weight=ft.FontWeight.BOLD)

    # Organizar cabecera en una columna
    header = ft.Column([logo, header_text], alignment="center")

    # Añadir elementos a la página
    page.add(
        header,  # Mostrar la cabecera primero
        ft.Divider(height=20),  # Divisor entre el logo y la sección de tareas
        ft.Row([new_task, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked, bgcolor=ft.colors.ORANGE)]),
    )

# Ejecutar la aplicación
ft.app(main)
