
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