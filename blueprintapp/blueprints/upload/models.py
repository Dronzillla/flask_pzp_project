from blueprintapp.app import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


class Project(db.Model):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    code = Column(String(80), nullable=False, unique=True)

    general = relationship("General", uselist=False, back_populates="project")
    ratios = relationship("Ratios", uselist=False, back_populates="project")


class General(db.Model):
    __tablename__ = "general"
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    reference_period = Column(Integer)
    analysis_method = Column(String(80))
    analysis_principle = Column(String(80))
    main_sector = Column(String(80))
    no_alternatives = Column(Integer)
    da_analysis = Column(Boolean, nullable=False)
    version = Column(String(80))

    project_id = Column(Integer, ForeignKey("project.id"), unique=True)
    project = relationship("Project", back_populates="general")


class Ratios(db.Model):
    __tablename__ = "ratios"
    id = Column(Integer, primary_key=True)
    enis = Column(Float)
    egdv = Column(Integer)
    evgn = Column(Float)
    sva = Column(Float)
    da = Column(Float)
    fgdv = Column(Integer)
    fvgn = Column(Float)
    fnis = Column(Float)

    project_id = Column(Integer, ForeignKey("project.id"), unique=True)
    project = relationship("Project", back_populates="ratios")


class Todo(db.Model):
    __tablename__ = "todos"

    tid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    done = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<TODO {self.title}, Done: {self.done}>"

    def get_id(self):
        return self.tid
