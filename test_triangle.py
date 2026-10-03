"""Unit tests for the Triangle program."""
import unittest

from triangle import classify_triangle


class TestTriangles(unittest.TestCase):
    """Tests for classify_triangle."""

    # Original test cases
    def test_right_triangle_a(self):
        """3, 4, 5 is a scalene right triangle."""
        self.assertEqual(classify_triangle(3, 4, 5), 'Scalene Right')

    def test_right_triangle_b(self):
        """5, 3, 4 is the same triangle in a different order."""
        self.assertEqual(classify_triangle(5, 3, 4), 'Scalene Right')

    def test_equilateral(self):
        """1, 1, 1 is equilateral."""
        self.assertEqual(classify_triangle(1, 1, 1), 'Equilateral')

    # New test cases
    def test_isosceles(self):
        """2, 2, 3 is isosceles."""
        self.assertEqual(classify_triangle(2, 2, 3), 'Isosceles')

    def test_isosceles_other_order(self):
        """3, 2, 3 is isosceles with the equal sides in other positions."""
        self.assertEqual(classify_triangle(3, 2, 3), 'Isosceles')

    def test_scalene(self):
        """4, 5, 6 is scalene and not right."""
        self.assertEqual(classify_triangle(4, 5, 6), 'Scalene')

    def test_not_a_triangle(self):
        """1, 2, 3 cannot form a triangle."""
        self.assertEqual(classify_triangle(1, 2, 3), 'NotATriangle')

    def test_zero_side(self):
        """A side of 0 is invalid."""
        self.assertEqual(classify_triangle(0, 4, 5), 'InvalidInput')

    def test_negative_side(self):
        """A negative side is invalid."""
        self.assertEqual(classify_triangle(3, -4, 5), 'InvalidInput')

    def test_not_an_integer(self):
        """Non-integer sides are invalid."""
        self.assertEqual(classify_triangle(3.5, 4, 5), 'InvalidInput')


if __name__ == '__main__':
    unittest.main()
