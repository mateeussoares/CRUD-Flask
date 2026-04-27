from flask import Flask, request, jsonify

#request: used to access data sent by the client in an HTTP request
#jsonify: converts Python data into a JSON response


from models.task import Task
app = Flask(__name__)

tasks = []
task_id_control = 1

#CRUD
#1: Create
@app.route("/tasks", methods=['POST'])
def create_task():

    global task_id_control
    data = request.get_json() 
    new_task = Task(id=task_id_control, title=data.get('title'), description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)

    return jsonify({"message": "New task created successfully!"})

#2: Read
@app.route('/tasks', methods=['GET'])
def get_tasks():

    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())
    #Another way to make the code above: task_list = [task.to_dict() for task in tasks] 

    output = {
            "tasks": task_list,
            "total_tasks": len(task_list)
    }
    return jsonify(output)

#method to search an individual task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = None 
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"message": "Could not find the activity."}), 404

#3: Update
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    print(task)
    if task == None:
        return jsonify({"message": "Could not find the activity."}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({"message": "Task edited successfully!"})

#4: Delete
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"message": "Could not find the task."}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Task deleted sucessfuly!"})

if __name__ == "__main__":
    app.run(debug=True)