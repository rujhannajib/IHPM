import getpass 
import encryption as enc
from cryptography.fernet import Fernet
import json
from sqlconfig import get_connection

# connect to db
conn = get_connection()
cursor = conn.cursor()

def display_menu():
    """Prints the main menu options."""
    print("\n--- Password Manager ---")
    print("1. Add a new password")
    print("2. Get a password")
    print("3. List all services")
    print("4. Delete a password")
    print("5. Quit")
    print("------------------------")

def add_password(fi, key):
    """Adds a new password entry to storage."""
    print("\n--- Add New Password ---")

    platform = input("Enter the service name (e.g., 'github'): ").lower()

    # check if password for the platform already existed
    command = f"""SELECT platform FROM cred"""
    cursor.execute(command)
    res = cursor.fetchall()
    existing_services = set()
    for i in res: existing_services.add(i[0])
    
    while platform in existing_services:
        platform = input("Service already existed. Enter different service name (e.g., 'github2'): ").lower()

    username = input(f"Enter your username for '{platform}': ")
    password = getpass.getpass("Enter the password: ")
    password2 = getpass.getpass("Re-enter the password: ")

    # ensure password entered correctly
    while (password != password2):
        print("The password does not match")
        password2 = getpass.getpass("Re-enter the password: ")

    # encrypting password
    password_entry = {"username": username, "password": password}
    data_to_encrypt = json.dumps(password_entry).encode('utf-8')
    encrypted_data = fi.encrypt(data_to_encrypt)
    print("Password Encrypted")

    try:
        command = f"""INSERT INTO cred (cred_id, platform, username, password, enckey) VALUES (NULL, %s, %s, %s, %s)"""
        cursor.execute(command, (platform, username, encrypted_data, key, ))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"\n❌ Error: A password for '{platform}' already exists.")
    except Exception as e:
        print(f"An error occcured: {e}")
    else:
        print(f"Successfully added password for '{platform}'.")




def get_password(fi, key):
    """Retrieves a password for a given service."""
    print("\n--- Get Password ---")
    platform = input("Enter the platform name to retrieve: ").lower()
    
    try:
        command = f"""SELECT * FROM cred WHERE platform = %s and enckey = %s"""
        cursor.execute(command, (platform, key, ))
        res = cursor.fetchone()
        if res:
            encrypted_data = res[3]
            decrypted_bytes = fi.decrypt(encrypted_data)
            retrieved_entry = json.loads(decrypted_bytes.decode('utf-8'))
            print(f"Service: {platform}")
            print(f"  Username: {res[2]}")
            print(f"  Password: {retrieved_entry["password"]}")
        else:
            print(f"Error: No password found for '{platform}'.")
    except Exception as e:
        print(f"An error occcured:{e}")

def delete_password(key):
    """Delete password in the database"""
    print("\n--- Delete Password ---")
    platform = input("Enter the platform name to delete: ").lower()

    try:
        command = f"""DELETE FROM cred WHERE platform = %s and enckey = %s"""
        cursor.execute(command, (platform, key, ))
        conn.commit()
        print(f"Password for {platform} is deleted")
    except Exception as e:
        print(f"An error occcured:{e}")



def list_services(fi, key):
    """Lists all the services stored."""
    try:
        command3 = f"""SELECT * FROM cred WHERE enckey = %s"""
        cursor.execute(command3, (key,))
        res = cursor.fetchall()
        if not res:
            print("Your password store is empty.")
            return
        print("You have passwords for the following services:")
        print("-----------------------------------------------------------------------")
        for service in res:
            encrypted_data = service[3]
            decrypted_bytes = fi.decrypt(encrypted_data)
            retrieved_entry = json.loads(decrypted_bytes.decode('utf-8'))
            print(f"Platform: {service[1]}, Name: {service[2]}, Email: {retrieved_entry["password"]}")
        print("-----------------------------------------------------------------------")
    except Exception as e:
        print(f"An error occcured:{e}")

def spinup(conn, cursor):
    """Initialize necessary tables"""
    # create user table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        salt BLOB NOT NULL,
        hash BLOB NOT NULL
    );
    """
    cursor.execute(create_table_sql)

    # create cred tables
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cred (
        cred_id INTEGER AUTO_INCREMENT PRIMARY KEY,
        platform TEXT NOT NULL,
        username TEXT NOT NULL,
        password BLOB NOT NULL,
        enckey TEXT NOT NULL
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    

# --- Main Program Loop ---
def main():
    """The main function to run the interactive menu."""
    encryption_key = None
    access = False

    q1 = input("New User (T/F): ")
    if q1.upper() == "T":
        spinup(conn, cursor)
        access, encryption_key = enc.register_new_user(conn, cursor)
    elif q1.upper() == "F":
        access, encryption_key = enc.login(conn, cursor)
    if not access:
        return
    
    # for encryption
    fernet_instance = Fernet(encryption_key)

    
    while access:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_password(fernet_instance, encryption_key)
        elif choice == '2':
            get_password(fernet_instance, encryption_key)
        elif choice == '3':
            list_services(fernet_instance, encryption_key)
        elif choice == "4":
            delete_password(encryption_key)
        elif choice == '5':
            print("\nGoodbye! 👋")
            break # Exit the while loop
        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()

