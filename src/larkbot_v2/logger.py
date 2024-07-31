import logging

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    handlers=[RichHandler(rich_tracebacks=True)],
    format="%(message)s",
)

logger = logging.getLogger(__name__)
