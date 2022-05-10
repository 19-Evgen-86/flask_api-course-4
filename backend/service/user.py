from backend.dao.model.user import User
from backend.dao.user import UserDao
from backend.schemas.base import UserSchema
from backend.tools.decorators import handling_exceptions
from backend.tools.secure import get_hash, decode_token, compare_pwd


class UserService:

    def __init__(self, dao: UserDao):
        self.dao = dao

    @handling_exceptions
    def get(self, token: str):

        email = decode_token(token)["email"]
        result = self.dao.get(email)
        if result:
            return UserSchema().dump(result)
        else:
            return {"message": "Пользователь не найден"}

    @handling_exceptions
    def create(self, data):
        valid_user = UserSchema().load(data=data)
        valid_user["password"] = get_hash(valid_user["password"])
        user = User(**valid_user)
        self.dao.create(user)
        return {"message": "Пользователь создан"}

    @handling_exceptions
    def update(self, data):
        data_update = {}

        if data['method'] == "patch":
            email = decode_token(data['token'])["email"]
            if "name" in data:
                data_update['name'] = data['name']
            if 'surname' in data:
                data_update["surname"] = data["surname"]
            if 'favorite_genre' in data:
                data_update['favorite_genre'] = data['favorite_genre']
            self.dao.update(data_update, email)
            return {"message": "данные обновлены"}

        elif data['method'] == "put":
            email = decode_token(data['token'])["email"]
            # создаем хеш пароля переданного пользователем
            old_pwd = get_hash(data["old_password"])
            # получаем хэш пароля из базы
            user_pwd = self.dao.get_pwd(email)[0]
            # сравниваем полученные хеши
            if compare_pwd(user_pwd, old_pwd):
                # если они совпадают, то сохраняем новый пароль
                pwd = get_hash(data["new_password"])
                self.dao.update_pwd(pwd, email)
                return {"message": "пароль обновлен"}
            else:
                # если не совпадают возвращаем ошибку
                return {"error": "неверный пароль"}
        else:
            return {'error': "unknown error"}
