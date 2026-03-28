import React from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";
import Analytics from "./Analytics";

export default function App() {
  return (
    <main style={{ fontFamily: "Arial, sans-serif", padding: 24 }}>
      <h1>zspin Cloud</h1>
      <Login />
      <Dashboard />
      <Analytics />
    </main>
  );
}
