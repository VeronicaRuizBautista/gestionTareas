from database import Session
from database.models import Task

session = Session()

def add_task(titulo, descripcion):
    task = Task(titulo=titulo, descripcion=descripcion, estado='pendiente')
    session.add(task)
    session.commit()

def list_tasks():
    return session.query(Task).all()

def complete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.estado = 'completada'
        session.commit()

def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()

def save_tasks_to_file(filename):
    tasks = list_tasks()
    data = [{'id': task.id, 'titulo': task.titulo, 'descripcion': task.descripcion, 'estado': task.estado} for task in tasks]
    with open(filename, 'w') as file:
        import json
        json.dump(data, file)

def load_tasks_from_file(filename):
    try:
        with open(filename, 'r') as file:
            import json
            data = json.load(file)
        for task in data:
            existing_task = session.query(Task).get(task['id'])
            if not existing_task:
                new_task = Task(
                    titulo=task['titulo'], 
                    descripcion=task['descripcion'], 
                    estado=task['estado']
                )
                session.add(new_task)
        session.commit()
    except FileNotFoundError:
        raise FileNotFoundError("Archivo no encontrado")
