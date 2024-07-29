from dotenv import load_dotenv
load_dotenv()

import unittest, os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import app
from src.extensions.flask_sqlalchemy import db
from src.models.usersmodel import UserModel
from src.models.vehiclesmodel import VehicleModel

class TestUserRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_vehicles_test.db'
        cls.app = app.create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.create_all()
        self.token = None

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """
        :description: Test create user
        """
        user_data = {
            "name": "MSX",
            "email": "msx@exemple.com",
            "password": "123456"
        }
        response = self.client.post('/api/users/register/', json=user_data)
        self.assertEqual(response.status_code, 201)

    def test_user_already_exists(self):
        """
        :description: Test user already exists
        """
        self.test_create_user()

        user_data = {
            "name": "MSX",
            "email": "msx@exemple.com",
            "password": "123456"
        }
        response = self.client.post('/api/users/register/', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'User already exists')

    def test_login_user(self):
        """
        :description: Test login user
        """
        self.test_create_user()

        user_data = {
            "email": "msx@exemple.com",
            "password": "123456"
        }
        response = self.client.post('/api/users/login/', json=user_data)
        self.assertEqual(response.status_code, 200)
        self.token = response.json.get('access_token')

    def test_login_credentials_invalid(self):
        """
        :description: Test login credentials invalid
        """
        self.test_create_user()

        user_data = {
            "email": "msx@exemple.com",
            "password": "1234568"
        }
        response = self.client.post('/api/users/login/', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid credentials')

    def test_create_vehicle(self):
        """
        :description: Test create vehicle
        """
        self.test_login_user()

        vehicle_data ={
            "chassi": "12345678901234567",
            "renavam": "12345678901",
            "plate": "ABC1234",
            "brand": "GM",
            "model": "Spin",
            "year": "2024",
            "color": "Branca",
            "price": 120000,
            "connected": True
        }
        response = self.client.post('/api/vehicles/', json=vehicle_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)

    def test_list_vehicles(self):
        """
        :description: Test list vehicles
        """
        self.test_create_vehicle()

        response = self.client.get('/api/vehicles/', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)

    def test_get_vehicle(self):
        """
        :description: Test get vehicle
        """
        self.test_create_vehicle()

        response = self.client.get('/api/vehicles/1/', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)

    def test_edit_vehicle(self):
        """
        :description: Test edit vehicle
        """
        self.test_create_vehicle()

        vehicle_data = {
            "connected": False
        }
        response = self.client.patch('/api/vehicles/1/', json=vehicle_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('vehicle').get('connected'), False)

    def test_delete_vehicle(self):
        """
        :description: Test delete vehicle
        """
        self.test_create_vehicle()

        response = self.client.delete('/api/vehicles/1/', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 204)

    def test_vehicle_not_found(self):
        """
        :description: Test vehicle not found
        """
        self.test_create_vehicle()

        response = self.client.get('/api/vehicles/2/', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 404)

    def test_unauthorized(self):
        """
        :description: Test unauthorized
        """
        self.test_create_vehicle()

        response = self.client.get('/api/vehicles/')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()