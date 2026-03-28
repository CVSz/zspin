import React, { useEffect, useState } from "react";

export default function Analytics() {
  const [data, setData] = useState({});

  useEffect(() => {
    const token = localStorage.getItem("zspinToken") || "";
    if (!token) {
      return;
    }
    fetch("http://localhost:8000/analytics", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then((res) => res.json())
      .then(setData)
      .catch(() => setData({ error: "Unable to fetch analytics" }));
  }, []);

  return (
    <section>
      <h2>Usage Analytics</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </section>
  );
}
