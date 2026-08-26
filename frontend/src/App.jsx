import { useState } from "react";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";

function App() {
  const [tasks, setTasks] = useState([
    {
      id: 1,
      title: "Learn React",
      completed: false,
    },
    {
      id: 2,
      title: "Practice JSX",
      completed: false,
    },
    {
      id: 3,
      title: "Learn Props",
      completed: true,
    },
  ]);

  const [filter, setFilter] = useState("all");

  function handleComplete(taskId) {
    setTasks((previousTasks) =>
      previousTasks.map((task) =>
        task.id === taskId
          ? {
              ...task,
              completed: !task.completed,
            }
          : task
      )
    );
  }

  function handleDelete(taskId) {
    setTasks((previousTasks) =>
      previousTasks.filter((task) => task.id !== taskId)
    );
  }

  const completedCount = tasks.filter(
    (task) => task.completed
  ).length;

  const pendingCount = tasks.filter(
    (task) => !task.completed
  ).length;

  const filteredTasks = tasks.filter((task) => {
    if (filter === "completed") {
      return task.completed;
    }

    if (filter === "pending") {
      return !task.completed;
    }

    return true;
  });

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="brand">
            <div className="brand-icon">✓</div>

            <div>
              <h1>Task Manager</h1>
              <p>Organize your tasks and get things done</p>
            </div>
          </div>

          <div className="task-count">
            ✓ {tasks.length} tasks
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-container">

        {/* Add Task Section */}
        <section className="add-task-section">
          <div className="add-task-icon">✎</div>

          <div className="add-task-content">
            <h2>Add a new task</h2>

            <TaskForm setTasks={setTasks} />
          </div>
        </section>

        {/* Statistics + Filters */}
        <section className="dashboard-controls">

          <div className="statistics">

            <div className="stat-card total">
              <div className="stat-icon">☷</div>

              <div>
                <strong>{tasks.length}</strong>
                <span>Total</span>
              </div>
            </div>

            <div className="stat-card completed">
              <div className="stat-icon">✓</div>

              <div>
                <strong>{completedCount}</strong>
                <span>Completed</span>
              </div>
            </div>

            <div className="stat-card pending">
              <div className="stat-icon">◷</div>

              <div>
                <strong>{pendingCount}</strong>
                <span>Pending</span>
              </div>
            </div>

          </div>

          {/* Filters */}
          <div className="filters">

            <button
              className={
                filter === "all" ? "filter active" : "filter"
              }
              onClick={() => setFilter("all")}
            >
              All
            </button>

            <button
              className={
                filter === "pending"
                  ? "filter active"
                  : "filter"
              }
              onClick={() => setFilter("pending")}
            >
              Pending
            </button>

            <button
              className={
                filter === "completed"
                  ? "filter active"
                  : "filter"
              }
              onClick={() => setFilter("completed")}
            >
              Completed
            </button>

          </div>
        </section>

        {/* Task List */}
        <TaskList
          tasks={filteredTasks}
          onComplete={handleComplete}
          onDelete={handleDelete}
        />

        

      </main>
    </div>
  );
}

export default App;