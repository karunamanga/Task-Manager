import TaskItem from "./TaskItem";

function TaskList({
  tasks,
  onComplete,
  onDelete,
}) {
  if (tasks.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">☷</div>

        <h2>No tasks yet!</h2>

        <p>
          Add a task above to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onComplete={onComplete}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}

export default TaskList;