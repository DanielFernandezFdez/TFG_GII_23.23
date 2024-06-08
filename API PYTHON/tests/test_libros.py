import unittest
import requests

class TestLibrosExternos(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:5000" 
    Libro_ID = None

    @classmethod
    def setUpClass(cls):
        auth_response = requests.post(f'{cls.BASE_URL}/usuarios/login', json={
            'correo': 'testuser',
            'contrasenya': 'testpassword'
        })
        cls.token = auth_response.json().get('token')
        cls.headers = {'Authorization': f'Bearer {cls.token}'}

    def test_1_agregar_libro(self):
        response = requests.post(f'{self.BASE_URL}/gestion-libros/agregarLibro', json={
            'titulo': 'Nuevo Libro',
            'isbn': '1234567890',
            'editorial': 'Editorial Ejemplo',
            'descripcion': 'Descripción del libro',
            'anyo_publicacion': 2024,
            'puntuacion': 5,
            'ubicacion_estudio': 'Estudio 1',
            'url_imagen': 'http://example.com/image.jpg',
            'puntuacion_masculino_generico': 4,
            'puntuacion_menores': 3,
            'puntuacion_adultos': 5,
            'puntuacion_ubicacion': 4,
            'puntuacion_actividades': 5
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Libro agregado exitosamente', response.json().get('mensaje'))
        self.__class__.Libro_ID = response.json().get('id')

    def test_2_editar_libro(self):
        self.assertIsNotNone(self.__class__.Libro_ID, "Libro_ID es None, 'test_1_agregar_libro' ha fallado o no se ha ejecutado.")
        response = requests.put(f'{self.BASE_URL}/gestion-libros/editarLibro/{self.__class__.Libro_ID}', json={
            'titulo': 'Libro Actualizado',
            'isbn': '0987654321'
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Libro editado exitosamente', response.json().get('mensaje'))

    def test_3_borrar_libro(self):
        self.assertIsNotNone(self.__class__.Libro_ID, "Libro_ID es None, 'test_1_agregar_libro' ha fallado o no se ha ejecutado.")
        response = requests.delete(f'{self.BASE_URL}/gestion-libros/borrarLibro/{self.__class__.Libro_ID}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Libro eliminado exitosamente', response.json().get('mensaje'))

    def test_listar_libros(self):
        response = requests.get(f'{self.BASE_URL}/gestion-libros/listadoLibros', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()
