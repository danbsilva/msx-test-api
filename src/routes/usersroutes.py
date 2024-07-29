from src.controllers.authcontroller import UsersResource, UserLoginResource

class UsersRoutes:

    def __init__(self, api):

        prefix = '/users'

        api.add_resource(UsersResource, f'/{prefix}/register/',
                         methods=['POST'])
        api.add_resource(UserLoginResource, f'/{prefix}/login/',
                         methods=['POST'])



