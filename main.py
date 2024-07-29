from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings("ignore")


import os
from src import app


server = app.create_app()


if __name__ == '__main__':
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    debug = 0 if os.getenv("FLASK_DEBUG") == "False" else 1
    server.run(host=host, port=port, debug=debug)
