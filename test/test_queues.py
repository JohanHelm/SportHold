from src.models.queues import BaseQueue


def test_regular_queue_creation():
    testQueue = BaseQueue(
        clients_queue=[],
    )

    assert testQueue.clients_queue == []
