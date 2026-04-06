import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

def log_command(user_id, username, command, args):
    logger.info(f"User {user_id} (@{username}) used /{command} {args}")