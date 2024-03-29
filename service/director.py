from dao.director import DirectorDao
from dao.model.directors import Director
from schemas.base import DirectorSchema
from utilites.decorators import handling_exceptions

class DirectorService:
    def __init__(self, director_dao: DirectorDao):
        self.director_dao = director_dao

    @handling_exceptions
    def get_director_all(self, param):
        if "page" in param:
            result = self.director_dao.get_all(param["page"])
        else:
            result = self.director_dao.get_all()
        if result:
            return DirectorSchema(many=True).dump(result), 200
        else:
            return {"message": "Directors into database not found"}, 404

    @handling_exceptions
    def get_director(self, did):
        result = self.director_dao.get_one(did)
        if result:
            return DirectorSchema().dump(result), 200
        else:
            return {"message": f"Genre with ID: '{did}' not found"}, 404

    @handling_exceptions
    def add_director(self, data):
        director_dict = DirectorSchema().load(data)
        director = Director(**director_dict)
        self.director_dao.create(director)

        return {"message": f"director {Director.name} added into database"}, 201

    @handling_exceptions
    def update(self, data, did):

        director_dict = DirectorSchema().load(data)
        self.director_dao.update(director_dict, did)
        return {"message": f"Director with ID: '{did}' is updated"}, 204

    @handling_exceptions
    def delete(self, did):
        self.director_dao.delete(did)
        return {"message": f"Director with ID: '{did}' is deleted"}, 204
