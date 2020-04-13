""" Basic API for IGSN namespaces
"""

from typing import List, Dict

import fastapi
from fastapi.responses import JSONResponse

from . import namespaces, types

app = fastapi.FastAPI()
ns = namespaces.download_data()


# Repeated keyword arguments
def add_err(*errs):
    "Add error responses as required"
    return dict(responses={err: {"model": types.HTTPErrorMessage} for err in errs})


@app.get("/")
def main() -> Dict[str, str]:
    "test"
    return {
        "message": "Hello from IGSN's agent finder API. "
        "Please see `GET /docs` for swagger docs"
    }


@app.get("/agents", **add_err(400))
def list_agents() -> types.HTTPResponse[List[str]]:
    "List all agents"
    agents = list(ns.agents.keys())
    return agents or JSONResponse(
        status_code=400, content={"detail": "No agents defined"}
    )


@app.get("/agent/{agent}", response_model=types.Agent, **add_err(404))
def get_agent(agent: str) -> types.HTTPResponse[types.Agent]:
    "Return namespaces controlled by a given agent"
    return ns.by_agent(agent) or JSONResponse(
        status_code=404, content={"detail": f"Agent {agent} not found"}
    )


@app.get(
    "/agent/{agent}/namespaces", response_model=List[types.Namespace], **add_err(404)
)
def list_agent_namespaces(agent: str) -> types.HTTPResponse[List[types.Namespace]]:
    "List namespaces controlled by a given agent"
    result = ns.by_agent(agent)
    return (
        result.namespaces
        if result
        else JSONResponse(
            status_code=404, content={"detail": f"Agent {agent} not found"}
        )
    )


@app.get("/namespaces", response_model=List[str], **add_err(400))
def list_namespaces() -> types.HTTPResponse[List[str]]:
    "List all namespaces"
    namespaces = list(ns.namespaces.keys())
    return namespaces or JSONResponse(
        status_code=400, content={"detail": "No namespaces defined"}
    )


@app.get("/namespace/{namespace}", response_model=types.Namespace, **add_err(404))
def get_namespace(namespace: str) -> types.HTTPResponse[types.Namespace]:
    "Return info about a namespace"
    return ns.by_namespace(namespace) or JSONResponse(
        status_code=404,
        content={
            "detail": f"Namespace {namespace} not found, "
            "see `GET /namespace` for valid values."
        },
    )
