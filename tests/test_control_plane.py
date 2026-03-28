from zspin.auth import create_token, verify_token
from zspin.billing import BillingEngine
from zspin.control_plane.manager import ControlPlane
from zspin.multicluster import MultiClusterScheduler


def test_scheduler_selects_first_sorted_cluster() -> None:
    scheduler = MultiClusterScheduler()
    cluster = scheduler.select_cluster({"name": "api"}, {"cluster-b": {}, "cluster-a": {}})
    assert cluster == "cluster-a"


def test_control_plane_deploy_tracks_tenant_service() -> None:
    cp = ControlPlane()
    result = cp.deploy({"name": "api"}, "tenant-1", "cluster-a")
    assert result["tenant"] == "tenant-1"
    assert cp.list_tenants() == ["tenant-1"]


def test_auth_round_trip_and_billing_calculation() -> None:
    token = create_token("alice", "tenant-1")
    payload = verify_token(token)
    assert payload["tenant"] == "tenant-1"

    total = BillingEngine().calculate({"deploys": 3, "cpu": 10})
    assert total == 0.04
