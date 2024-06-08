import unittest
import requests

class TestEstimacionExterna(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:5000"  

    @classmethod
    def setUpClass(cls):
        auth_response = requests.post(f'{cls.BASE_URL}/usuarios/login', json={
            'correo': 'testuser',
            'contrasenya': 'testpassword'
        })
        cls.token = auth_response.json().get('token')
        cls.headers = {'Authorization': f'Bearer {cls.token}'}

    def test_calcular_estimacion(self):
        response = requests.post(f'{self.BASE_URL}/gestion-estimacion/calcularEstimacion', json={
            'masculino_generico': False,
            'numero_ninyos': 10,
            'numero_ninyas': 15,
            'numero_hombres': 20,
            'numero_mujeres': 25,
            'res_actividades_hombre': ['Cazar'],
            'res_actividades_mujer': ['Pescar', 'Escribir'],
            'ubicacion': 0
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('resultado'), 65)
        self.assertIn('resultado', response.json())
if __name__ == '__main__':
    unittest.main()