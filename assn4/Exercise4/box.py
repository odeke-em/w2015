class BoxValueError(Exception):
    """
    A Box Value Error occurs when a user tries to create a box with non-positive dimensions
    """
    pass

class Box:
    def __init__(self, dim1,dim2):
        """
        A 2-dimensional box, where dim1 is the length of the first dimension of the box and box.dim2 is the length of the second dimension. You can interpret this loosly as the width and height of the box, but we use the boxes without regard to orientation. 
        
        Args:
        dim1 : the size of one side of a 2D box. Must be positive
        dim2 : the size of the second side of a 2d box. Must be positive
        
        Raises:
        BoxValueError when non-positive dimensions are added

        >>> b = Box(3,4)
        >>> print(b)
        (3,4)
        >>> b.dim1
        3
        >>> b.dim2
        4
        >>> b = Box(-1,-2)
        Traceback (most recent call last):
            ...
        box.BoxValueError: Tried to create a box with non-positive dimensions
        >>> b = Box(0,3)
        Traceback (most recent call last):
            ...
        box.BoxValueError: Tried to create a box with non-positive dimensions
        """
        self.dim1 = dim1
        self.dim2 = dim2
        
    @property
    def dim1(self):
        return self._dim1
        
    @property
    def dim2(self):
        return self._dim2
    
    @dim1.setter
    def dim1(self,value):
        if value <= 0:
            raise(BoxValueError("Tried to create a box with non-positive dimensions"))
        self._dim1 = value
    
    @dim2.setter
    def dim2(self,value):
        if value <= 0:
            raise(BoxValueError("Tried to create a box with non-positive dimensions"))
        self._dim2 = value
    
    
        
    def __str__(self):
        return "({},{})".format(self.dim1, self.dim2)

    def __lt__(self, b):
        """
        Returns true if box self will fit inside of box b, otherwise returns false. If the boxes are the same size, this will return false.
        Note when we compare boxes, we do not care about their orientation. 
        
        >>> b1 = Box(3,6)
        >>> b1 < Box(4,7)
        True
        >>> Box(4,7) < b1
        False
        >>> b1 < Box(3,6)
        False
        >>> b1 < Box(4, 5)
        False
        >>> b1 < Box(2, 7)
        False
        >>> b1 < Box(6, 7)
        True
        """
        return ((min(self.dim1, self.dim2) < min(b.dim1,b.dim2)) and
                 (max(self.dim1,self.dim2) < max(b.dim1,b.dim2)))
