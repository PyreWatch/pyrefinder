def client_from_topic(topic_path):
    """Return client id when give a topic path

    Args:
        topic_path (str): the topic path, i.e "dt/fighter/client_id"

    Returns:
        client_id [str]: the client/destination client id  
    """
    topics = topic_path.split("/")
    return topics[2]
