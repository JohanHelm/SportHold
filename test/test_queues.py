from src.models.queues import BaseQueue


def test_regular_queue_creation():
    testQueue = BaseQueue(
        owner_queue=[],
        visitor_queue=[]
    )

    assert testQueue.owner_queue == []
    assert testQueue.visitor_queue == []
