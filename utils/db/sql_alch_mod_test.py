from typing import List, Tuple
from sqlalchemy import (
    Row,
    Select,
    create_engine,
    Integer,
    String,
    ForeignKey,
    select,
    delete,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()
engine = create_engine("sqlite:///example.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class BaseObject(Base):
    __tablename__ = "objects"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="object")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    queues: Mapped[List["Queue"]] = relationship(back_populates="user")


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    object_id: Mapped[int] = mapped_column(Integer, ForeignKey("objects.id"))
    object: Mapped["BaseObject"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship(back_populates="schedule")
    queues: Mapped[List["Queue"]] = relationship(back_populates="schedule")


class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey("schedules.id"))
    schedule: Mapped["Schedule"] = relationship(back_populates="slots")
    queues: Mapped[List["Queue"]] = relationship(back_populates="slot")


# Модель очереди на слот
class Queue(Base):
    __tablename__ = "queues"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[User] = mapped_column(Integer, ForeignKey("users.id"), unique=False)
    slot_id: Mapped[Slot] = mapped_column(Integer, ForeignKey("slots.id"), unique=False)
    schedule_id: Mapped[Schedule] = mapped_column(
        Integer, ForeignKey("schedules.id"), unique=False
    )
    user: Mapped["User"] = relationship(back_populates="queues")
    slot: Mapped["Slot"] = relationship(back_populates="queues")
    schedule: Mapped["Schedule"] = relationship(back_populates="queues")


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

user1 = User(name="user1")
user2 = User(name="user2")
obj1 = BaseObject(name="obj1")

session.add(user1)
session.add(user2)
session.add(obj1)

session.commit()

curr_obj = session.get(BaseObject, 1)

sch1 = Schedule(name="schedule 1")
curr_obj.schedules.append(sch1)

session.commit()
slot1 = Slot(name="slot 1")

curr_sch = session.get(Schedule, 1)

curr_sch.slots.append(slot1)
session.commit()

q1 = Queue(schedule=curr_sch, slot=slot1, user=user1)
q2 = Queue(schedule=curr_sch, slot=slot1, user=user2)

session.add(q1)
session.add(q2)

session.commit()

stmt: Select[Tuple[Queue]] = (
    select(Queue).where(Queue.user == user1).where(Queue.slot == slot1)
)
res: Row[Tuple[Queue]] | None = session.execute(stmt).fetchone()
if not res is None:
    for row in res:
        print(row.user.name)

# удаление пользователя их очереди
stmt: Select[Tuple[Queue]] = (
    delete(Queue).where(Queue.slot == slot1).where(Queue.user == user1)
)
res: Row[Tuple[Queue]] | None = session.execute(stmt)

stmt: Select[Tuple[Queue]] = select(Queue).where(Queue.slot == slot1)
res: Row[Tuple[Queue]] | None = session.execute(stmt).fetchone()
print(res[0].user.name)


session.commit()
