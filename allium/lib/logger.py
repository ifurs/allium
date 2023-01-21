# TODO: define debugger
import logging


logging.basicConfig(
    filename="allium.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logging.info("Running Allium parser")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger = logging.getLogger("allium")
logger.addHandler(console_handler)

# debugger = logging.getLogger("allium-debug")
