from blueprintapp.app import db

# from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
# from sqlalchemy.orm import relationship


# Association Table for Many-to-Many Relationship
# Project - Sector
project_sector = db.Table(
    "project_sector",
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
    db.Column("sector_id", db.Integer, db.ForeignKey("sector.id"), primary_key=True),
)


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    code = db.Column(db.String(80), nullable=False, unique=True)

    # Relationships (PK) one to one
    # uselist=False
    general = db.relationship("General", uselist=False, back_populates="project")
    ratios = db.relationship("Ratios", uselist=False, back_populates="project")
    # Relationships (PK) one to many
    cashflow = db.relationship("Cashflow", back_populates="project")
    capex = db.relationship("Capex", back_populates="project")
    reinvestment = db.relationship("Reinvestment", back_populates="project")
    opex = db.relationship("Opex", back_populates="project")
    revenue = db.relationship("Revenue", back_populates="project")
    tax_revenue = db.relationship("TaxRevenue", back_populates="project")
    vat = db.relationship("Vat", back_populates="project")
    private_revenue = db.relationship("PrivateRevenue", back_populates="project")
    private_cost = db.relationship("PrivateCost", back_populates="project")
    benefit = db.relationship("Benefit", back_populates="project")
    # Relationships Many to many
    # Sector
    sectors = db.relationship(
        "Sector",
        secondary=project_sector,
        lazy="subquery",
        back_populates="projects",
    )

    # TODO create Harm model
    # TODO Remove sector db connection
    # harm = db.relationship("Harm", back_populates="project")


class General(db.Model):
    __tablename__ = "general"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    reference_period = db.Column(db.Integer)
    analysis_method = db.Column(db.String(80))
    analysis_principle = db.Column(db.String(80))
    main_sector = db.Column(db.String(80))
    no_alternatives = db.Column(db.Integer)
    da_analysis = db.Column(db.Boolean)
    version = db.Column(db.String(80))

    # Relationship one to one
    # Project
    # unique=True
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), unique=True)
    project = db.relationship("Project", back_populates="general")


class Ratios(db.Model):
    __tablename__ = "ratios"
    id = db.Column(db.Integer, primary_key=True)
    enis = db.Column(db.Float)
    egdv = db.Column(db.Integer)
    evgn = db.Column(db.Float)
    sva = db.Column(db.Float)
    da = db.Column(db.Float)
    fgdv = db.Column(db.Integer)
    fvgn = db.Column(db.Float)
    fnis = db.Column(db.Float)

    # Relationship one to one
    # Project
    # unique=True
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), unique=True)
    project = db.relationship("Project", back_populates="ratios")


class Cashflow(db.Model):
    __tablename__ = "cashflow"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)
    category = db.Column(db.String(80))
    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="cashflow")


class Capex(db.Model):
    __tablename__ = "capex"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="capex")


class Reinvestment(db.Model):
    __tablename__ = "reinvestment"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="reinvestment")


class Opex(db.Model):
    __tablename__ = "opex"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="opex")


class Revenue(db.Model):
    __tablename__ = "revenue"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="revenue")


class TaxRevenue(db.Model):
    __tablename__ = "tax_revenue"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="tax_revenue")


class Vat(db.Model):
    __tablename__ = "vat"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="vat")


class PrivateRevenue(db.Model):
    __tablename__ = "private_revenue"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="private_revenue")


class PrivateCost(db.Model):
    __tablename__ = "private_cost"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="private_cost")


class BenefitComponent(db.Model):
    __tablename__ = "benefit_component"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Relationship (PK) one to many
    benefit = db.relationship("Benefit", back_populates="benefit_component")

    # Relationship many to one
    # Sector
    # unique=False
    sector_id = db.Column(db.Integer, db.ForeignKey("sector.id"))
    sector = db.relationship("Sector", back_populates="benefit_component")


class Benefit(db.Model):
    __tablename__ = "benefit"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # BenefitComponent
    # unique=False
    benefit_id = db.Column(db.Integer, db.ForeignKey("benefit_component.id"))
    benefit_component = db.relationship("BenefitComponent", back_populates="benefit")

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="benefit")


class Sector(db.Model):
    __tablename__ = "sector"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Relationship (PK) one to many
    benefit_component = db.relationship("BenefitComponent", back_populates="sector")
    # Relationship many to many
    # Project
    projects = db.relationship(
        "Project",
        secondary=project_sector,
        lazy="subquery",
        back_populates="sectors",
    )


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
