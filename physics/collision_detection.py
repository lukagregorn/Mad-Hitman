from math import sqrt

RECT = 0
CIRCLE = 1

DEFAULT_TYPE = CIRCLE


def circle_circle_collision(circle1, circle2):

    rC1 = max(circle1.size) * circle1.collider_scale / 2
    rC2 = max(circle2.size) * circle2.collider_scale / 2

    return (rC1 + rC2) > sqrt((circle2.transform.position[0] - circle1.transform.position[0]) ** 2 + (circle2.transform.position[1] - circle1.transform.position[1]) ** 2)


def circle_rect_collision(circle, rect):

    rectX = rect.size[0]*rect.collider_scale
    rectY = rect.size[1]*rect.collider_scale

    rectRight = rect.transform.position[0] + rectX/2
    rectLeft = rect.transform.position[0] - rectX/2
    rectBottom = rect.transform.position[1] + rectY/2
    rectTop = rect.transform.position[1] - rectY/2

    # Find the closest point to the circle within the rectangle
    closestX = min(max(rectLeft, circle.transform.position[0]), rectRight)
    closestY = min(max(rectTop, circle.transform.position[1]), rectBottom)

    # Calculate the distance between the circle's center and this closest point
    distanceX = circle.transform.position[0] - closestX
    distanceY = circle.transform.position[1] - closestY

    # If the distance is less than the circle's radius, an intersection occurs
    distanceSquared = (distanceX ** 2) + (distanceY ** 2)
    return distanceSquared < (min(circle.size)*circle.collider_scale ** 2)


def collision_detection(obj1, obj2):

    type1 = obj1._collider
    type2 = obj2._collider

    interescting = False
    if (type1 == CIRCLE) and (type2 == RECT):
        interescting = circle_rect_collision(obj1, obj2)
    
    elif (type1 == RECT) and (type2 == CIRCLE):
        interescting = circle_rect_collision(obj2, obj1)

    elif (type1 == CIRCLE) and (type2 == CIRCLE):
        interescting = circle_circle_collision(obj1, obj2)

    else:  # we dont care about 2 rects because all moving bodies are circles
        return


    # resolve collision
    if (interescting):
        if not obj2.destroyed and not obj1.destroyed:

            # call on obj2 so that static objects can react to non-static
            if obj2.rigidBody.on_touch:
                obj2.rigidBody.on_touch(obj1)