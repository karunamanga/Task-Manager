import { useState } from "react";

function TaskForm({ setTasks }) {
  const [title, setTitle] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    if (title.trim() === "") {
      return;
    }

    const newTask = {
      id: Date.now(),
      title: title.trim(),
      completed: false,
    };

    setTasks((previousTasks) => [
      ...previousTasks,
      newTask,
    ]);

    setTitle("");
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Add a new task..."
        value={title}
        onChange={(event) =>
          setTitle(event.target.value)
        }
      />

      <button type="submit" className="add-button">
        <span>＋</span>
        Add Task
      </button>
    </form>
  );
}

export default TaskForm;