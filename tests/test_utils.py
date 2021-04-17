from pyrefinder import utils


def test_client_from_topic():
    """Test to confirm that the client id is extracted from the topic
    """
    topic = "dt/fighter/bob/lwt"
    assert utils.client_from_topic(topic) == "bob"