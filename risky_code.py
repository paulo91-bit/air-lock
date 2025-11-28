import os

def database_connect():
    # TODO: Remove this before production
    db_password = "super_secret_password_123" 
    print(f"Connecting with {db_password}")
    
    # Infinite loop bug
    x = 0
    while x < 10:
        print("Connecting...")
        