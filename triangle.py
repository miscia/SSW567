"""Triangle program: classifies a triangle based on the lengths of its sides."""


def classify_triangle(a, b, c):
    """Return the type of triangle for sides a, b and c.

    Returns 'Equilateral', 'Isosceles' or 'Scalene', with ' Right' added
    if it is a right triangle. Returns 'NotATriangle' if the sides can't
    form a triangle and 'InvalidInput' for bad values.
    """
    sides = (a, b, c)

    if not all(isinstance(side, int) for side in sides) or min(sides) <= 0:
        return 'InvalidInput'
    if a >= b + c or b >= a + c or c >= a + b:
        return 'NotATriangle'

    if a == b == c:
        kind = 'Equilateral'
    elif a in (b, c) or b == c:
        kind = 'Isosceles'
    else:
        kind = 'Scalene'

    if is_right(a, b, c):
        kind += ' Right'
    return kind


def is_right(a, b, c):
    """Return True if the sides form a right triangle."""
    x, y, z = sorted((a, b, c))
    return x ** 2 + y ** 2 == z ** 2


if __name__ == '__main__':
    print(classify_triangle(3, 4, 5))
