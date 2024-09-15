# server

## server
sudo apt update
sudo apt install python3-pip git
sudo apt install python3-pip
pip3 install fastapi uvicorn
sudo apt install uvicorn
git clone https://github.com/jejudatavisualization/server.git
cd server
pip3 install -r requirements.txt
cd app
<!-- nohup uvicorn main:app --host 0.0.0.0 --port 8000 & -->
sudo nohup uvicorn main:app --host 0.0.0.0 --port 80 &


## local
cd server
.\vevn\Scripts\activate
pip3 install -r requirements.txt
cd app
uvicorn main:app --reload