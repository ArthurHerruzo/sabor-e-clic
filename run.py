from flask import Flask
from app.database import close_db

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'sabor_clic_secret_key_2026'

if __name__ == '__main__':
    app.run(debug=True, port=5000)