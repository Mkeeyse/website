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
            text("SELECT * FROM User WHERE username = :username AND password = :password"),
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

def get_file_info():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM file"))
        files = result.fetchall()

        file_info_list = []
        for record in files:
            file_info = {
                'file_number': record[0],
                'user_id': record[1],
                'date_added': record[2],
                'category': record[3],
                'sub_category': record[4],
                'ref_num': record[5],
                'title': record[6],
                'status': record[7]
            }
            file_info_list.append(file_info)

        return file_info_list

# Test the functions
if __name__ == '__main__':
    print("DB_CONN:", repr(db_conn))

    # Test user information retrieval
    print("Users:")
    users = get_user_info()
    for user in users:
        print("ID:", user['id'])
        print("Username:", user['username'])
        print("Department:", user['department'])
        print("Email:", user['email'])
        print()

    # Test file information retrieval
    print("Files:")
    files = get_file_info()
    for file in files:
        print("File Number:", file['file_number'])
        print("User ID:", file['user_id'])
        print("Date Added:", file['date_added'])
        print("Category:", file['category'])
        print("Sub Category:", file['sub_category'])
        print("Reference Number:", file['ref_num'])
        print("Title:", file['title'])
        print("Status:", file['status'])
        print()
