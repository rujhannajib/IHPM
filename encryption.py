import getpass 
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- Part A: Setting the Master Password ---
def derive_key(password, salt):
    """Generates encyption key"""

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=250000, # Increased iterations for better security
    )

    # Return the salt and the key (hash) for storage
    return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))


# --- Part B: Verifying the Master Password ---
def verify_master_password(stored_salt, stored_key, password_to_check):
    """Hashes the password to check and compares it to the stored key."""
    # Use the same salt and iterations to hash the password attempt

    key_to_check = derive_key(password_to_check, stored_salt)
    
    # Compare the new key with the stored key
    if key_to_check == stored_key:
        return True, key_to_check
    else:
        return False, ""


def register_new_user(conn, cursor):
    """Register new user"""
    try:
        my_username = input("Enter a username: ")
        my_password = getpass.getpass("Enter a password: ")
        stored_salt = os.urandom(16)
        stored_key = derive_key(my_password, stored_salt)

        add_password_sql = f"""
        INSERT INTO users (id, username, salt, hash) VALUES (NULL, %s, %s, %s)
        """

        cursor.execute(add_password_sql, (my_username, stored_salt, stored_key))

        conn.commit()

        return True, derive_key(my_password, stored_salt)
    except Exception as e:
        print(f"Register new user: An error occured: {e}")
        return False, ""
    

def login(conn, cursor):
    """Login for existing user"""
    try:
        my_username = input("Enter a username: ")
        my_password = getpass.getpass("Enter a password: ")

        select_password_sql = f"""
        SELECT * FROM users WHERE username = '{my_username}'
        """

        cursor.execute(select_password_sql)
        res = cursor.fetchone()
        if res:
            access, key = verify_master_password(res[2], res[3], my_password)
            return access, key
        raise Exception("User not found")
    except Exception as e:
        print(f"User is not verified:{e}")
        return False, ""
    
