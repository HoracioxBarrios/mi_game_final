class Animation:
    def __init__(self, name: str, path: str, columns: int, rows: int, cut_row: int, from_column_cut: int, up_column_cut: int, flip: bool) -> None:
        self.name = name
        self.path = path
        self.columns = columns
        self.rows = rows
        self.cut_row = cut_row
        self.from_column_cut = from_column_cut
        self.up_column_cut = up_column_cut
        self.flip = flip
