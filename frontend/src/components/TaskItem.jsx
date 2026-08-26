function TaskItem({
  task,
  onComplete,
  onDelete,
}) {
  return (
    <div
      className={
        task.completed
          ? "task-item completed-task"
          : "task-item"
      }
    >
      <div className="task-information">

        <div
          className={
            task.completed
              ? "task-check checked"
              : "task-check"
          }
          onClick={() => onComplete(task.id)}
        >
          {task.completed ? "✓" : ""}
        </div>

        <div className="task-details">
          <h3>
            {task.title}
          </h3>

          <p> Created just now</p>
        </div>

      </div>

      <div className="task-actions">

        <button
          className={
            task.completed
              ? "complete-button completed-button"
              : "complete-button"
          }
          onClick={() => onComplete(task.id)}
        >
          ✓{" "}
          {task.completed
            ? "Completed"
            : "Complete"}
        </button>

        <button
          className="delete-button"
          onClick={() => onDelete(task.id)}
        >
          🗑 
        </button>

      </div>
    </div>
  );
}

export default TaskItem;