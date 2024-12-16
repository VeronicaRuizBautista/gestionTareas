from database.models import Session, Task  

def add_task(titulo, descripcion):
    session = Session()  
    task = Task(titulo=titulo, descripcion=descripcion, estado='pendiente')
    session.add(task)
    session.commit()
    session.close() 

def list_tasks():
    session = Session()  
    tasks = session.query(Task).all()
    session.close() 
    return tasks

def complete_task(task_id):
    session = Session()  
    task = session.query(Task).get(task_id)
    if task:
        task.estado = 'completada'
        session.commit()
    session.close() 

def delete_task(task_id):
    session = Session()  
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
    session.close() 

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
        
        session = Session()
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
        session.close() 

    except FileNotFoundError:
        raise FileNotFoundError("Archivo no encontrado")
