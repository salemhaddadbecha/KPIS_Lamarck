#https://repost.aws/knowledge-center/lambda-layer-simulated-docker
# Use Amazon Linux 2 as the base image
FROM amazonlinux:2
#1 Package des bibliothques
sudo docker run -v "$PWD":/var/task "amazon/aws-sam-cli-build-image-python3.8" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.8/site-packages/; exit"
sudo docker run -v "$PWD":/var/task "amazon/aws-sam-cli-build-image-python3.8" /bin/sh -c "pip install psycopg2-binary -t python/lib/python3.8/site-packages/; exit"
#Compresser le dossier
zip -r mypythonlibs.zip python > /dev/null
#Créer un secret Key du user IAM et configurer aws configure
#Publier la couche sous Lambda
aws lambda publish-layer-version   --layer-name mypythonlibs   --description "My python libs"   --zip-file fileb://mypythonlibs.zip   --compatible-runtimes "python3.8" "python3.10"
#Assigner la couche à la fonction Lambda pour qu'elle utilise les fonctions liéess
aws lambda update-function-configuration --layers arn:aws:lambda:us-east-1:577638363319:layer:mypythonlibs:2 --function-name

