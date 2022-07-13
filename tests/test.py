from AssemblerInterpreter import AssemblerInterpreter
from texts import *
import unittest


class Test(unittest.TestCase):
    def test1(self):
        self.interpreter = AssemblerInterpreter(simple_program)
        self.assertEqual(self.interpreter.main_loop(), '(5+1)/2 = 3')

    def test2(self):
        self.interpreter = AssemblerInterpreter(factorial)
        self.assertEqual(self.interpreter.main_loop(), '5! = 120')

    def test3(self):
        self.interpreter = AssemblerInterpreter(fibonacci)
        self.assertEqual(self.interpreter.main_loop(), 'Term 8 of Fibonacci series is: 21')

    def test4(self):
        self.interpreter = AssemblerInterpreter(modulo)
        self.assertEqual(self.interpreter.main_loop(), 'mod(11, 3) = 2')

    def test5(self):
        self.interpreter = AssemblerInterpreter(gcd)
        self.assertEqual(self.interpreter.main_loop(), 'gcd(81, 153) = 9')

    def test6(self):
        self.interpreter = AssemblerInterpreter(power)
        self.assertEqual(self.interpreter.main_loop(), '2^10 = 1024')

    def tearDown(self) -> None:
        super(Test, self).tearDown()


if __name__ == '__main__':
    unittest.main()
