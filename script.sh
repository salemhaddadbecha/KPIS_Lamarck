mkdir logs

crontab -e
*/5 * * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1

15 48 * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1

15 48 * * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1

00 00 * * * ENV=production /usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1