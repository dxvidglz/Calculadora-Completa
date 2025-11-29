import unittest
# Importamos la clase Calculator del archivo que contiene la lógica
from calculator_gui import Calculator

class TestCalculatorOperations(unittest.TestCase):
    """
    Pruebas unitarias para la clase Calculator, enfocadas en las operaciones aritméticas.
    """

    def setUp(self):
        """
        Configura una nueva instancia de Calculator antes de cada prueba.
        """
        self.calculator = Calculator()

    def perform_operation(self, num1_str, operator, num2_str):
        """
        Método auxiliar para simular la secuencia de entrada de una operación.
        """
        # Limpiar por si acaso (aunque setUp ya lo hace)
        self.calculator.clear() 
        
        # 1. Ingresar el primer número
        for digit in num1_str:
            self.calculator.append_number(digit)
            
        # 2. Elegir la operación
        self.calculator.choose_operation(operator)
        
        # 3. Ingresar el segundo número
        for digit in num2_str:
            self.calculator.append_number(digit)
            
        # 4. Ejecutar el cálculo
        self.calculator.compute()
        
        # Devolver el resultado actual como string
        return self.calculator.current_operand

    # --- Pruebas de Operaciones Básicas ---

    def test_addition(self):
        """Prueba que la suma de enteros sea correcta."""
        result = self.perform_operation('5', '+', '3')
        self.assertEqual(result, '8')

        # Prueba con decimales
        result_float = self.perform_operation('10.5', '+', '2.2')
        self.assertAlmostEqual(float(result_float), 12.7, places=2)

    def test_subtraction(self):
        """Prueba que la resta de enteros y decimales sea correcta."""
        result = self.perform_operation('15', '-', '7')
        self.assertEqual(result, '8')

        # Prueba con resultado flotante
        result_float = self.perform_operation('5.0', '-', '2.5')
        self.assertEqual(result_float, '2.5')

    def test_multiplication(self):
        """Prueba que la multiplicación sea correcta."""
        result = self.perform_operation('6', '*', '4')
        self.assertEqual(result, '24')

        # Prueba con resultado flotante
        result_float = self.perform_operation('1.5', '*', '2')
        self.assertEqual(result_float, '3') # Verifica que '3.0' se convierte a '3'

    def test_division(self):
        """Prueba que la división sea correcta."""
        # División exacta (resultado entero)
        result_int = self.perform_operation('100', '/', '10')
        self.assertEqual(result_int, '10')

        # División con resultado decimal
        result_float = self.perform_operation('7', '/', '2')
        self.assertEqual(result_float, '3.5')
    
    def test_division_by_zero(self):
        """Prueba que la división por cero resulte en 'Error'."""
        result = self.perform_operation('5', '/', '0')
        self.assertEqual(result, 'Error')

    # --- Pruebas de Comportamiento Adicional ---

    def test_chained_operation(self):
        """Prueba una secuencia de operaciones: 2 + 3 * 4 = 20 (sin orden de precedencia)"""
        # La calculadora ejecuta la operación pendiente antes de establecer la nueva.
        # Secuencia: 2 + 3 -> 5
        for digit in '2': self.calculator.append_number(digit)
        self.calculator.choose_operation('+') # current=0, previous=2, operation=+
        for digit in '3': self.calculator.append_number(digit)
        
        # compute() se llama implícitamente: 2 + 3 = 5. current=0, previous=5, operation=*
        self.calculator.choose_operation('*') 
        
        # Ingresar 4
        for digit in '4': self.calculator.append_number(digit)
        
        # Ejecutar 5 * 4 = 20
        self.calculator.compute()
        self.assertEqual(self.calculator.current_operand, '20')

    def test_decimal_input_and_output(self):
        """Prueba la entrada de números decimales y la representación del resultado."""
        # 0.5 + 0.5 = 1
        result = self.perform_operation('.5', '+', '.5')
        self.assertEqual(result, '1') # Debe ser '1' (entero)

        # 1.25 * 4 = 5
        result_int_output = self.perform_operation('1.25', '*', '4')
        self.assertEqual(result_int_output, '5') # Debe ser '5' (entero)
        
        # 10 / 3 = 3.333...
        result_float_output = self.perform_operation('10', '/', '3')
        # Usamos assertAlmostEqual por la imprecisión de punto flotante.
        self.assertAlmostEqual(float(result_float_output), 3.3333333333333335)


if __name__ == '__main__':
    unittest.main()