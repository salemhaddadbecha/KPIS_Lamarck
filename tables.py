from sqlalchemy import Column, String, Integer, Boolean, Date, Float
from sqlalchemy.orm import relationship
from connectors.database_connectors import Base

class Candidats(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    boond_id = Column(Integer)
    # Attributs
    nom = Column(String)
    prenom = Column(String)
    date_de_creation = Column(Date)
    date_derniere_maj = Column(Date)
    provenance_cv = Column(String)
    commentaire_provenance_cv = Column(String)
    recrute = Column(Boolean)
    prise_de_contact = Column(Boolean)
    entretien_1 = Column(Boolean)
    entretien_2 = Column(Boolean)
    entretien_3 = Column(Boolean)
    signature = Column(Boolean)
    # RelationShip(s)
    boond_rm_id = Column(Integer)
    boond_ressource_id = Column(Integer)

class Ressources(Base):
    __tablename__ = 'ressources'
    id = Column(Integer, primary_key=True)
    boond_id = Column(Integer)
    # Attributs
    date_de_creation = Column(Date)
    nom = Column(String)
    prenom = Column(String)
    sexe = Column(String)
    agence = Column(String)
    etat = Column(String)
    profil = Column(String)
    type = Column(String)
    est_rm = Column(Boolean)
    date_de_recrutement = Column(Date)
    # RelationShip(s)
    boond_rm_id = Column(Integer)

class Besoins(Base):
    __tablename__ = 'besoins'
    id = Column(Integer, primary_key=True)
    boond_id = Column(Integer)
    # Attributs
    date_de_creation = Column(Date)
    etat = Column(String)
    date_maj_drae = Column(Date)
    est_interne = Column(Boolean)
    # RelationShip(s)
    boond_rm_id = Column(Integer)
    boond_contact_id = Column(Integer)

class Projets(Base):
    __tablename__ = 'projets'
    id = Column(Integer, primary_key=True)
    boond_id = Column(Integer)
    # Attributs
    date_de_debut = Column(Date)
    date_de_fin = Column(Date)
    # RelationShip(s)
    boond_rm_id = Column(Integer)
    boond_besoin_id = Column(Integer)

class Prestations(Base):
    __tablename__ = 'prestations'
    id = Column(Integer, primary_key=True)
    boond_id = Column(Integer)
    # Attributs
    date_de_debut = Column(Date)
    date_de_fin = Column(Date)
    etat = Column(String)
    ca_ht = Column(Float)
    ca_realise = Column(Float)
    ca_previsionnel = Column(Float)
    # RelationShip(s)
    boond_resource_id = Column(Integer)

class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    boond_id = Column(Integer)
    # Attributs
    nom = Column(String)
    prenom = Column(String)
    date_de_creation = Column(Date)
    provenance = Column(String)
    detail_provenance = Column(String)
    # RelationShip(s)
    boond_rm_id = Column(Integer)

class Actions(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    boond_id = Column(Integer)
    # Attributs
    date_de_creation = Column(Date)
    table_associee = Column(String)
    type = Column(String)
    # RelationShip(s)
    boond_id_element_associe = Column(Integer)

class Temps(Base):
    __tablename__ = 'temps'
    id = Column(Integer, primary_key=True)
    boond_id = Column(String)
    # Attributs
    date_de_creation = Column(Date)
    type = Column(String)
    duree = Column(Float)
    # RelationShip(s)
    boond_resource_id = Column(Integer)
    boond_id_projet = Column(Integer)


class Controle_qualite(Base):
    __tablename__ = 'controle_qualite'
    id = Column(Integer, primary_key=True)
    # Attributs
    defaut = Column(String)
    date_releve = Column(Date)
    est_corrige = Column(Boolean)
    # RelationShip(s)
    nom_table_correspondante = Column(String)
    id_correspondant = Column(Integer)
