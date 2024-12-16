from tkinter import Tk, Label, Button, Entry, Listbox, END, StringVar, Scrollbar, Frame, messagebox
from tkinter import ttk
from services.task_service import add_task, list_tasks, complete_task, delete_task, save_tasks_to_file, load_tasks_from_file

def refresh_task_list(task_list):
    task_list.delete(0, END)
    for task in list_tasks():
        task_list.insert(END, f"{task.id}. {task.estado} - {task.titulo} - {task.descripcion}")

def create_main_window():
    app = Tk()
    app.title("Gestión de Tareas")
    app.geometry("700x600")

    titulo_var = StringVar()
    descripcion_var = StringVar()

    # Frame de entradas
    input_frame = Frame(app, bg="#ECEFF1")
    input_frame.grid(row=0, column=0, sticky="w")

    Label(input_frame, text="Título:", font=("Helvetica", 12, "bold"), bg="#ECEFF1").grid(row=0, column=0, sticky="w")
    Entry(input_frame, textvariable=titulo_var, font=("Helvetica", 12), width=40, bd=2).grid(row=0, column=1)

    Label(input_frame, text="Descripción:", font=("Helvetica", 12, "bold"), bg="#ECEFF1").grid(row=1, column=0, sticky="w", pady=10)
    Entry(input_frame, textvariable=descripcion_var, font=("Helvetica", 12), width=40, bd=2).grid(row=1, column=1)

    # Frame de botones con márgenes
    button_frame = Frame(app, bg="#ECEFF1")
    button_frame.grid(row=1, column=0, sticky="w")

    def add_task_ui():
        titulo = titulo_var.get()
        descripcion = descripcion_var.get()
        if titulo:
            add_task(titulo, descripcion)
            refresh_task_list(task_list)
            titulo_var.set("")
            descripcion_var.set("")
        else:
            messagebox.showerror("Error", "El título no puede estar vacío")

    def complete_task_ui():
        try:
            selected_item = task_list.get(task_list.curselection())
            task_id = int(selected_item.split('.')[0])
            complete_task(task_id)
            refresh_task_list(task_list)
        except IndexError:
            messagebox.showerror("Error", "Seleccione una tarea de la lista")

    def delete_selected_task_ui():
        try:
            selected_item = task_list.get(task_list.curselection())
            task_id = int(selected_item.split('.')[0])
            delete_task(task_id)
            refresh_task_list(task_list)
        except IndexError:
            messagebox.showerror("Error", "Seleccione una tarea de la lista")

    def save_tasks_ui():
        save_tasks_to_file('tasks.json')
        messagebox.showinfo("Éxito", "Tareas guardadas en tasks.json")

    def load_tasks_ui():
        load_tasks_from_file('tasks.json')
        refresh_task_list(task_list)

    def import_tasks_ui():
        from tkinter.filedialog import askopenfilename
        filename = askopenfilename(title="Selecciona el archivo JSON", filetypes=[("JSON Files", "*.json")])
        if filename:
            try:
                load_tasks_from_file(filename)
                refresh_task_list(task_list)
                messagebox.showinfo("Éxito", f"Tareas importadas desde {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo importar: {e}")

    def export_tasks_ui():
        from tkinter.filedialog import asksaveasfilename
        filename = asksaveasfilename(title="Guardar archivo JSON", filetypes=[("JSON Files", "*.json")], defaultextension=".json")
        if filename:
            try:
                save_tasks_to_file(filename)
                messagebox.showinfo("Éxito", f"Tareas exportadas a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {e}")

    # Estilo para botones
    button_style = {
        "font": ("Helvetica", 12, "bold"),
        "relief": "flat",
        "cursor": "hand2",
    }

    # Botones organizados en 2 columnas
    Button(button_frame, text="Agregar Tarea", command=add_task_ui,  bg="#673AB7", fg="white", **button_style).grid(row=0, column=0, padx=8, pady=8)
    Button(button_frame, text="Marcar como Completada", command=complete_task_ui, bg="#673AB7", fg="white", **button_style).grid(row=1, column=1, padx=8, pady=8)

    Button(button_frame, text="Eliminar Tarea Seleccionada", command=delete_selected_task_ui,  bg="#673AB7", fg="white", **button_style).grid(row=1, column=0, padx=8, pady=8)
    Button(button_frame, text="Importar Tareas", command=import_tasks_ui, bg="#673AB7", fg="white", **button_style).grid(row=2, column=1, padx=8, pady=8)

    Button(button_frame, text="Exportar Tareas", command=export_tasks_ui, bg="#673AB7", fg="white", **button_style).grid(row=2, column=0, padx=8, pady=8)

    # Frame de lista de tareas
    task_list_frame = Frame(app, bg="#ECEFF1")
    task_list_frame.grid(row=2, column=0, padx=20, pady=20)

    task_list = Listbox(task_list_frame, width=70, height=18, font=("Helvetica", 12), bd=2, relief="solid", bg="#FFFFFF")
    task_list.grid(row=0, column=0)

    scrollbar = Scrollbar(task_list_frame)
    scrollbar.grid(row=0, column=1, sticky="ns")

    task_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=task_list.yview)

    refresh_task_list(task_list)

    return app
