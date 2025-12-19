import math
def area_circle(rad):
    """returns area of circle by taking input radius"""
    area_of_circle = math.pi * rad *rad 
    return area_of_circle

def area_rectangle(l, w):
    """returns area of rectangle by taking input length and width"""
    area_of_rectangle = l * w
    return area_of_rectangle

def area_square(s):
    """returns area of square by taking input side"""
    area_of_square = s ** 2
    return area_of_square

def area_triangle(l, w, h):
    """returns area of triangle by taking input length, width, height"""

    s = (l + w + h)/2
    area_of_triangle = math.sqrt(s *(s - l) *(s - w ) *(s - h))
    return area_of_triangle

if __name__== "__main__":
    r = int(input("Enter a radius: "))
    circle = area_circle(r)
    print(f"Area of cirlce of radius {r} is {circle}")

    l = int(input("\nEnter a length : "))
    w = int(input("Enter a width : "))
    rectangle = area_rectangle(l, w)
    print(f"Area of rectangle of lenth {l} width {w} is {rectangle}")

    s = int(input("\nEnter a side: "))
    square = area_square(s)
    print(f"Area of square of side {s} is {square}")

    l = int(input("\nEnter a length: "))
    w = int(input("Enter a width: "))
    h = int(input("Enter a height: "))
    triangle = area_triangle(l, w, h)
    print(f"Area of triangle of length {l}, width {w}, heigth {h} is {triangle}")