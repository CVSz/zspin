import { useEffect, useMemo, useState } from 'react';
import { socket } from '../services/socket';

export default function Dashboard() {
  const userId = 1;
  const [balance, setBalance] = useState(0);
  const [events, setEvents] = useState<string[]>([]);
  const channels = useMemo(
    () => ({
      balance: `balance-${userId}`,
      bet: `bet-${userId}`,
    }),
    [userId],
  );

  useEffect(() => {
    const onBalance = (data: { balance: number }) => {
      setBalance(data.balance);
      setEvents((prev) => [`Balance updated: ${data.balance}`, ...prev].slice(0, 10));
    };

    const onBet = (bet: { id: number; status: string; amount: number }) => {
      setEvents((prev) => [
        `Bet #${bet.id} status=${bet.status}, amount=${bet.amount}`,
        ...prev,
      ].slice(0, 10));
    };

    socket.on(channels.balance, onBalance);
    socket.on(channels.bet, onBet);

    return () => {
      socket.off(channels.balance, onBalance);
      socket.off(channels.bet, onBet);
    };
  }, [channels]);

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 24 }}>
      <h1>Dashboard</h1>
      <h2>Live Balance: {balance}</h2>
      <h3>Recent Events</h3>
      <ul>
        {events.map((event, index) => (
          <li key={`${event}-${index}`}>{event}</li>
        ))}
      </ul>
    </div>
  );
}
