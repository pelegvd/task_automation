git clone https://github.com/pelegvd/task_automation.git
cd task_automation
python3 -m venv venv
source venv/bin/activate     # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest -s -v main.py
