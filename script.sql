ALTER TABLE projets ADD COLUMN company_name VARCHAR;
ALTER TABLE temps ADD COLUMN first_name VARCHAR;
ALTER TABLE TEMPS ADD COLUMN last_name VARCHAR;
-- Table: candidates
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    nom VARCHAR,
    prenom VARCHAR,
    date_de_creation DATE,
    date_derniere_maj DATE,
    provenance_cv VARCHAR,
    commentaire_provenance_cv VARCHAR,
    recrute BOOLEAN,
    prise_de_contact BOOLEAN,
    entretien_1 BOOLEAN,
    entretien_2 BOOLEAN,
    entretien_3 BOOLEAN,
    signature BOOLEAN,
    agence VARCHAR,
    boond_rm_id INTEGER,
    boond_ressource_id INTEGER
);

-- Table: ressources
CREATE TABLE ressources (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    date_de_creation DATE,
    nom VARCHAR,
    prenom VARCHAR,
    sexe VARCHAR,
    agence VARCHAR,
    etat VARCHAR,
    profil VARCHAR,
    type VARCHAR,
    est_rm BOOLEAN,
    date_de_recrutement DATE,
    debut_derniere_prestation DATE,
    fin_derniere_prestation DATE,
    boond_rm_id INTEGER
);

-- Table: besoins
CREATE TABLE besoins (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    date_de_creation DATE,
    etat VARCHAR,
    date_maj_drae DATE,
    est_interne BOOLEAN,
    boond_rm_id INTEGER,
    boond_contact_id INTEGER
);

-- Table: projets
CREATE TABLE projets (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    date_de_debut DATE,
    date_de_fin DATE,
    boond_rm_id INTEGER,
    boond_besoin_id INTEGER,
    company_name VARCHAR(255),
    company_id INTEGER(255)
);

-- Table: prestations
CREATE TABLE prestations (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    date_de_debut DATE,
    date_de_fin DATE,
    etat VARCHAR,
    ca_ht FLOAT,
    ca_realise FLOAT,
    ca_previsionnel FLOAT,
    boond_resource_id INTEGER
);

-- Table: contacts
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    nom VARCHAR,
    prenom VARCHAR,
    date_de_creation DATE,
    provenance VARCHAR,
    detail_provenance VARCHAR,
    boond_rm_id INTEGER,
    derniere_modification DATE
);

-- Table: actions
CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    date_de_creation DATE,
    table_associee VARCHAR,
    type VARCHAR,
    boond_id_element_associe INTEGER
);

-- Table: temps
CREATE TABLE temps (
    id SERIAL PRIMARY KEY,
    boond_id VARCHAR,
    date_de_creation DATE,
    type VARCHAR,
    duree FLOAT,
    boond_resource_id INTEGER,
    boond_id_projet INTEGER
);

-- Table: controle_qualite
CREATE TABLE controle_qualite (
    id SERIAL PRIMARY KEY,
    defaut VARCHAR,
    date_releve DATE,
    est_corrige BOOLEAN,
    nom_table_correspondante VARCHAR,
    id_correspondant INTEGER
);

-- Table: all_actions
CREATE TABLE all_actions (
    id SERIAL PRIMARY KEY,
    boond_id INTEGER,
    date_de_creation DATE,
    table_associee VARCHAR,
    type VARCHAR,
    boond_id_element_associe INTEGER
);

--table company
CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    boond_id INT,
    boond_rm_id INT,
    company_name VARCHAR(255),
    country VARCHAR(255),
    phone VARCHAR(255)
);
