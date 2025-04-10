class Key():
    """Key for R-Tree"""
    def __init__(self, tupleId=None, mbr=None, node=None, childNode=None):
        self.mbr = mbr # MBR of the element
        self.tupleId = tupleId # Identifier of the element
        self.node = node # Node associated with the element
        self.childNode = childNode # Child node associated with the element

    def __lt__(self, other):
        if other:
            return self.mbr.priority() < other.mbr.priority()

    def __repr__(self):
        return f"""
    mbr:{self.mbr}
    tupleId:{self.tupleId}
    node:{self.node}
    childNode:{self.childNode}
    """