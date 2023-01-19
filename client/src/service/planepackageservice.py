from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="http://127.0.0.1:5000")

client = Client(transport=transport, fetch_schema_from_transport=True)

def create_planePackage(planePackageData):
    mutation = gql(
        """
        mutation ($planePackageData: PlanePackageInput!) {
            createPlanePackage(planePackageData: $planePackageData) {
                planePackage{
                    name
                }
            }
        }
        """
    )
    params: dict[str, any] = {"planePackageData": planePackageData}
    result: dict[str, any] = client.execute(mutation, variable_values=params)
    return result["createPlanePackage"]

def get_planePackage_list() -> dict[str, any]:
    query = gql(
        """
        {
            allPackages {
                name
                topPlane
            }
        }
        """
    )
    result: dict[str, any] = client.execute(query)
    return result["allPackages"]

def check_planePackage_name(name):
    query = gql(
        """
        query ($name: String) {
            package(name: $name) {
                name
            }
        }
        """
    )
    params: dict[str, any]= {"name": name}
    result: dict[str, any] = client.execute(query, variable_values=params)
    return result["package"]

def get_planePackage_by_name(name):
    query = gql(
        """
        query ($name: String) {
            package(name: $name) {
                name
                topPlane
                planes {
                    edges {
                        node {
                            name
                            width
                            height
                            elements {
                                edges {
                                    node {
                                        name
                                        description
                                        posX
                                        posY
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """
    )
    params: dict[str, any] = {"name": name}
    result: dict[str, any] = client.execute(query, variable_values=params)
    return result["package"]

def update_planePackage(planePackageData) -> dict[str, any]:
    mutation = gql(
        """
        mutation ($planePackageData: PlanePackageInput!) {
            updatePlanePackage(planePackageData: $planePackageData) {
                planePackage{
                    name
                }
            }
        }
        """
        )
    params: dict[str, any] = {"planePackageData": planePackageData}
    result: dict[str, any] = client.execute(mutation, variable_values=params)
    return result["updatePlanePackage"]

def delete_planePackage_by_name(name) -> dict[str, any]:
    mutation = gql(
        """
        mutation ($name: String!) {
            deletePlanePackage(name: $name) {
                success
            }
        }
        """
    )
    params: dict[str, any] = {"name": name}
    result: dict[str, any] = client.execute(mutation, variable_values=params)
    return result['deletePlanePackage']