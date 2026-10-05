import hashlib
import hmac
import os
import sqlite3


DATABASE_NAME = os.getenv(
    "POCKETSMART_DATABASE",
    "pocketsmart.db"
)


def get_connection():
    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            monthly_income REAL NOT NULL,
            rent REAL NOT NULL,
            food REAL NOT NULL,
            transport REAL NOT NULL,
            utilities REAL NOT NULL,
            education REAL NOT NULL,
            healthcare REAL NOT NULL,
            entertainment REAL NOT NULL,
            other REAL NOT NULL,
            savings_goal REAL NOT NULL,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()

    connection.close()


def hash_password(password: str) -> str:

    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        120000
    )

    return (
        f"{salt.hex()}${digest.hex()}"
    )


def verify_password(
    password: str,
    stored_hash: str
) -> bool:

    try:

        salt_hex, digest_hex = (
            stored_hash.split("$", 1)
        )

        salt = bytes.fromhex(
            salt_hex
        )

        expected = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            120000
        )

        return hmac.compare_digest(
            expected.hex(),
            digest_hex
        )

    except (ValueError, TypeError):

        return False


def create_user(
    name: str,
    email: str,
    password: str
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                name.strip(),
                email.strip().lower(),
                hash_password(password)
            )
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:

        return None

    finally:

        connection.close()


def get_user_by_email(email: str):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (
            email.strip().lower(),
        )
    ).fetchone()

    connection.close()

    return row


def get_user_by_id(user_id: int):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return row


def save_budget(
    user_id: int,
    data: dict,
    recommendation: str
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO budgets (
            user_id,
            monthly_income,
            rent,
            food,
            transport,
            utilities,
            education,
            healthcare,
            entertainment,
            other,
            savings_goal,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            data["monthly_income"],
            data["rent"],
            data["food"],
            data["transport"],
            data["utilities"],
            data["education"],
            data["healthcare"],
            data["entertainment"],
            data["other"],
            data["savings_goal"],
            recommendation
        )
    )

    connection.commit()

    budget_id = cursor.lastrowid

    connection.close()

    return budget_id


def get_user_budgets(user_id: int):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM budgets
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return rows
