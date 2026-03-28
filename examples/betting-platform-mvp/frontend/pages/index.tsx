import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ fontFamily: 'sans-serif', padding: 24 }}>
      <h1>Betting Platform MVP</h1>
      <p>Open the live dashboard to see real-time balance and bet events.</p>
      <Link href="/dashboard">Go to dashboard</Link>
    </main>
  );
}
