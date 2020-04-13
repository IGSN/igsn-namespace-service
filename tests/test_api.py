import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_read_main(client):
    "Check base endpoint"
    response = client.get("/")
    assert response.ok
    assert response.status_code == 200
    assert response.json()["message"].startswith("Hello from IGSN")


def test_get_agents(client):
    "Check agent list endpoint"
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data)
    assert all(x in data for x in ("CSIRO", "IEDA", "GEOAUS"))


@pytest.mark.parametrize(
    "agent", ["GEOAUS", "IEDA", "CSIRO", "geoaus", "iEdA", "csiro"]
)
def test_get_agent(client, agent):
    "Check agent response (should be case insensitive)"
    response = client.get(f"/agent/{agent}")
    assert response.status_code == 200
    assert response.json()["name"] == agent.upper()


@pytest.mark.parametrize("agent", ["foo", "0245s", "; drop TABLE"])
def test_fail_agent(client, agent):
    response = client.get(f"/agent/{agent}")
    assert response.status_code == 404


def test_get_agent_namespaces(client):
    response = client.get(f"/agent/csiro/namespaces")
    assert response.status_code == 200
    namespace_list = response.json()
    assert isinstance(namespace_list, list)
    assert all(ns['owner'] == 'CSIRO' for ns in namespace_list)
    namespaces = [ns['namespace'] for ns in namespace_list]
    for ns in ["ARRC", "CS", "CSI"]:
        assert ns in namespaces


NAMESPACES = ["000", "cs", "CS", "au", "AU", "ARRC", "Arrc", "Kiel"]


def test_get_namespaces(client):
    "Check namespace list endpoint"
    response = client.get("/namespaces")
    assert response.status_code == 200
    namespace_list = response.json()
    assert isinstance(namespace_list, list)
    assert all(ns.upper() in namespace_list for ns in NAMESPACES)


@pytest.mark.parametrize("namespace", NAMESPACES)
def test_get_namespace(client, namespace):
    response = client.get(f"/namespace/{namespace}")
    assert response.status_code == 200
    assert isinstance


@pytest.mark.parametrize("namespace", ["f00", "b4r", "b4z", "quuX"])
def test_fail_namespace(client, namespace):
    response = client.get(f"/namespace/{namespace}")
    assert response.status_code == 404
