from flask_restful import Api

from src.routes import usersroutes, vehiclesroutes, swaggerroutes

api = Api(prefix='/api')


def init_app(app):
    api.init_app(app)

# Endpoints for users
usersroutes.UsersRoutes(api)

# Endpoints for vehicles
vehiclesroutes.VehiclesRoutes(api)

# Endpoints for swagger
swaggerroutes.SwaggerRoutes(api)

