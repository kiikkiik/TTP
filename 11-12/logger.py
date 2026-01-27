import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filename="bot.log"
)

def log(msg):
    logging.info(msg)
    print(f"[LOG] {msg}")

def error(msg):
    logging.error(msg)
    print(f"[ERROR] {msg}")