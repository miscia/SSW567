import unittest
from Triangle import classify_triangle

class TestTriangles(unittest.TestCase):
    def testRightTriangleA(self):
        self.assertEqual(classify_triangle(3,4,5),'Scalene Right')

    def testRightTriangleB(self):
        self.assertEqual(classify_triangle(5,3,4),'Scalene Right')

    def testEquilateralTriangles(self):
        self.assertEqual(classify_triangle(1,1,1),'Equilateral')

if __name__ == '__main__':
    unittest.main()
