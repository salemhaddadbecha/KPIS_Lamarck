#Configure EC2 time:
timedatectl #check time zobe
sudo timedatectl set-timezone Europe/Paris

mkdir logs
#Give access to write in the log
chmod 755 /home/ec2-user/kpis/logs

#Crontab to schedule jobs:
crontab -e
*/5 * * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1

40 20 * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1
TZ=Europe/Paris

21 13 * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1

#Copy from Local to EC2 instance
scp -i  C:\Users\salem\PycharmProjects\kpis\kpisinstance.pem -r  C:\Users\salem\PycharmProjects\kpis ec2-user@34.238.150.105:/home/ec2-user

47 * * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1




