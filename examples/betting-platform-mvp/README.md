# Betting Platform MVP (Buildable Monorepo Example)

This example implements a runnable MVP stack with:

- NestJS backend API + Socket.IO gateway
- Next.js player frontend with real-time dashboard
- React (Vite) admin panel with user + balance view
- Docker Compose to boot local infra and apps

## Repo structure

```text
examples/betting-platform-mvp/
├── backend/
├── frontend/
├── admin-panel/
└── docker-compose.yml
```

## Quick start (local)

```bash
cd examples/betting-platform-mvp

docker compose up --build
```

Services:

- Backend API: http://localhost:3000/api
- Frontend: http://localhost:3001
- Admin panel: http://localhost:3002

## Core API endpoints

- `POST /api/wallet/:userId/deposit`
- `POST /api/wallet/:userId/withdraw`
- `GET /api/wallet/:userId/balance`
- `POST /api/betting/:userId/place`
- `POST /api/betting/:betId/settle`
- `GET /api/admin/users`

## Real-time events

- `balance-<userId>`
- `bet-<userId>`

## Notes

- Data is in-memory for fast MVP iteration.
- Replace in-memory stores with PostgreSQL repositories + transactions for production.
- Add JWT auth, webhook signature verification, and rate limits before going live.
