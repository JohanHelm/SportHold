from app.domain.models.objects import BaseObject
from app.infra.db.inmemory.objects import ObjectController
from app.infra.db.inmemory.dao import InMemoryDB

db = InMemoryDB
object_control = ObjectController(db)


def test_regular_object_create_retvive():
    test_object = BaseObject(
        name="Test object",
        desc="Test description",
        schedules=[]
    )

    result_object: BaseObject = object_control.save_object(test_object)
    assert result_object == object_control.get_object_by_name(test_object.name)
