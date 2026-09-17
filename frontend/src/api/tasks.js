const API_BASE_URL = "http://127.0.0.1:8000";

async function handleResponse(response) {
  if (!response.ok) {
    let errorMessage = "Something went wrong.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep the default error message
    }

    throw new Error(errorMessage);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function getAuthHeaders() {
  const token = localStorage.getItem("access_token");

  return {
    Authorization: `Bearer ${token}`,
  };
}

export async function getTasks() {
  const response = await fetch(
    `${API_BASE_URL}/tasks`,
    {
      headers: {
        ...getAuthHeaders(),
      },
    }
  );

  return handleResponse(response);
}

export async function createTask(title) {
  const response = await fetch(
    `${API_BASE_URL}/tasks`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify({
        title: title,
        completed: false,
      }),
    }
  );

  return handleResponse(response);
}

export async function updateTask(
  taskId,
  title,
  completed
) {
  const response = await fetch(
    `${API_BASE_URL}/tasks/${taskId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify({
        title: title,
        completed: completed,
      }),
    }
  );

  return handleResponse(response);
}

export async function deleteTask(taskId) {
  const response = await fetch(
    `${API_BASE_URL}/tasks/${taskId}`,
    {
      method: "DELETE",
      headers: {
        ...getAuthHeaders(),
      },
    }
  );

  return handleResponse(response);
}