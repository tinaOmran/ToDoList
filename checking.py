from sqlalchemy import text
from db.session import engine

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    )
    print([row[0] for row in result])
