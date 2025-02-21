#bin/bash
source printer/bin/activate
pip install -r requirements.txt
sudo docker compose up -d
nohup python3 app.py  > api.log &