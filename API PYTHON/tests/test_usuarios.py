import unittest
import requests

class TestUsuariosExternos(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:5000" 
    Usuario_ID = None
    @classmethod
    def setUpClass(cls):
        auth_response = requests.post(f'{cls.BASE_URL}/usuarios/login', json={
            'correo': 'testuser',
            'contrasenya': 'testpassword'
        })
        cls.token = auth_response.json().get('token')
        cls.headers = {'Authorization': f'Bearer {cls.token}'}

    def test_1_registro_usuario(self):
        response = requests.post(f'{self.BASE_URL}/usuarios/registro', json={
            'usuario': 'nuevo',
            'correo': 'nuevo@nuevo.com',
            'rol': 2
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario registrado exitosamente', response.json().get('mensaje'))
        self.__class__.Usuario_ID = response.json().get('id')

    def test_2_modificar_usuario(self):
        response = requests.put(f'{self.BASE_URL}/usuarios/modificar_usuario/{self.__class__.Usuario_ID}', json={
            'usuario': 'usuario_modificado',
            'correo': 'nuevo@nuevo.com',
            'contrasenya_actual': '12345678',
            'contrasenya_nueva': 'newpassword'
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario modificado exitosamente', response.json().get('mensaje'))

    def test_3_eliminar_usuario(self):
        response = requests.delete(f'{self.BASE_URL}/usuarios/eliminar_usuario/{self.__class__.Usuario_ID}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario eliminado exitosamente', response.json().get('mensaje'))

    def test_listar_usuarios(self):
        response = requests.get(f'{self.BASE_URL}/usuarios/usuarios', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()
