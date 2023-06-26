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
    # Perform the database query to retrieve file information
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT file_number, date_added, category, ref_num, title, status FROM file")
        )

        # Create a list to store the file information
        files = []

        # Iterate over the query result and extract the file information
        for record in result:
            file_info = {
                'file_number': record[0],
                'date_added': record[1],
                'category': record[2],
                'ref_num': record[3],
                'title': record[4],
                'status': record[5]
            }
            files.append(file_info)

        return files


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
        print("Date Added:", file['date_added'])
        print("Category:", file['category'])
        print("Reference Number:", file['ref_num'])
        print("Title:", file['title'])
        print("Status:", file['status'])
        print()
