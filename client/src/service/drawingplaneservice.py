from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="http://127.0.0.1:5000")

client = Client(transport=transport, fetch_schema_from_transport=True)

def get_default_plane()-> dict[str, any]:
    query = gql(
        """
    {
    plane(name: "dev") {
        id
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
    """
    )
    result: dict[str, any] = client.execute(query)
    return result["plane"]

def get_plane_list() -> dict[str, any]:
    query = gql(
        """
        {
            allPlanes {
                name
            }
        }
        """
    )
    result: dict[str, any] = client.execute(query)
    return result["allPlanes"]

def get_plane_by_name(planeName) -> dict[str, any]:
    query = gql(
        """
        query ($name: String) {
            plane(name: $name) {
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
        """
    )
    params: dict[str, any] = {"name": planeName}
    result: dict[str, any] = client.execute(query, variable_values=params)
    return result["plane"]

def check_plane_by_name(planeName)-> dict[str, any]:
    query = gql(
        """
        query ($planeName: String){
            plane(name: $planeName) {
                name
            }
        }
        """
    )
    params: dict[str, any]= {"planeName": planeName}
    result: dict[str, any] = client.execute(query, variable_values=params)
    return result["plane"]

def delete_plane_by_name(planeName) -> dict[str, any]:
    mutation = gql(
        """
        mutation ($name: String!){
            deletePlane(name: $name) {
                success
            }
        }
        """
    )
    params: dict[str, any] = {"name": planeName}
    result: dict[str, any] = client.execute(mutation, variable_values=params)
    return result['deletePlane']

def create_plane(planeData) -> dict[str, any]:
    mutation = gql(
        """
        mutation($plane: PlaneInput!) {
            createPlane(planeData: $plane){
                plane {
                    name
                    elements {
                        edges {
                            node {
                                name
                                description
                            }
                        }
                    }
                }
            }
        }
        """
    )
    params: dict[str, any] = {"plane": planeData}
    result: dict[str, any] = client.execute(mutation, variable_values=params)
    return result["createPlane"]

def update_plane(planeData) -> dict[str, any]:
    mutation = gql(
        """
        mutation($plane: PlaneInput!) {
            updatePlane(planeData: $plane){
                plane {
                    name
                    elements {
                        edges {
                            node {
                                name
                                description
                            }
                        }
                    }
                }
            }
        }
        """
        )
    params: dict[str, any] = {"plane": planeData}
    result: dict[str, any] = client.execute(mutation, variable_values=params)
    return result["updatePlane"]
