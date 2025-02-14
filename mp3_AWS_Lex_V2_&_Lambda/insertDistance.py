import json
import boto3
from collections import deque, defaultdict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GraphDistance')


def parse_graph(graph):
    adj_list = defaultdict(list)
    edges = graph.split(",")
    for edge in edges:
        source, destination = edge.split("->")
        adj_list[source].append(destination)
        adj_list[destination]
    return adj_list


def bfs(graph):
    shortest_paths = []
    for node in graph:
        dq = deque([(node, 0)])
        visited = set([node])
        while dq:
            current_node, dist = dq.popleft()
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    shortest_paths.append({
                        "source": node,
                        "destination": neighbor,
                        "distance": dist + 1
                    })
                    dq.append((neighbor, dist + 1))
    return shortest_paths


def lambda_handler(event, context):
    try:
        graph = event["graph"]

        if not graph:
            return {
                'statusCode': 400,
                'body': json.dumps({"message": "Invalid input"})
            }

        # parse graph into an adjacency list
        adj_list = parse_graph(graph)
        # bfs
        shortest_paths = bfs(adj_list)

        # store in dynamodb
        with table.batch_writer() as batch:
            for path in shortest_paths:
                batch.put_item(Item=path)

        return {
            'statusCode': 200,
            'body': json.dumps('Graph processed and stored successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"message": str(e)})
        }