#!/usr/bin/env python
# -*-coding:utf-8-*


from Vec2d import Vec2d
from Vec2d.commands import CmdAdditionVec2d
from Vec2d.commands import CmdChangeVec2d

import sys
sys.path.append('../ManageTools')
import CommandManager
import GroupUndoableCommands
# from ..ManageTools.CommandManager import CommandManager
# from ..ManageTools.GroupUndoableCommands import GroupUndoableCommands


def testVec2DCmds():
    cmdManager = CommandManager.CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    v1 = Vec2d.Vec2d(1, 2)
    v2 = Vec2d.Vec2d(3, 4)
    v3 = Vec2d.Vec2d(0, 1)

    assert cmdManager.countUndo() == 0
    assert cmdManager.countRedo() == 0
    assert cmdManager.canUndo() == False
    assert cmdManager.canRedo() == False
    assert v1.x == 1
    assert v1.y == 2
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    # push the addition command
    cmdAddition = CmdAdditionVec2d.CmdAdditionVec2d(v1, v2)
    cmdManager.push(cmdAddition)

    # cmdManager.getCommands()[0].runDo()
    # the addition command is at 0 on the list of commands (CmdManager.commands)
    assert cmdManager.count() == 1
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 0
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    # push the addition command
    cmdAddition = CmdAdditionVec2d.CmdAdditionVec2d(v2, v2)
    cmdManager.push(cmdAddition)

    # cmdManager.getCommands()[0].runDo()
    # the addition command is at 0 on the list of commands (CmdManager.commands)
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 2
    assert cmdManager.countRedo() == 0
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 6
    assert v2.y == 8
    assert v3.x == 0
    assert v3.y == 1

    #undo the addition command
    assert cmdManager.canUndo() == True
    assert cmdManager.canRedo() == False
    cmdManager.undo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 1
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    #undo the addition command
    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == True
    cmdManager.undo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 0
    assert cmdManager.countRedo() == 2
    assert v1.x == 1
    assert v1.y == 2
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    #undo the addition command
    assert(cmdManager.canUndo()) == False
    assert(cmdManager.canRedo()) == True
    cmdManager.undo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 0
    assert cmdManager.countRedo() == 2
    assert v1.x == 1
    assert v1.y == 2
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    #redo the addition command
    assert(cmdManager.canUndo()) == False
    assert(cmdManager.canRedo()) == True
    cmdManager.redo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 1
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    #redo the addition command
    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == True
    cmdManager.redo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 2
    assert cmdManager.countRedo() == 0
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 6
    assert v2.y == 8
    assert v3.x == 0
    assert v3.y == 1

    #redo
    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == False
    cmdManager.redo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 2
    assert cmdManager.countRedo() == 0
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 6
    assert v2.y == 8
    assert v3.x == 0
    assert v3.y == 1

    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == False
    cmdManager.undo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 1
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    # push a group of addition commands :
    groupeCmds = GroupUndoableCommands.GroupUndoableCommands([
        CmdAdditionVec2d.CmdAdditionVec2d(v1, v3),
        CmdAdditionVec2d.CmdAdditionVec2d(v1, v3),
        CmdAdditionVec2d.CmdAdditionVec2d(v2, v3)
    ])
    cmdManager.push(groupeCmds)
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 2
    assert cmdManager.countRedo() == 0
    assert v1.x == 4
    assert v1.y == 8
    assert v2.x == 3
    assert v2.y == 5
    assert v3.x == 0
    assert v3.y == 1

    #undo the group of addition commands
    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == False
    cmdManager.undo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 1
    assert v1.x == 4
    assert v1.y == 6
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == True
    cmdManager.undo()
    assert cmdManager.count() == 2
    assert cmdManager.countUndo() == 0
    assert cmdManager.countRedo() == 2
    assert v1.x == 1
    assert v1.y == 2
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    cmdManager.push(CmdChangeVec2d.CmdChangeVec2d(v1, 0, -502))
    assert cmdManager.count() == 1
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 0
    assert v1.x == 0
    assert v1.y == -502
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == False
    cmdManager.undo()
    assert cmdManager.count() == 1
    assert cmdManager.countUndo() == 0
    assert cmdManager.countRedo() == 1
    assert v1.x == 1
    assert v1.y == 2
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    assert(cmdManager.canUndo()) == False
    assert(cmdManager.canRedo()) == True
    cmdManager.redo()
    assert cmdManager.count() == 1
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 0
    assert v1.x == 0
    assert v1.y == -502
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1

    assert(cmdManager.canUndo()) == True
    assert(cmdManager.canRedo()) == False
    cmdManager.redo()
    assert cmdManager.count() == 1
    assert cmdManager.countUndo() == 1
    assert cmdManager.countRedo() == 0
    assert v1.x == 0
    assert v1.y == -502
    assert v2.x == 3
    assert v2.y == 4
    assert v3.x == 0
    assert v3.y == 1


if __name__ == "__main__":
    testVec2DCmds()
