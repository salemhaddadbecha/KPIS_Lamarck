# Automatisation ETL avec AWS et BoondManager API  

Ce projet met en œuvre une solution ETL (Extraction, Transformation, Chargement) automatisée en utilisant AWS et des scripts Python pour extraire des données de l'API BoondManager, les transformer et les charger dans une base de données cloud AWS RDS PostgreSQL.  

---

## 🌐 Architecture  

### 1. **Source de Données - API**  
Les données sont récupérées depuis l'API BoondManager via des scripts Python.  

### 2. **Base de Données Cloud**  
Les données transformées sont stockées dans une base AWS RDS PostgreSQL, accessible pour la génération de rapports via Power BI.  

### 3. **Déploiement des Scripts**  
Les scripts Python sont déployés sur une instance AWS EC2.  

### 4. **Automatisation ETL avec AWS**  
Un processus automatisé est configuré avec :  
- **AWS Lambda** et **EventBridge** pour :  
  - Démarrer les instances RDS et EC2.  
  - Exécuter les scripts Python pour traiter les données hebdomadaires ou mensuelles.  
  - Arrêter les instances une fois le traitement terminé.  

### 5. **Reporting**  
Power BI se connecte directement à AWS RDS PostgreSQL pour générer des tableaux de bord dynamiques.  

---

## ✅ Prérequis  

### 1. **Infrastructure AWS**  
- Une instance EC2 avec les scripts déployés.  
- Une instance RDS PostgreSQL pour stocker les données.  
- AWS Lambda et EventBridge configurés pour automatiser les tâches.  

### 2. **Bibliothèques Python**  
- `boto3` pour interagir avec les services AWS.  
- Dépendances spécifiées dans le fichier `requirements.txt`.  

### 3. **Accès API BoondManager**  
- Clé API valide pour récupérer les données.  

---

## 🚀 Installation  

### 1. **Cloner le Dépôt**  
```bash
https://github.com/salemhaddadbecha/KPIS_Lamarck.git
cd KPIS_Lamarck
```
### 2. Configurer les Variables d'Environnement ###
Définir les identifiants AWS dans le fichier de configuration ou via des variables d’environnement.
### 3. Installer les Dépendances ###
Sur l'instance EC2 :
```bash
pip install --user -r requirements.txt
```
## 📜 Scripts ##
### 1. main.py ### 
Ce script exécute les tâches ETL :
- Détermine si c’est le dernier samedi du mois ou un autre samedi.
- Extrait les données, les transforme, et les charge dans AWS RDS.
- Arrête les instances RDS et EC2 une fois le processus terminé.
#### Usage : Le script est automatiquement exécuté par AWS Lambda via un appel SSM. ####

### 2. Fonction Lambda ### 
- Démarre les instances RDS et EC2.
- Exécute le script Python via AWS Systems Manager (SSM).
- Configure un job récurrent via EventBridge pour déclencher la fonction Lambda tous les samedis à 11 h.

### 🔄 Processus ETL ###
#### 1. Dernier samedi du mois  #### 
Le script traite toutes les données du mois précédent.

#### 2. Autres samedis #### 
Le script traite les données de la semaine écoulée.

### ⚙️ Automatisation #### 
L'automatisation repose sur plusieurs services AWS :
- AWS Lambda : Gestion du déclenchement des instances et de l'exécution des scripts.
- AWS EventBridge : Programmation des exécutions hebdomadaires.
- AWS Systems Manager (SSM) : Exécution des commandes sur l'instance EC2.

## Détails Techniques ##
### Chaîne de Connexion RDS ###
Assurez-vous de configurer correctement la chaîne de connexion pour accéder à la base de données depuis les scripts Python et Power BI.

####  Exemple de Commande SSM #### 
```bash
export ENV=production && /usr/local/bin/python3.8 -m pip install --user -r /home/ec2-user/kpis/requirements.txt && /usr/local/bin/python3.8 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +%Y%m%d_%H%M%S).log 2>&1
```
### 🔑 Contrôle des Accès IAM ###
- Cette configuration IAM permet à l'instance EC2 d'interagir uniquement avec les ressources nécessaires, réduisant ainsi le risque d'accès non autorisé ou accidentel à d'autres services AWS.
- Elle permet aussi de gérer les rôles.

### 📈 Monitoring et Logs ### 
- Les journaux d'exécution sont enregistrés dans le répertoire logs de l'instance EC2.
- AWS CloudWatch peut être utilisé pour surveiller les exécutions et configurer des alertes en cas d’échec.
### 🌟 Améliorations Futures ### 
- Optimisation des performances avec des instances EC2 et RDS adaptées.
- Mise en œuvre de tests unitaires pour valider les transformations de données.
- Amélioration du contrôle qualité avec des KPI supplémentaires.


