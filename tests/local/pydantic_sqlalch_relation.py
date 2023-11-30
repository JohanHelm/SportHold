from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
from sqlalchemy import ForeignKey, Column, Integer, String
from typing_extensions import Annotated

Base = declarative_base()


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

    children = relationship("Child", back_populates="parent")


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    parent_id = Column("parent_id", Integer(), ForeignKey("parents.id"), nullable=False)

    parent = relationship("Parent", back_populates="children")


class ChildSchema(BaseModel):
    id: Optional[int] = None
    name: str
    parent_id: int = None

    model_config = ConfigDict(from_attributes=True)


class ParentSchema(BaseModel):
    id: Optional[int] = None
    name: str

    children: List[ChildSchema] = None

    model_config = ConfigDict(from_attributes=True)


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def main():
    db = SessionLocal()

    parent = ParentSchema(name="1", children=[])

    db_parent = Parent(**parent.model_dump())

    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)

    child = ChildSchema(name="2", parent_id=db_parent.id)
    db_child = Child(**child.model_dump())
    db.add(db_child)
    db.commit()
    db.refresh(db_child)

    db_child.name = "changed"
    
    p = ParentSchema.model_validate(db_parent)
    s = ChildSchema.model_validate(db_child)

    db.commit()
    db.refresh(db_child)

    print(1, p)
    print(2, s)


if __name__ == "__main__":
    main()
