import logging
import os
import sys

# 1. Configurar carpetas y archivos
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "registro_jurassic.txt")

logger = logging.getLogger("jurassic_monitor")
logger.setLevel(logging.INFO)


if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Guardar en txt
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

class AsyncAdapter:
    def __init__(self, logger):
        self.logger = logger

    async def info(self, msg):
        self.logger.info(msg)

    async def warning(self, msg):
        self.logger.warning(msg)

    async def error(self, msg):
        self.logger.error(msg)

# Exportamos el adaptador para que processor.py crea que es asincrono
logger = AsyncAdapter(logger)