import pymysql

# Configuration for RDS connection
rds_host = "mysql-ssa-1.c3uztxubh3hp.us-east-2.rds.amazonaws.com"
db_username = "photoapp-read-write"
db_password = "def456!!"
db_name = "weatherapp"

def lambda_handler(event, context):
    # Extract the username from the event
    username = event['username']
    
    # Establish a connection to the RDS instance
    connection = pymysql.connect(host=rds_host,
                                 user=db_username,
                                 password=db_password,
                                 database=db_name)
    
    try:
        with connection.cursor() as cursor:
            # Check if the username exists in the table
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            
            if cursor.fetchone():
                return "Username already exists"
            
            # If username does not exist, insert it into the table
            insert_query = "INSERT INTO users (username) VALUES (%s)"
            cursor.execute(insert_query, (username,))
            connection.commit()
            
            return "Username added successfully"
    
    except Exception as e:
        print("Error:", str(e))
        return "Error occurred"
    
    finally:
        connection.close()