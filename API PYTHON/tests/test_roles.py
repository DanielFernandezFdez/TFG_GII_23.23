import unittest
import requests

class TestRolesExternos(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:5000" 
    Rol_ID = None
    @classmethod
    def setUpClass(cls):
        auth_response = requests.post(f'{cls.BASE_URL}/usuarios/login', json={
            'correo': 'testuser',
            'contrasenya': 'testpassword'
        })
        cls.token = auth_response.json().get('token')
        cls.headers = {'Authorization': f'Bearer {cls.token}'}

    def test_1_crear_rol(self):
        response = requests.post(f'{self.BASE_URL}/roles/crear_rol', json={
            'nombre_rol': 'nuevo_rol_prueba'
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rol creado exitosamente', response.json().get('mensaje'))
        self.__class__.Rol_ID = response.json().get('id')

    def test_2_editar_rol(self):
        response = requests.put(f'{self.BASE_URL}/roles/editar_rol/{self.__class__.Rol_ID}', json={
            'nombre_rol': 'rol_actualizado'
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rol modificado exitosamente', response.json().get('mensaje'))

    def test_3_borrar_rol(self):
        response = requests.delete(f'{self.BASE_URL}/roles/borrar_rol/{self.__class__.Rol_ID}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rol eliminado exitosamente', response.json().get('mensaje'))

    def test_listar_roles(self):
        response = requests.get(f'{self.BASE_URL}/roles/roles', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()
