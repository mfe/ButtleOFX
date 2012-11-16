#!/usr/bin/env python
# -*-coding:utf-8-*


from ..Vec2d import Vec2d


class CmdAdditionVec2d():
    """
        Command which enable us to addition Vector2d
    """

    def __init__(self, vec2d_target, vec2d_add):
        """
            Iinitializes the member variables :
            vec2d_target is the target vector wich will be changed by the addition
            vec2d_add is the vector wich will be added to the target
            vec2d_old is the old value of the target vector, wich will be used for reset the target in case of undo command
        """
        self.vec2dTarget = vec2d_target
        self.vec2dAdd = vec2d_add
        self.vec2dOld = Vec2d(vec2d_target.x, vec2d_target.y)

    def undoCmd(self):
        """
            Undoes the addition of the vectors.
            The target vector is reset with the old coordinates.
        """
        self.vec2dTarget.x = self.vec2dOld.x
        self.vec2dTarget.y = self.vec2dOld.y
        return self.vec2dTarget

    def redoCmd(self):
        """
            Redoes the addition of the vectors.
        """
        return self.doCmd()

    def doCmd(self):
        """
            Executes the addition of the vectors.
        """
        self.vec2dTarget.x += self.vec2dAdd.x
        self.vec2dTarget.y += self.vec2dAdd.y
        return self.vec2dTarget
