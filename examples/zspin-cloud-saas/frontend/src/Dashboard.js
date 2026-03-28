import React, { useState } from "react";

export default function Dashboard() {
  const [result, setResult] = useState("");

  const runQuery = async () => {
    const token = localStorage.getItem("zspinToken") || "";
    const form = new URLSearchParams({ sql: "INSERT hello world" });
    const res = await fetch("http://localhost:8000/query?" + form.toString(), {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    setResult(JSON.stringify(data, null, 2));
  };

  return (
    <section>
      <h2>Dashboard</h2>
      <button onClick={runQuery}>Run Query</button>
      <pre>{result}</pre>
    </section>
  );
}
