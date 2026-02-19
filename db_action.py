import pandas as pd

def user_existed(conn, cursor, user):
    '''
    Return true if user is already registered
    '''
    all_users_sql = f"""
        SELECT username FROM users
        """
    cursor.execute(all_users_sql)
    res = [i[0] for i in cursor.fetchall()]
    return user in res

def platform_existed(conn, cursor, platform):
    '''
    Return true if platform is already registered
    '''
    all_platforms_sql = f"""
        SELECT platform FROM cred
        """
    cursor.execute(all_platforms_sql)
    res = [i[0] for i in cursor.fetchall()]
    return platform in res

def export_password(conn, cursor):
    # Read directly to DataFrame and export
    df = pd.read_sql("SELECT * FROM cred", conn)
    df.to_csv('passwords.csv', index=False)

    print(f"Exported {len(df)} rows to passwords.csv")

