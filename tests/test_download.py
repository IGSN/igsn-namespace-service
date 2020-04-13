import pytest

from app import namespaces, types


@pytest.fixture
def namespace_data():
    "Download table from website to check tests"
    return namespaces.download_data()


def test_scraped_data(namespace_data):
    "Check we've got the data that we expect"
    expected = ["namespace", "handle_prefix", "owner"]
    for ns, data in namespace_data.namespaces.items():
        assert ns.upper() == data.namespace
        for attr in expected:
            assert getattr(data, attr) is not None


@pytest.mark.parametrize(
    "expected",
    [
        types.Namespace(
            namespace="000",
            owner="IEDA",
            handle_prefix="10273/000",
            date_created="2013-06-07T08:14:01+02:00",
        ),
        types.Namespace(
            namespace="CS",
            owner="CSIRO",
            handle_prefix="10273/CS",
            date_created="2015-01-22T13:01:15+01:00",
        ),
        types.Namespace(
            namespace="AU",
            owner="GEOAUS",
            handle_prefix="10273/AU",
            date_created="2015-02-12T08:23:28+01:00",
        ),
    ],
)
def test_queries(namespace_data, expected):
    "Check that we can query the data"
    result = namespace_data.by_namespace(expected.namespace)
    assert result == expected


@pytest.mark.parametrize(
    "expected",
    [
        types.Agent(
            name="GEOAUS",
            namespaces=[
                types.Namespace(
                    namespace="AU",
                    owner="GEOAUS",
                    handle_prefix="10273/AU",
                    date_created="2015-02-12T08:23:28+01:00",
                )
            ],
        ),
        types.Agent(
            name="CSIRO",
            namespaces=[
                types.Namespace(
                    namespace="ARRC",
                    owner="CSIRO",
                    handle_prefix="10273/ARRC",
                    date_created="2013-05-24T15:07:34+02:00",
                ),
                types.Namespace(
                    namespace="CS",
                    owner="CSIRO",
                    handle_prefix="10273/CS",
                    date_created="2015-01-22T13:01:15+01:00",
                ),
                types.Namespace(
                    namespace="CSD",
                    owner="CSIRO",
                    handle_prefix="10273/CSD",
                    date_created="2014-05-19T08:44:04+02:00",
                ),
                types.Namespace(
                    namespace="CSI",
                    owner="CSIRO",
                    handle_prefix="10273/CSI",
                    date_created="2013-05-24T15:06:59+02:00",
                ),
            ],
        ),
        types.Agent(
            name="UKIEL",
            namespaces=[
                types.Namespace(
                    namespace="GIK",
                    owner="UKIEL",
                    handle_prefix="10273/GIK",
                    date_created=None,
                ),
                types.Namespace(
                    namespace="KIEL",
                    owner="UKIEL",
                    handle_prefix="10273/KIEL",
                    date_created="2017-11-29T09:30:00+01:00",
                ),
                types.Namespace(
                    namespace="ZMUK",
                    owner="UKIEL",
                    handle_prefix="10273/ZMUK",
                    date_created=None,
                ),
            ],
        ),
    ],
)
def test_agents(namespace_data, expected):
    "Check queries against agents"
    result = namespace_data.by_agent(expected.name)
    assert result == expected
