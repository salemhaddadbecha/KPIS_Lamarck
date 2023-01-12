from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import or_

from connectors.database_connectors import get_database_session
from tables import Candidats, Ressources, Contacts, AllActions, Projets


def get_last_week_updated_candidates():
    with get_database_session() as session:
        return session.query(Candidats).filter(
            Candidats.date_derniere_maj <= datetime.today().date()
        ).filter(
            Candidats.date_derniere_maj >= datetime.today().date() + timedelta(weeks=-1)
        ).all()


def get_all_candidates():
    with get_database_session() as session:
        return session.query(Candidats).all()


def get_all_resources():
    with get_database_session() as session:
        return session.query(Ressources).all()


def get_all_resources_consultant_interne_in_mission_or_intern():
    with get_database_session() as session:
        return session.query(Ressources).filter(
            Ressources.type == 'Consultant Interne'
        ).filter(
            or_(
                Ressources.etat == 'en mission',
                Ressources.etat == 'en interne'
            )
        ).all()


def get_all_contacts_updated_last_ten_days():
    with get_database_session() as session:
        return session.query(Contacts).filter(
            Contacts.derniere_modification > datetime.now().date() - timedelta(days=10)
        ).all()


def get_all_resource_as_dict():
    resources = get_all_resources()
    return {resource.boond_id: resource for resource in resources}


def get_candidates_actions_as_dict():
    with get_database_session() as session:
        actions = session.query(AllActions).filter(AllActions.table_associee == 'candidate').all()
        return {action.boond_id_element_associe: action for action in actions}


def get_all_projects():
    with get_database_session() as session:
        return session.query(Projets).all()


def get_projects_actions_as_dict():
    result = defaultdict(list)
    with get_database_session() as session:
        projects_actions = session.query(AllActions).filter(AllActions.table_associee == 'project').all()
        for project_action in projects_actions:
            result[project_action.boond_id_element_associe].append(project_action.type)
    return result


if __name__ == '__main__':
    x = get_all_contacts_updated_last_ten_days()
    print(x)