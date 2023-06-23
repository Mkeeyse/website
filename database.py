from sqlalchemy import create_engine, text

# Establish a connection
engine = create_engine(
    "mysql+mysqlconnector://642ky6svrnizgbjw53hg:pscale_pw_oqbUdqC2dOCT8CLH2XmWC2wydOeA4NH68tC5r0TCTSC@aws.connect.psdb.cloud/file_system?ssl_ca=/etc/ssl/cert.pem"
)

# Execute a test query
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM User"))
    rows = result.fetchall()

# Convert rows to a list of dictionaries
result_dict = [dict(row._mapping) for row in rows]

# Print the result
print(result_dict[0])
