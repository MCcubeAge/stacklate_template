import logging
import os

class Logger:
    def __init__(self, name):
        logs_dir = os.path.join(os.getcwd(), 'logs')

        # Create logs directory if it doesn't exist
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,  # Set default logging level
            datefmt='%d-%m-%Y %H:%M',
            handlers=[]
        )

        # Custom formatter for other levels
        other_formatter = logging.Formatter('%(asctime)s | %(name)s | [%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M')

        # Create handler for debug level file logs
        debug_handler = logging.FileHandler(os.path.join(logs_dir, 'debug_logs.txt'), encoding='utf-8')
        debug_handler.setLevel(logging.DEBUG)  # Set logging level DEBUG for debug file
        debug_handler.setFormatter(other_formatter)
        logging.getLogger().addHandler(debug_handler)

        # Create handler for file logs
        file_handler = logging.FileHandler(os.path.join(logs_dir, 'logs.txt'), encoding='utf-8')
        file_handler.setLevel(logging.INFO)  # Set logging level INFO for file
        file_handler.setFormatter(other_formatter)
        logging.getLogger().addHandler(file_handler)

        # Create handler for console logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Set logging level INFO for console
        console_handler.setFormatter(other_formatter)
        logging.getLogger().addHandler(console_handler)

        self.logger = logging.getLogger(name)

    def get_logger(self):
        return self.logger