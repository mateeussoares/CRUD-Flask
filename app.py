from flask import Flask, request, jsonify
#Request is a global proxy to access data from a http request sen by a client.
#jsonify is used to convert data structure to a json response ready to be send to an API web.


from models.task import Task
app = Flask(__name__)

tasks = []
task_id_control = 1


#Create
@app.route("/tasks", methods=['POST'])
def create_task():

    global task_id_control
    data = request.get_json() 
    new_task = Task(id=task_id_control, title=data.get('title'), description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "New task created successfully!"})

#Read
@app.route('/tasks', methods=['GET'])
def get_tasks():

    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())
    #Outra forma de fazer o código acima: task_list = [task.to_dict() for task in tasks] 

    output = {
            "tasks": task_list,
            "total_tasks": len(task_list)
    }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = None 
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"message": "Could not find the activity."}), 404


if __name__ == "__main__":
    app.run(debug=True)