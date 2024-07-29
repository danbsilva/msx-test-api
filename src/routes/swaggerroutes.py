from src.controllers.swaggercontroller import SwaggerResource, SwaggerUIResource

class SwaggerRoutes:

    def __init__(self, api):

        api.add_resource(SwaggerResource, '/swagger.json',
                         methods=['GET'], endpoint='swagger')
        api.add_resource(SwaggerUIResource, '/docs/',
                         methods=['GET'])
