from tkinter import Tk, Label, Button, Entry, Listbox, StringVar, Scrollbar, END, messagebox
from services.task_service import add_task, list_tasks, complete_task, delete_task, save_tasks_to_file, load_tasks_from_file

def refresh_task_list(task_list):
    task_list.delete(0, END)
    for task in list_tasks():
        task_list.insert(END, f"{task.id}. {task.estado} - {task.titulo} - {task.descripcion}")

def create_main_window():
    app = Tk()
    app.title("Gestión de Tareas")
    app.geometry("600x600")

    titulo_var = StringVar()
    descripcion_var = StringVar()

    Label(app, text="Título:").pack()
    Entry(app, textvariable=titulo_var).pack()

    Label(app, text="Descripción:").pack()
    Entry(app, textvariable=descripcion_var).pack()

    task_list = Listbox(app, width=80, height=20)
    task_list.pack()

    scrollbar = Scrollbar(app)
    scrollbar.pack(side="right", fill="y")

    task_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=task_list.yview)

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

    Button(app, text="Agregar Tarea", command=add_task_ui).pack()
    Button(app, text="Marcar como Completada", command=complete_task_ui).pack()
    Button(app, text="Eliminar Tarea Seleccionada", command=delete_selected_task_ui).pack()
    Button(app, text="Importar Tareas", command=import_tasks_ui).pack()
    Button(app, text="Exportar Tareas", command=export_tasks_ui).pack()

    refresh_task_list(task_list)

    return app
