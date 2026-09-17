import { useEffect, useState } from "react";

import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import Login from "./components/Login";

import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
} from "./api/tasks";


function App() {
  const [tasks, setTasks] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [isAuthenticated, setIsAuthenticated] =
    useState(
      Boolean(
        localStorage.getItem("access_token")
      )
    );


  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }

    async function loadTasks() {
      try {
        setLoading(true);
        setError("");

        const data = await getTasks();

        setTasks(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadTasks();
  }, [isAuthenticated]);


  function handleLogin() {
    setIsAuthenticated(true);
  }


  function handleLogout() {
    localStorage.removeItem("access_token");

    setIsAuthenticated(false);
    setTasks([]);
  }


  async function handleComplete(taskId) {
    const task = tasks.find(
      (task) => task.id === taskId
    );

    if (!task) {
      return;
    }

    try {
      setError("");

      const updatedTask = await updateTask(
        task.id,
        task.title,
        !task.completed
      );

      setTasks((previousTasks) =>
        previousTasks.map((task) =>
          task.id === updatedTask.id
            ? updatedTask
            : task
        )
      );
    } catch (error) {
      setError(error.message);
    }
  }


  async function handleDelete(taskId) {
    try {
      setError("");

      await deleteTask(taskId);

      setTasks((previousTasks) =>
        previousTasks.filter(
          (task) => task.id !== taskId
        )
      );
    } catch (error) {
      setError(error.message);
    }
  }


  async function handleAdd(title) {
    try {
      setError("");

      const newTask = await createTask(title);

      setTasks((previousTasks) => [
        ...previousTasks,
        newTask,
      ]);
    } catch (error) {
      setError(error.message);
    }
  }


  if (!isAuthenticated) {
    return (
      <Login onLogin={handleLogin} />
    );
  }


  return (
    <div className="app">

      <header className="app-header">
        <h1>Task Manager</h1>

        <p>
          Manage your tasks efficiently
        </p>

        <button onClick={handleLogout}>
          Logout
        </button>
      </header>


      <main className="app-main">

        <TaskForm onAdd={handleAdd} />


        {error && (
          <div className="error-message">
            {error}
          </div>
        )}


        {loading ? (
          <div className="status-message">
            Loading tasks...
          </div>
        ) : (
          <TaskList
            tasks={tasks}
            onComplete={handleComplete}
            onDelete={handleDelete}
          />
        )}

      </main>

    </div>
  );
}


export default App;