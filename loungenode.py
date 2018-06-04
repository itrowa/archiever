from vectors import Vector

class PlanVector(Vector):
    """ encapsulate some high-order operations. """
    def __init__(self, x, y, z):
        super(PlanVector, self).__init__(x, y, z)

class VectorMethods:
    def midPoint(a, b):
        """ return an mid point from a and b."""
        return VectorMethods.eval2Pts(a, b, 0.5)

    def eval2Pts(a, b, t):
        """ eval alone point a and b using parameter t."""
        return PlanVector((1-t)*a.x + t*b.x, (1-t)*a.y + t*b.y, (1-t)*a.z + t*b.z)

    def perpendicular(v):
        """ Shifts the angle by pi/2 and cal the vector using original
            vector length
            http://stackoverflow.com/questions/16890711/normalise-and-perpendicular-function-in-python
        """ 
