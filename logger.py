import logging
import os
from logging.handlers import RotatingFileHandler
from Config import Configurations


class LogConfig:

    def __init__(self):
        self.file_path = './logs/%s.log' % Configurations.get_configurations()['LogName']
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self._setup_log_configs()

    def _setup_log_configs(self):
        logging_handler = RotatingFileHandler(
            self.file_path, maxBytes=int(1e7), backupCount=2
        )
        logging.basicConfig(
            level=logging.INFO,
            handlers=[logging_handler],
            datefmt="%Y-%m-%d %H:%M:%S",
            format='%(asctime)s - DLPExporter - %(levelname)s - %(message)s',
        )
