from PySide import QtCore
from PySide import QtDeclarative

from pyTuttle import tuttle

import logging

from buttleofx.data import ButtleDataSingleton


class TimerPlayer(QtDeclarative.QDeclarativeItem):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self._timer = QtCore.QTimer()
        self._fps = 25
        self._speed = 1000/self._fps  # delay between frames in milliseconds
        self.connect(self._timer, QtCore.SIGNAL("timeout()"), self.nextFrame)  # initialize the timer
        # new tests with processGraph
        self._frame = 0
        self._fps = 25
        self._nbFrames = 1
        self._processGraph = None

    # fonctions used in QML for the Viewer (in the file TimelineTools.qml)
    @QtCore.Slot()
    def play(self):
        print "--------------playing-------------"

        buttleData = ButtleDataSingleton().get()
        #Get the name of the currentNode of the viewer
        node = buttleData.getCurrentViewerNodeName()
        # initialization of the process graph
        graph = buttleData.getGraph().getGraphTuttle()
        processOptions = tuttle.ComputeOptions()
        processGraph = tuttle.ProcessGraph(processOptions, graph, [node])
        processGraph.setup()
        # timeRange between the frames of beginning and end (first frame, last frame, step)
        timeRange = tuttle.TimeRange(self._frame, self._nbFrames, 1)
        processGraph.beginSequence(timeRange)
        # communicate processGraph to buttleData
        buttleData.setProcessGraph(processGraph)

        buttleData.setVideoIsPlaying(True)

        self._timer.start(self._speed)


    @QtCore.Slot()
    def pause(self):
        self._timer.stop()
        buttleData = ButtleDataSingleton().get()
        buttleData.setVideoIsPlaying(False)
        # close processGraph and delete it
        buttleData.getProcessGraph.endSequence()
        buttleData.setProcessGraph(None)

    @QtCore.Slot()
    def stop(self):
        self._timer.stop()
        buttleData = ButtleDataSingleton().get()
        buttleData.setVideoIsPlaying(False)
        # close processGraph and delete it
        buttleData.getProcessGraph.endSequence()
        buttleData.setProcessGraph(None)
        # return to the beginning of the video
        self._frame = 0
        self.framePlayerChanged.emit()

    @QtCore.Slot()
    def nextFrame(self):
        if(self._frame < self._nbFrames - 1):
            self._frame = self._frame + 1
        else:
            return
        self.framePlayerChanged.emit()

    @QtCore.Slot()
    def previousFrame(self):
        if(self._frame > 0):
            self._frame = self._frame - 1
        else:
            return
        self.framePlayerChanged.emit()

    def getFrame(self):
        return self._frame

    def setFrame(self, frame):
        if(int(frame) >= self._nbFrames):
            print 'setFrame, ignore: frame outside bounds'
            return
        self._frame = int(frame)
        self.framePlayerChanged.emit()

    def getFPS(self):
        return self._fps

    def setFPS(self, fps):
        self._fps = fps
        self.fpsVideoChanged.emit()

    def setNbFrames(self, nbFrames):
        self._nbFrames = nbFrames
        self.nbFramesChanged.emit()

    def getNbFrames(self):
        return self.nbFrames

    framePlayerChanged = QtCore.Signal()
    fpsVideoChanged = QtCore.Signal()
    nbFramesChanged = QtCore.Signal()

    frame = QtCore.Property(float, getFrame, setFrame, notify=framePlayerChanged)
    fps = QtCore.Property(float, getFPS, setFPS, notify=fpsVideoChanged)
    nbFrames = QtCore.Property(int, getNbFrames, setNbFrames, notify=nbFramesChanged)
