from modules.logger import Logger
import subprocess
logger = Logger('setup').get_logger()
logger.info('Установка зависимостей..')
try:
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except Exception as e:
    logger.critical('Произошла ошибка во время установки зависимостей: ' + str(e))
    exit()

import yaml
from Example import app
import time

# Чтения конфига
logger.info('Чтение конфига..')
with open('config.yml', 'r') as file:
    _config = yaml.safe_load(file)

host = str(_config['server']['host'])
port = str(_config['server']['port'])
autostart = _config['setup']['autostart']

# Gunicorn
if not autostart:
    with open('example.txt', 'w') as f:
        f.write(f'gunicorn -w 4 -b {host}:{port} app:app --access-logfile logs/gunicorn/access.log --error-logfile logs/gunicorn/error.log')
logger.info('Запуск сервера с Gunicorn..')

try:
    from gunicorn.app.base import BaseApplication
    class App(BaseApplication):
        def __init__(self, app, options=None):
            self.application = app
            self.options = options or {}
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key, value)

        def load(self):
            return self.application
    options = {
        'bind': host + ':' + port,
        'accesslog': 'logs/gunicorn/access.log',  # Файл доступа
        'errorlog': 'logs/gunicorn/error.log',  # Файл ошибок
    }
    App(app, options).run()
except Exception as e:
    logger.error('Gunicorn: ' + str(e))
    logger.warning("Запускаю альтернативный Flask сервер..")
    time.sleep(2)
    app.run(host=host, port=int(port), debug=False)