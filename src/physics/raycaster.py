class Raycaster:

    def __init__(self, map):
        self.map = map


    def ccw(self, A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])


    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)


    def check_if_path_clear(self, pos1, pos2):
        for obj in self.map:
            rectX2 = obj.size[0]*obj.collider_scale*0.5
            rectY2 = obj.size[1]*obj.collider_scale*0.5

            topRight = (obj.transform.position[0] + rectX2, obj.transform.position[1] - rectY2)
            topLeft = (obj.transform.position[0] - rectX2, obj.transform.position[1] - rectY2)
            bottomRight = (obj.transform.position[0] + rectX2, obj.transform.position[1] + rectY2)
            bottomLeft = (obj.transform.position[0] - rectX2, obj.transform.position[1] + rectY2)

            if self.intersect(pos1, pos2, topRight, topLeft) or self.intersect(pos1, pos2, topLeft, bottomLeft) or \
                        self.intersect(pos1, pos2, bottomLeft, bottomRight) or self.intersect(pos1, pos2, bottomRight, topRight):

                return False

        return True