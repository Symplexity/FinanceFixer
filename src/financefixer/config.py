from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PROD_PATH = BASE_DIR / "data" / "financefixer.db"
DB_TEST_PATH = BASE_DIR / "data" / "financefixer_test.db"

DB_PATH = DB_TEST_PATH
