from math import sqrt


def circle_circle_collision(obj1, obj2):
    
    r1 = max(obj1.size) / 2
    r2 = max(obj2.size) / 2

    r12 = sqrt( (obj2.transform.position[0] - obj1.transform.position[0]) ** 2 + (obj2.transform.position[1] - obj1.transform.position[1]) ** 2)

    if r12 < r1 + r2:
        if not obj2.destroyed and not obj1.destroyed:
            if obj1.rigidBody.on_touch:
                obj1.rigidBody.on_touch(obj2)