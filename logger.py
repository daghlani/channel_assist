from balebot.utils.logger import Logger
from config.public import log_file
import logging

Logger.get_logger().setLevel(level=logging.ERROR)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG, filename=log_file)

logger = logging.getLogger(__name__)
