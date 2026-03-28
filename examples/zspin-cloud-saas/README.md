# zspin Cloud SaaS Skeleton

This example packages a launch-ready starter with:

- FastAPI backend with JWT auth, analytics, and Stripe checkout hooks
- React frontend with login, query runner, and analytics panels
- Static landing and pricing pages
- FastAPI waitlist collector
- Deployment artifacts for Docker + Cloudflare Tunnel

## Run backend

```bash
cd examples/zspin-cloud-saas/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run frontend

```bash
cd examples/zspin-cloud-saas/frontend
npm install
npm start
```

## Run waitlist API

```bash
cd examples/zspin-cloud-saas/waitlist
uvicorn server:app --reload --port 9000
```
