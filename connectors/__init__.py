from connectors.database_connectors import ENGINE, Base
"""
from tables import (
    Candidats,
    Ressources,
    Besoins,
    Projets,
    Prestations,
    Contacts,
    Actions,
    Temps,
    Controle_qualite
)
"""
def migrate_database():
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)

if __name__ == '__main__':
    migrate_database()

#migrate_database()