from box import Box

def largest_box_subset(baby_boxes, mama_box, memo = None):
    """ 
    Given a tuple of 2-D boxes (baby_boxes), use dynamic programming 
    (with memoization) to find the size of the largest subset of these 
    boxes that will fit inside of the mama_box, where each box has at most
    one box stacked inside of it.  ie: box_0 is the smallest box and fits 
    inside of box_1. box_1 fits inside of box_2 ... box_(n-1) fits inside of        the mama_box. Note you never have more than one box in each box (even if    
    more than one box could fit).
    It is like you are finding the largest possible subset of boxes that form
    a matryoshka-doll-like set of boxes
    (http://en.wikipedia.org/wiki/Matryoshka_doll)! 
    
    Note a box does not fit into another box that is the same size, so a box
    with width 1 and length 1 would not fit into another box with width 1 and
    length 1. Similarly, a box of width 1 and length 1 doesn't fit into a box
    with width 1 and length 5. Also note that we do not care about the
    orientation of a box --- so a box with a width of 1 and height of 2 is the
    same as a box with a width of 2 and height of 1. Both of these boxes can
    fit into a box with a width of 3 and a height of 2.
    
     We can think of this problem recursively. If no baby_boxes fit in the
    mama_box, the answer is 1. Otherwise, for each baby box that fits in the
    mama_box, recursively find the largest box subset that starts at that baby
    box and add 1 (for the enclosing mama box). More explicitly, the
    recurrence for this function is:
    
    largest_box_subset(baby_boxes, mama_box) =:
        1 if no box fits in mama_box
        or
        1 + max(largest_box_subset(baby_boxes, child)) over all child boxes             that possibly fit in mama_box
        
    memo is a dictionary that you can use to make your solution use
    memoization.
    
    Args: 
    baby_boxes (tuple of Box objects): A tuple of boxes that can potentially be
    stacked inside of mama_box
    mama_box (Box object) : the outer box that all stacked boxes should be 
    stacked into
    memo (dictionary): An optional arguement. A dictionary for storing 
    already solved subproblems of the largest_box_subset function. Assumed to
    map from problem instances to correct solutions.
        
    >>> b = (Box(1,3), Box(4,2), Box(1,5), Box(6,2), Box(7,4),Box(2,6))
    >>> largest_box_subset(b,Box(8,8))
    4
    >>> b = (Box(1,1), Box(2,2))
    >>> largest_box_subset(b,Box(3, 3))
    3
    >>> largest_box_subset(b,Box(1,1))
    1
    >>> b = (Box(1,1), Box(1,2), Box(1,2.5))
    >>> largest_box_subset(b,Box(3,3))
    2
    >>> largest_box_subset((Box(2,2), Box(1,1)), Box(3, 3))
    3
    >>> largest_box_subset((Box(3,3), Box(1,1)), Box(2,2))
    2
    """
    # fill in your definition of largest_box_subset here. Feel free to write
    # any auxillary functions you feel will help you/make your code cleaner.
    # NOTE: hese doctests are NOT exhaustive. You need to add more tests.
    # Additionally, docstrings are not usually enough: you will likely want 
    # to include inline comments to help explain what your code is doing.
    # REMEMBER: your solution must use dynamic programming and memoization.
    
    #memo is a dictionary that you can use to make your solution use memoization
    if memo is None:
        memo = {}

    
