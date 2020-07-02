def create_dxf_rectangle(msp, x, y, width, height):
    points = [(x, y),
              (x + width, y),
              (x + width, y + height),
              (x, y + height)]

    lwp = msp.add_lwpolyline(points)
    lwp.close()
