from sqlalchemy import create_engine, text
import os

# Retrieve the database connection string from an environment variable
db_conn = os.getenv('DB_CONN')

# Remove unwanted quotes from the db_conn variable
if db_conn is not None:
    db_conn = db_conn.replace('"', '')

print("DB_CONN:", repr(db_conn))

if db_conn is None:
    print("DB_CONN environment variable is not set.")
else:
    # Establish a connection to the database
    engine = create_engine(db_conn)

def login_user(username, password):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM User WHERE user_name = :username AND user_password = :password"),
            {"username": username, "password": password}
        )
        record = result.fetchone()

    if record:
        user_info = {
            'id': record[0],
            'username': record[1],
            'is_admin': record[5]
        }
        return user_info
    else:
        return None

def get_user_info(user_id=None):
    with engine.connect() as connection:
        if user_id:
            result = connection.execute(
                text("SELECT * FROM User WHERE id = :user_id"),
                {"user_id": user_id}
            )
            record = result.fetchone()
            if record:
                user_info = {
                    'id': record[0],
                    'username': record[1],
                    'department': record[4],
                    'email': record[2]
                }
                return user_info
            else:
                return None
        else:
            result = connection.execute(
                text("SELECT * FROM User")
            )
            users = result.fetchall()

            user_info_list = []
            for record in users:
                user_info = {
                    'id': record[0],
                    'username': record[1],
                    'department': record[4],
                    'email': record[2]
                }
                user_info_list.append(user_info)

            return user_info_list

