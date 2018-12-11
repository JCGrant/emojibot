from flask import Flask

app = Flask(__name__, template_folder="../client/build", static_folder="../client/build/static")
app.config['SECRET_KEY'] = "Super Secret"

import views
