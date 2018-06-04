from __future__ import division
import math
from functools import reduce


#  This is the basic class for supporting vector calculation.

class Point(object):
    """ Point class: Reprepsents a point in the x, y, z space. """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__, self.x,
                                           self.y, self.z)

    def substract(self, point):
        """ Return a Point instance as the displacement of two points. """

        return Point(point.x - self.x, point.y - self.y, point.z - self.z)

    @classmethod
    def from_list(cls, l):
        """ Return a Point instance from a given list """

        x, y, z = map(float, l)
        return cls(x, y, z)


class Vector(Point):
    """ Vector class: Represents a vector in the x, y, z space. """

    def __init__(self, x, y, z):
        self.vector = [x, y, z]
        super(Vector, self).__init__(x, y, z)

    def move_to(self, Vector):
        self.x = Vector.x
        self.y = Vector.y
        self.z = Vector.z

    def add(self, number):
        """ Return a Vector instance as the product of the vector and a real
            number. """

        return self.from_list([x+number for x in self.vector])

    def multiply(self, number):
        """ Return a Vector instance as the product of the vector and a real
            number. """

        # return self.from_list([x*number for x in self.vector])
        return Vector(self.x*number, self.y*number, self.z*number)

    def magnitude(self): # @todo @caution check: something wrong?
        """ Return magnitude of the vector. """

        return (math.sqrt(reduce(lambda x, y: x+y,
                [x**2 for x in self.vector])))

    def sum(self, vector):
        """ Return a Vector instance as the vector sum of two vectors. """

        # return (self.from_list([x+vector.vector[self.vector.index(x)]
        #         for x in self.vector]))
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def substract(self, vector):
        """ Return a Vector instance as the vector difference of two vectors.
        """

        # return (self.from_list([vector.vector[self.vector.index(x)]-x for x in
        #                         self.vector]))
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def length(self):# @todo @caution how to avoid zero length check?
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        # @todo @caution zero divition check
        if self.length() == 0:
            return Vector(0.001,0.001,0)
        else:
            return Vector(self.x/self.length(), self.y/self.length(), self.z/self.length())

    # def dot(self, vector, theta=None): # @ need check!
        """ Return the dot product of two vectors. If theta is given then the
        dot product is computed as v1*v1 = |v1||v2|cos(theta). Argument theta
        is measured in degrees. """

        # if theta is not None:
        #     return (self.magnitude() * vector.magnitude() *
        #             math.degrees(math.cos(theta)))
        # return (reduce(lambda x, y: x+y,
        #         [x*vector.vector[self.vector.index(x)]
        #          for x in self.vector]))

    def dot(self, vector, theta=None): 
        """ Return the dot product of two vectors. If theta is given then the
        dot product is computed as v1*v1 = |v1||v2|cos(theta). Argument theta
        is measured in degrees. """

        if theta is not None:
            raise Exception(' theta function is not implemented yet.')
            # return (self.magnitude() * vector.magnitude() *
            #         math.degrees(math.cos(theta)))
        else:
            return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def cross(self, vector):
        """ Return a Vector instance as the cross product of two vectors """

        return Vector((self.y * vector.z - self.z * vector.y),
                      (self.z * vector.x - self.x * vector.z),
                      (self.x * vector.y - self.y * vector.x))

    def negative(self):
        """ Return a Vector as self negative """
        return Vector(0-self.x, 0-self.y, 0-self.z)

    def angle(self, vector):
        """ Return the angle between two vectors in degrees. """

        return (math.degrees(math.acos((self.dot(vector) / (self.magnitude() *
                vector.magnitude())))))

    def get_angle_2d(self):
        # Returns the vector's angle (in radians)
        return math.atan2(self.y,self.x)    

    def parallel(self, vector):
        """ Return True if vectors are parallel to each other. 
            if 2 vectors are negative we slao called "parallel"
        """

        # if self.cross(vector).magnitude() == 0 or self.cross(vector.negative()).magnitude() == 0:
        if abs(self.cross(vector).magnitude()) < 0.01 : # @todo @caution:: find a better way.
            return True
        return False

    def parallels(self, vector):
        """ Return True if vectors are parallel(strictly) to each other. 
            if 2 vectors are negative, they are not parallel strictly.
        """

        # if self.cross(vector).magnitude() == 0 or self.cross(vector.negative()).magnitude() == 0:
        if abs(self.cross(vector).magnitude()) < 0.01 : # @todo @caution:: find a better way.
            return True
        return False

    def is_perpendicular_to(self, vector):
        """ Return True if vectors are perpendicular to each other. """

        if abs(self.dot(vector)) < 0.01:
            return True
        return False

    def non_parallel(self, vector):
        """ Return True if vectors are non-parallel. Non-parallel vectors are
            vectors which are neither parallel nor perpendicular to each other.
        """

        if (self.is_parallel(vector) is not True and
                self.is_perpendicular(vector) is not True):
            return True
        return False

    def mid_point(self, vector):
        """ return an mid point from a and b."""
        return self.eval_2pts(vector, 0.5)

    def eval_2pts(self, vector, t):
        """ eval alone point a and b using parameter t.
            if t=0 the return vector has the same coord as self vector.
        """
        if t < 0 or t > 1:
            raise Exception("Cannot Eval ", e,  " with t=", t, ": t Should Satisfy 0<=t<=1.")
        else:
            return Vector((1-t)*self.x + t*vector.x, (1-t)*self.y + t*vector.y, (1-t)*self.z + t*vector.z)

    def perpendicular(self): #@caution: not tested
        """ http://codereview.stackexchange.com/questions/43928/algorithm-to-get-an-arbitrary-perpendicular-vector
        Finds an arbitrary perpendicular vector . 
        """
        # for two vectors (x, y, z) and (a, b, c) to be perpendicular,
        # the following equation has to be fulfilled
        #     0 = ax + by + cz

        # x = y = z = 0 is not an acceptable solution
        if self.x == self.y == self.z == 0:
            raise ValueError('zero-vector')

        # If one dimension is zero, this can be solved by setting that to
        # non-zero and the others to zero. Example: (4, 2, 0) lies in the
        # x-y-Plane, so (0, 0, 1) is orthogonal to the plane.
        if self.x == 0:
            return Vector(1, 0, 0)
        if self.y == 0:
            return Vector(0, 1, 0)
        if self.z == 0:
            return Vector(0, 0, 1)

        # arbitrarily set a = b = 1
        # then the equation simplifies to
        #     c = -(x + y)/z
        return Vector(1, 1, -1.0 * (self.x + self.y) / self.z)

    def perpendicular_2d(self):
        # Shifts the angle by pi/2 (rotate vector CCW) and calculate the coordinates
        # using the original vector length
        return Vector(
            self.length()*math.cos(self.get_angle_2d() + math.pi/2),
            self.length()*math.sin(self.get_angle_2d() + math.pi/2),
            0
            )

    def rotate_ccw_90(self):
        """ return a new vector that is original one by rotating ccw 90 degrees """
        return self.perpendicular_2d()

    def rotate_cw_90(self):
        return self.negative().perpendicular_2d()


    @classmethod
    def from_points(cls, point1, point2):
        """ Return a Vector instance from two given points. """

        if isinstance(point1, Point) and isinstance(point2, Point):
            displacement = point1.substract(point2)
            return cls(displacement.x, displacement.y, displacement.z)
        raise TypeError


if __name__=="__main__":
    a = Vector(0,10,0)
    b = Vector(0, 3, 4)
    c = Vector(0, 2, 3)
    d = Vector(10, 0, 0)
    v1 = Vector(0, 1, 0)
    v2 = Vector(0, -1, 0)

    # test length(), normalize
    print("1111111111")
    print(a.length())
    print(b.length())
    print(a.normalize())
    print(b.normalize())
    print(a.normalize().length())
    print(b.normalize().length())

    # test perpendicular_2d
    print("2222222222")
    print(a.perpendicular_2d())
    print(a.perpendicular_2d().length())
    print(a.normalize().perpendicular_2d())
    print(a.normalize().perpendicular_2d().length())

    print(v1.perpendicular_2d().normalize())
    print(v2.perpendicular_2d().normalize())

    # test negative,
    print("333333333")
    print(a.perpendicular_2d())
    print(a.negative())
    print(b.negative())
    print(a.negative().length())
    print(b.negative().length())
    print(b.substract(c))

    # test parallel
    print(a.parallel(a))
    print(a.parallel(a.negative()))
    print(a.parallel(b))

    # test perpendicular
    print("44444444444")
    print(a.is_perpendicular_to(d))

    # test sum
    print(a.sum(b))
    print(a.sum(b.negative()))
    print(Vector(400, 150, 0).sum(Vector(0, -100, 0)))

    # test set_coord
    # print(a.set_coord(Vector(100, 2, 3)))

    # test multiply
    print(a.multiply(10))

    # tes rotate 90
    print("----------rotate----------")
    print(a.rotate_cw_90())
    print(a.rotate_ccw_90())
