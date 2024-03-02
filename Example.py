import os

from flask import Flask, session
from flask_compress import Compress

app = Flask(__name__)
app.secret_key = os.urandom(24)
Compress(app)
app.template_folder = 'views'
app.static_folder = 'public'

for file in os.listdir('routes'):
    if file.endswith('.py') and file != '__init__.py':
        module = file.split('.')[0]
        mod = __import__('routes.' + module, fromlist=[module])
        app.register_blueprint(getattr(mod, module + '_bp'))

for file in os.listdir('api'):
    if file.endswith('.py') and file != '__init__.py':
        module = file.split('.')[0]
        mod = __import__('api.' + module, fromlist=[module])
        app.register_blueprint(getattr(mod, module + '_bp'), url_prefix='/api')