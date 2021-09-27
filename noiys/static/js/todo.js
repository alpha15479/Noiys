function changeStatus(task) {
    console.log("Task", task);
    let completed = !task.Completed;
    let url = `http://127.0.0.1:8000/api/todo-updates/${task.id}`;
    fetch(url, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ title: task.title, Completed: completed }),
    }).then(function() {
        buildList();
    });
}