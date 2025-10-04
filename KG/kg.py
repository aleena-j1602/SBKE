from tqdm import tqdm


# 1. Add main nodes without creating relationships
def create_nodes(graph, data: dict, node_label: str, node_name: str):
    # Create the main node
    main_node_query = f"""
    MERGE (main:{node_label} {{name: $name}})
    """
    graph.query(main_node_query, params={"name": node_name})

    # Create section nodes only (without relationships)
    for section, content in data.items():
        query = f"""
        MERGE (s:Section {{type: $type, parent_name: $name}})
     
        """
        params = {
            "type": section,
            "name": node_name
        }
        graph.query(query, params=params)


# 2. Add Chunks
def ingest_Chunks(graph, chunks, node_name, node_label):
    """
    Ingests file chunk data into the knowledge graph by merging chunk nodes.

    Args:
        graph: A knowledge graph client or connection object that has a `query` method.
        chunks: A list of dictionaries, each representing a file chunk with keys:
                     'chunkId', 'text', 'source', 'formItem', and 'chunkSeqId'.
        node_name: A string used to tag the chunk nodes.
        node_label: The dynamic label for the chunk nodes.
    """
    merge_chunk_node_query = f"""
    MERGE (mergedChunk:{node_label} {{chunkId: $chunkParam.chunkId}})
        ON CREATE SET
            mergedChunk.text = $chunkParam.text, 
            mergedChunk.source = $chunkParam.Source, 
            mergedChunk.formItem = $chunkParam.formItem, 
            mergedChunk.chunkSeqId = $chunkParam.chunkSeqId,
            mergedChunk.node_name = $node_name
    RETURN mergedChunk
    """

    node_count = 0
    for chunk in chunks:
        print(f"Creating `:{node_label}` node for chunk ID {chunk['chunkId']}")
        graph.query(merge_chunk_node_query, params={'chunkParam': chunk, 'node_name': node_name})
        node_count += 1
    print(f"Created {node_count} nodes")
