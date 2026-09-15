import sqlite3
from contextlib import contextmanager


# ---------- Connections and Cursors ----------

def get_connection():
    return sqlite3.connect("app.db")


# ---------- Creating a Table ----------

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT
        )
    """)
    conn.commit()   # commit() saves the change permanently to disk
    conn.close()    # always close the connection when you're done with it


# ---------- Parameterized Queries  ----------

def add_user(name: str, email: str, city: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, city) VALUES (?, ?, ?)",
        (name, email, city)
    )
    conn.commit()
    conn.close()


# ---------- Reading Data ----------

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, city FROM users")
    rows = cursor.fetchall()   # fetchall() pulls every matching row
    conn.close()
    return rows


def get_user_by_city(city: str):
    conn = get_connection()
    cursor = conn.cursor()
    # Still parameterized, even for SELECT - same injection risk applies
    cursor.execute("SELECT id, name, email FROM users WHERE city = ?", (city,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------- Transactions ----------
 

@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()       # all steps worked -> save everything
    except Exception:
        conn.rollback()     # something failed -> undo everything
        raise
    finally:
        conn.close()


def update_two_users_safely(user_id_1: int, new_city_1: str,
                             user_id_2: int, new_city_2: str):
    with transaction() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET city = ? WHERE id = ?", (new_city_1, user_id_1))
        cursor.execute("UPDATE users SET city = ? WHERE id = ?", (new_city_2, user_id_2))
        # if the second line crashes, the first update is rolled back too



# ---------- Running the SQLite Demo ----------
def run_sqlite_demo():
    create_table()
    try:
        add_user("Mona", "monamobeen@gmail.com", "Lahore")
        add_user("Mobeen", "mobeenmonaa@yahoo.com", "Islamabad")
    except sqlite3.IntegrityError:
        print("Users already exist - skipping insert")

    print("All users:", get_all_users())
    print("Users in Lahore:", get_user_by_city("Lahore"))


# ---------- SQLAlchemy (ORM) ----------
 

def run_sqlalchemy_demo():
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.orm import declarative_base, sessionmaker

    engine = create_engine("sqlite:///app_orm.db")  # separate demo file
    Base = declarative_base()

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        name = Column(String)
        email = Column(String, unique=True)
        city = Column(String)

    Base.metadata.create_all(engine)  # creates the table if it doesn't exist

    Session = sessionmaker(bind=engine)
    session = Session()

    # Add a user the ORM way (no SQL string at all)
    new_user = User(name="Zara", email="zara@example.com", city="Islamabad")
    session.add(new_user)
    session.commit()

    # Query the ORM way
    lahore_users = session.query(User).filter_by(city="Islamabad").all()
    for u in lahore_users:
        print(u.name, u.email, u.city)

    session.close()


if __name__ == "__main__":
    run_sqlite_demo() 
 