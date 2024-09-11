from manim import *

def construct_head(width, height):
    head_shape = [
            [height/2, width/2, 0],
            [-height/2, width/2, 0],
            [-height/2, -width/2, 0],
            [height/2, -width/2, 0],
        ]
        # expressions = Cross(scale_factor=0.3, color=RED)
    face_arc_conf = {
            "stroke_width": 7,
            'color': YELLOW_C,
            # 'fill_opacity': 1,
            # 'fill_color': BLUE_A,
        }
    face_conf = {
            # "stroke_width": 0,
            'color': RED,
            'fill_opacity': 1,
            'fill_color': BLACK,
        }
    face = [
            [0, -0.6, 0],
            [0.45, 0.45, 0],
            [-0.45, 0.45, 0],
            [0, 0.3/np.sqrt(2), 0],
        ]
    a, b, c, d = face
    arc0 = ArcBetweenPoints(a, b, angle=TAU/4, **face_arc_conf)
    arc1 = ArcBetweenPoints(c, a, angle=TAU/4, **face_arc_conf)
    arc2 = ArcBetweenPoints(b, d, angle=TAU/4.5, **face_arc_conf)
    arc3 = ArcBetweenPoints(d, c, angle=TAU/4.5, **face_arc_conf)
    mask = ArcPolygonFromArcs(arc0, arc1, arc2, arc3, **face_conf)
    head = Polygon(*head_shape, color=PURPLE_B)

    Head_point = [
            Dot(point=point, color=YELLOW_C, radius=0.03) for point in head_shape
        ]
    Corner = VGroup(*Head_point)
    Head = VGroup()
    Head.add(head, mask, Corner)
    Head.add(*[Dot(point=point, color=YELLOW_C, radius=0.03) for point in face])
        # Headx_updater = ValueTracker(0)
        # Heady_updater = ValueTracker(0)
        # Head.add_updater(lambda x: x.set_x(Headx_updater.get_value()))
        # Head.add_updater(lambda y: y.set_y(Heady_updater.get_value()))
    Head.move_to(UP)
    return Head