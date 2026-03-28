import React, { useState } from "react";

export default function Login() {
  const [token, setToken] = useState("");

  const handleLogin = async () => {
    const res = await fetch("http://localhost:8000/login", { method: "POST" });
    const data = await res.json();
    setToken(data.token);
    localStorage.setItem("zspinToken", data.token);
  };

  return (
    <section>
      <h2>Login</h2>
      <button onClick={handleLogin}>Generate Demo JWT</button>
      <pre>{token}</pre>
    </section>
  );
}
