from alembic import command
from alembic.config import Config
import os

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    script_dir = os.path.join(os.path.dirname(__file__), "alembic")
    alembic_cfg.set_main_option("script_location", script_dir)
    command.upgrade(alembic_cfg, "head")