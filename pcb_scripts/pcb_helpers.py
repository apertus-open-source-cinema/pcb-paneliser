# Remove gerber outline to avoid interference with mixed panel outlines
def remove_gerber_outline(board_outline):
    delete_start = -1
    delete_end = -1
    data = board_outline.main_statements
    for drawing in board_outline.main_statements:
        if drawing.type == "APERTURE" and drawing.d == 10:
            delete_start = data.index(drawing)
        elif drawing.type == "APERTURE" and drawing.d != 10 and delete_start != -1:
            delete_end = data.index(drawing)
            break

    del data[delete_start:delete_end]
