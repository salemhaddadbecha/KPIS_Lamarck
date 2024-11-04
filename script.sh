mkdir logs

crontab -e
*/5 * * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1

15 48 * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1


21 00 * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1


scp -i  C:\Users\salem\PycharmProjects\kpis\kpisinstance.pem -r  C:\Users\salem\PycharmProjects\kpis ec2-user@34.238.150.105:/home/ec2-user

21 35 * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py

