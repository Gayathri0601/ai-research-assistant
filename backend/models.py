from sqlalchemy import Column, Integer, String, Text
from backend.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)

    # ✅ ADD THIS LINE
    embedding = Column(Text)