from src.models.objects import BaseObject


def test_regular_object_creation():
    testObject = BaseObject(
        name="Test object",
        desc="Test description",
        schedules=[]
    )

    assert testObject.name == "Test object"
