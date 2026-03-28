import { useEffect, useState } from 'react';
import axios from 'axios';

type AdminUser = {
  id: number;
  email: string;
  balance: number;
};

export function AdminDashboard() {
  const [users, setUsers] = useState<AdminUser[]>([]);

  useEffect(() => {
    axios.get<AdminUser[]>('http://localhost:3000/api/admin/users').then((res) => {
      setUsers(res.data);
    });
  }, []);

  return (
    <div className="p-6" style={{ fontFamily: 'sans-serif' }}>
      <h1 className="text-xl font-bold">Admin Panel</h1>

      <table className="mt-4 w-full border" cellPadding={8}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.email}</td>
              <td>{u.balance}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
