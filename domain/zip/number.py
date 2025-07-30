class Number:
    """
    Represents numbered constraints on the grid.
    """

    def __init__(self, row: int, col: int, val: int):
        self.row = row
        self.col = col
        self.val = val

    def get_row(self) -> int:
        """
        Get the row index of the number.
        """
        return self.row
    
    def get_col(self) -> int:
        """
        Get the column index of the number.
        """
        return self.col

    def get_value(self) -> int:
        """
        Get the value of the number.
        """
        return self.val
    
    def get_value_str(self) -> str:
        """
        Get the value of the number as a string.
        """
        return chr(self.val + ord('A') - 1)