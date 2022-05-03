import requests
from flask_login import LoginManager, current_user

payload = {'license': '5ESA6'}

r = requests.get('https://dkja-carpool-app.herokuapp.com/scan/', params=payload)
print(r.url)