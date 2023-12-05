    
import unittest
from main import app, OperationIn, evaluate_npi
from fastapi.testclient import TestClient

client = TestClient(app)

class TestApp(unittest.TestCase):
    def test_evaluate_npi(self):
        self.assertEqual(evaluate_npi("2 3 +"), 5)
        self.assertEqual(evaluate_npi("2 3 *"), 6)
        self.assertEqual(evaluate_npi("6 3 /"), 2)

    def test_calculate(self):
        response = client.post("/calculate", json={"expression": "2 3 +"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": 5})

    def test_operations_csv(self):
        response = client.get("/operations/csv")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
