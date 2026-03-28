from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException

from zspin.auth import verify_token
from zspin.billing import BillingEngine
from zspin.control_plane.manager import ControlPlane
from zspin.metering import get_usage, record_deploy

app = FastAPI(title="zspin control plane")
cp = ControlPlane()
billing = BillingEngine()


@app.post("/deploy")
def deploy(service: dict, cluster: str, authorization: str = Header(...)) -> dict[str, str]:
    try:
        token = authorization.split(" ", maxsplit=1)[1]
        user = verify_token(token)
        tenant = user["tenant"]
        result = cp.deploy(service, tenant, cluster)
    except (IndexError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - jwt library specific errors
        raise HTTPException(status_code=401, detail=f"invalid token: {exc}") from exc

    record_deploy(tenant)
    return result


@app.get("/tenants")
def list_tenants() -> list[str]:
    return cp.list_tenants()


@app.get("/clusters")
def list_clusters() -> list[str]:
    return cp.list_clusters()


@app.get("/billing")
def get_billing(authorization: str = Header(...)) -> dict[str, float | dict[str, float]]:
    try:
        token = authorization.split(" ", maxsplit=1)[1]
        user = verify_token(token)
        tenant = user["tenant"]
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"invalid token: {exc}") from exc

    usage = get_usage(tenant)
    total = billing.calculate(usage)
    return {"usage": usage, "cost": total}
