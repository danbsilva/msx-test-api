from src.controllers.vehiclescontroller import VehiclesResource, VehicleResource

class VehiclesRoutes:

    def __init__(self, api):

        prefix = '/vehicles'

        api.add_resource(VehiclesResource, f'/{prefix}/',
                         methods=['POST', 'GET'])
        api.add_resource(VehicleResource, f'/{prefix}/<id>/',
                            methods=['GET', 'PATCH', 'DELETE'])



