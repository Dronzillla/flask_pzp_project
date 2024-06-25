from blueprintapp.app import db


# Association Table for Many-to-Many Relationship
# Project - Sector
project_sector = db.Table(
    "project_sector",
    db.Column(
        "project_id",
        db.Integer,
        db.ForeignKey("project.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "sector_id",
        db.Integer,
        db.ForeignKey("sector.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    code = db.Column(db.String(80), nullable=False, unique=True)

    # Relationships (PK) one to one
    # uselist=False
    general = db.relationship(
        "General", uselist=False, back_populates="project", cascade="all, delete-orphan"
    )
    ratios = db.relationship(
        "Ratios", uselist=False, back_populates="project", cascade="all, delete-orphan"
    )
    # Relationships (PK) one to many
    cashflow = db.relationship(
        "Cashflow", back_populates="project", cascade="all, delete-orphan"
    )
    benefit = db.relationship(
        "Benefit", back_populates="project", cascade="all, delete-orphan"
    )
    harm = db.relationship(
        "Harm", back_populates="project", cascade="all, delete-orphan"
    )
    # Relationships Many to many
    # Sector
    sectors = db.relationship(
        "Sector",
        secondary=project_sector,
        lazy="subquery",
        back_populates="projects",
        # cascade="all, delete",
    )


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
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"), unique=True
    )
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
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"), unique=True
    )
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
    project_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    project = db.relationship("Project", back_populates="cashflow")


class BenefitComponent(db.Model):
    __tablename__ = "benefit_component"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Relationship (PK) one to many
    benefit = db.relationship("Benefit", back_populates="benefit_component")


class Benefit(db.Model):
    __tablename__ = "benefit"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # BenefitComponent
    # unique=False
    benefit_id = db.Column(
        db.Integer, db.ForeignKey("benefit_component.id", ondelete="CASCADE")
    )
    benefit_component = db.relationship("BenefitComponent", back_populates="benefit")

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    project = db.relationship("Project", back_populates="benefit")


class HarmComponent(db.Model):
    __tablename__ = "harm_component"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Relationship (PK) one to many
    harm = db.relationship("Harm", back_populates="harm_component")


class Harm(db.Model):
    __tablename__ = "harm"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    year = db.Column(db.Integer)

    # Relationship many to one
    # HarmComponent
    # unique=False
    harm_id = db.Column(
        db.Integer, db.ForeignKey("harm_component.id", ondelete="CASCADE")
    )
    harm_component = db.relationship("HarmComponent", back_populates="harm")

    # Relationship many to one
    # Project
    # unique=False
    project_id = db.Column(db.Integer, db.ForeignKey("project.id", ondelete="CASCADE"))
    project = db.relationship("Project", back_populates="harm")


class Sector(db.Model):
    __tablename__ = "sector"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Relationship many to many
    # Project
    projects = db.relationship(
        "Project",
        secondary=project_sector,
        lazy="subquery",
        back_populates="sectors",
    )
