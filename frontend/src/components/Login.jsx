import { useState } from "react";
import { loginUser } from "../api/auth";

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(event) {
    event.preventDefault();

    try {
      setError("");

      const result = await loginUser(email, password);

      localStorage.setItem(
        "access_token",
        result.access_token
      );

      onLogin();
    } catch (error) {
      setError(error.message);
    }
  }

  return (
    <div className="app">
      <main className="app-main">
        <h2>Login</h2>

        <form onSubmit={handleLogin}>
          <div>
            <label>Email</label>

            <input
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label>Password</label>

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter your password"
            />
          </div>

          <button type="submit">
            Login
          </button>
        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
      </main>
    </div>
  );
}

export default Login;