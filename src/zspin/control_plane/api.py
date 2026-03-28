from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException

from zspin.apikeys import get_tenant
from zspin.auth import verify_token
from zspin.billing import BillingEngine
from zspin.cache import r
from zspin.control_plane.manager import ControlPlane
from zspin.metering import get_usage, record_deploy
from zspin.rbac import check_permission

app = FastAPI(title="zspin control plane")
cp = ControlPlane()
billing = BillingEngine()


def _resolve_identity(authorization: str | None, x_api_key: str | None) -> tuple[str, str]:
    if authorization:
        try:
            token = authorization.split(" ", maxsplit=1)[1]
            user = verify_token(token)
            tenant = user["tenant"]
            role = user.get("role", "developer")
            return tenant, role
        except (IndexError, KeyError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # pragma: no cover - jwt library specific errors
            raise HTTPException(status_code=401, detail=f"invalid token: {exc}") from exc

    if x_api_key:
        tenant = get_tenant(x_api_key)
        if tenant:
            return tenant, "developer"

    raise HTTPException(status_code=401, detail="Unauthorized")


def _apply_rate_limit(tenant: str) -> None:
    key = f"rate:{tenant}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, 60)
    if count > 10:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")


@app.post("/deploy")
def deploy(
    service: dict,
    cluster: str,
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None),
) -> dict[str, str]:
    tenant, role = _resolve_identity(authorization, x_api_key)

    if not check_permission(role, "deploy"):
        raise HTTPException(status_code=403, detail="Forbidden")

    _apply_rate_limit(tenant)
    result = cp.deploy(service, tenant, cluster)
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
