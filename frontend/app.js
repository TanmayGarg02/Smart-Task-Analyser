let tasks = [];

document.getElementById("taskForm").addEventListener("submit", addTask);
document.getElementById("analyzeBtn").addEventListener("click", analyzeTasks);
document.getElementById("suggestBtn").addEventListener("click", suggestTasks);

async function addTask(event) {
    event.preventDefault();

    const title = document.getElementById("title").value;
    const due_date = document.getElementById("due_date").value;
    const effort = parseInt(document.getElementById("effort").value);
    const importance = parseInt(document.getElementById("importance").value);
    const dependenciesInput = document.getElementById("dependencies").value;
    const dependencies = dependenciesInput
        ? dependenciesInput.split(",").map(d => parseInt(d.trim()))
        : [];

    const taskData = { title, due_date, effort, importance, dependencies };

    const response = await fetch("http://127.0.0.1:8000/api/tasks/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(taskData)
    });

    const savedTask = await response.json();

    tasks.push(savedTask);
    renderTaskList();

    document.getElementById("taskForm").reset();
}

function renderTaskList() {
    const listDiv = document.getElementById("taskList");
    listDiv.innerHTML = "";

    tasks.forEach(task => {
        const div = document.createElement("div");
        div.classList.add("result-item");
        div.innerHTML = `
            <strong>${task.title}</strong> 
            | Due: ${task.due_date} 
            | Effort: ${task.effort} 
            | Importance: ${task.importance} 
            | ID: ${task.id}
            | Dependencies: [${task.dependencies.join(", ")}]
        `;
        listDiv.appendChild(div);
    });
}

async function analyzeTasks() {
    const strategy = document.getElementById("strategySelect").value;

    const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ strategy, tasks })
    });

    const data = await response.json();
    renderAnalyzeResults(data);
}

function renderAnalyzeResults(data) {
    const resultDiv = document.getElementById("resultList");
    resultDiv.innerHTML = "";

    data.sorted_tasks.forEach(task => {
        const div = document.createElement("div");
        div.classList.add("result-item");

        let priorityClass = task.score >= 50 ? "high" :
                            task.score >= 30 ? "medium" : "low";

        div.classList.add(priorityClass);

        div.innerHTML = `
            <strong>${task.title}</strong> 
            | Score: ${task.score} 
            | Due: ${task.due_date}
            | Effort: ${task.effort}
            | Importance: ${task.importance}
        `;

        resultDiv.appendChild(div);
    });
}

async function suggestTasks() {
    const strategy = document.getElementById("strategySelect").value;

    const response = await fetch(
        `http://127.0.0.1:8000/api/tasks/suggest/?strategy=${strategy}`
    );

    const data = await response.json();
    renderSuggestions(data);
}

function renderSuggestions(data) {
    const suggestDiv = document.getElementById("suggestList");
    suggestDiv.innerHTML = "";

    if (!data.suggestions || data.suggestions.length === 0) {
        suggestDiv.innerHTML = "<p>No suggestions available.</p>";
        return;
    }

    data.suggestions.forEach(task => {
        const div = document.createElement("div");
        div.classList.add("result-item");

        div.innerHTML = `
            <strong>${task.title}</strong>
            | Score: ${task.score}
            | Reason: ${task.reason}
            | Due: ${task.due_date}
            | Effort: ${task.effort}
            | Importance: ${task.importance}
        `;

        suggestDiv.appendChild(div);
    });
}
