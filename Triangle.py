# Triangle program
def classify_triangle(a,b,c):
    if not(isinstance(a,int) and isinstance(b,int) and isinstance(c,int)):
        return 'InvalidInput'
    if a <= 0 or b <= 0 or c <= 0:
        return 'InvalidInput'
    if (a >= (b + c)) or (b >= (a + c)) or (c >= (a + b)):
        return 'NotATriangle'
    if a == b and b == c:
        kind = 'Equilateral'
    elif a == b or b == c or a == c:
        kind = 'Isoceles'
    else:
        kind = 'Scalene'
    if ((a ** 2) + (b ** 2)) == (c ** 2) or ((a ** 2) + (c ** 2)) == (b ** 2) or ((b ** 2) + (c ** 2)) == (a ** 2):
        return kind + ' Right'
    else:
        return kind

if __name__ == '__main__':
    print(classify_triangle(3,4,5))
