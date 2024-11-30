from sqlalchemy import text
from config import db, app

TABLE_NAME = "books"

def table_exists(name):
    sql_table_existence = text(
      "SELECT EXISTS ("
      "  SELECT 1"
      "  FROM information_schema.tables"
      f" WHERE TABLE_NAME = '{name}'"
      ")"
    )

    print(f"Checking if table {name} exists")
    print(sql_table_existence)

    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]

def reset_db():
    print(f"Clearing contents from table {TABLE_NAME}")
    sql = text(f"DELETE FROM {TABLE_NAME}")
    db.session.execute(sql)
    db.session.commit()

def setup_db():
    if table_exists(TABLE_NAME):
        print(f"Table {TABLE_NAME} exists, dropping")
        sql = text(f"DROP TABLE {TABLE_NAME}")
        db.session.execute(sql)
        db.session.commit()

    # VARCHAR(100) laittaa maksimi pituuden ja NOT NULL kieltää sen olemast tyhjä
    print(f"Creating table {TABLE_NAME}")
    sql = text(
        f"CREATE TABLE {TABLE_NAME} ("
        "  id SERIAL PRIMARY KEY, "
        "  author VARCHAR(100) NOT NULL, "
        "  title VARCHAR(100) NOT NULL, "
        "  publisher VARCHAR(100) NOT NULL, "
        "  year INTEGER NOT NULL"


        "  volume VARCHAR(100), "
        "  series VARCHAR(100), "
        "  address VARCHAR(100), "
        "  edition VARCHAR(100), "
        "  month VARCHAR(100), "
        "  note TEXT, "
        "  key VARCHAR(100), "
        "  url VARCHAR(100)"
        ")"
    )

    db.session.execute(sql)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
