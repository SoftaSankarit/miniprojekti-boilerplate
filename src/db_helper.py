from sqlalchemy import text
from config import db, app

SCHEMA_FILE = "schema.sql"

def execute_sql_file(file_path):
    with open(file_path, "r") as file:
        sql_commands = file.read()
    with db.session.begin():
        for command in sql_commands.split(";"):
            if command.strip():
                db.session.execute(text(command))

def reset_db():
    print("Resetting database...")
    sql = text("TRUNCATE TABLE reference CASCADE")
    db.session.execute(sql)
    db.session.commit()

def setup_db():
    print("Setting up database using schema.sql")
    execute_sql_file(SCHEMA_FILE)

if __name__ == "__main__":
    with app.app_context():
        setup_db()
