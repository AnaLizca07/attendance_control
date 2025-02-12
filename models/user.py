from zk import const

class User:
    @staticmethod
    def get_users_info(conn):
        users_info = {}
        users = conn.get_users()
        for user in users:
            users_info[user.user_id] = {
                'user_id': user.user_id,
                'name': user.name,
                'privilege': 'Admin' if user.privilege == const.USER_ADMIN else 'User'
            }
        return users_info