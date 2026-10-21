import axios from "https://esm.sh/axios";

const API_URL = "http://127.0.0.1:8000/api/todos/";
const tableBody = document.getElementById("task-table-body");
const taskForm = document.getElementById("task-form");

// Function to fetch and render all tasks
async function fetchTasks() {
    try {
        const response = await axios.get(API_URL);
        const tasks = response.data;
        
        tableBody.innerHTML = ""; // Clear existing table contents

        tasks.forEach(task => {
            const tr = document.createElement("tr");

            // Handle image rendering safely
            const imageHtml = task.image 
                ? `<img src="${task.image}" alt="Task Image" class="img-thumbnail" style="width: 50px; height: 50px; object-fit: cover;">`
                : `<span class="text-muted small">No image</span>`;

            tr.innerHTML = `
                <td>${task.id}</td>
                <td>${imageHtml}</td>
                <td>${task.title}</td>
                <td><span class="badge bg-primary">Due: ${task.due_date}</span></td>
                <td>
                    <button class="btn btn-danger btn-sm delete-btn" data-id="${task.id}">Delete</button>
                </td>
            `;

            tableBody.appendChild(tr);
        });

        // Add event listeners to delete buttons
        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", async (e) => {
                const taskId = e.target.getAttribute("data-id");
                await deleteTask(taskId);
            });
        });

    } catch (error) {
        console.error("Error fetching tasks:", error);
    }
}

// Function to handle task creation
if (taskForm) {
    taskForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        // FormData handles text fields AND file inputs properly
        const formData = new FormData(taskForm);

        try {
            await axios.post(API_URL, formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            taskForm.reset();
            fetchTasks(); // Reload the table
        } catch (error) {
            console.error("Error creating task:", error.response?.data);
        }
    });
}

// Function to delete a task
async function deleteTask(id) {
    try {
        await axios.delete(`${API_URL}${id}/`);
        fetchTasks(); // Reload the table
    } catch (error) {
        console.error("Error deleting task:", error);
    }
}

// Initial load when the script runs
fetchTasks();