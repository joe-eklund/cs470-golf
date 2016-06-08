#!/usr/bin/python

import sys, rospy, math, time
from PyQt4 import QtGui, QtCore

from sphero_swarm_node.msg import SpheroTwist, SpheroColor
from multi_apriltags_tracker.msg import april_tag_pos
STEP_LENGTH = 100
FOLLOW_SPPED = 75
RADIUS = 150
BALL_ID = 5
SPHERO_ID = 1
GOAL_ID = 32
phases = ['initial','setup','swing','rolling']

class SpheroSwarmLineForm(QtGui.QWidget):
    
    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        self.resize(600, 480) 
        self.sphero_dict = {}
        self.initUI()
        self.initialized = False
        '''The Sphero bluetooth controller maps string names to addresses, The camera maps num to locations numToSphero
        and spheroToNum are dictoinaries that will map back and forth'''
        self.numToSphero = {}
        self.spheroToNum = {}
        self.order = [] #used to keep a follow the leadrer order
        self.location = {} #dictionary that maps sphero id nums to last known location
        self.ballMoving = False
        self.ballField = AttractiveField(BALL_ID,-1,-1,0,0,10)
        self.phase = "setup"
        self.rotateFrames = 0

        rospy.init_node('sphero_swarm_line_gui', anonymous=True)

        self.cmdVelPub = rospy.Publisher('cmd_vel', SpheroTwist, queue_size=1) #self.cmdVelPub is who we tell about to move sphero
        self.cmdVelSub = rospy.Subscriber("cmd_vel", SpheroTwist, self.cmdVelCallback)

        self.colorPub = rospy.Publisher('set_color', SpheroColor, queue_size=1) #who we tell if we want to update the color
        self.aprtSub = rospy.Subscriber('april_tag_pos', april_tag_pos, self.aprtCallback)
        #aprtSub tells us when april tags are updated. When this happens the callback function is called.
       
    def initUI(self):   
        
        key_instruct_label = """
    Control Your Sphero!
    ---------------------------
    Moving around:
       u    i    o
       j    k    l
       m    ,    .
    """
        self.keyInstructLabel = QtGui.QLabel(key_instruct_label)
        self.cmdVelLabel = QtGui.QLabel("cmd_vel")
        self.cmdVelTextbox = QtGui.QTextEdit()
        self.cmdVelTextbox.setReadOnly(True)  
        self.connect(self, QtCore.SIGNAL("sendCmdVelText(PyQt_PyObject)"), self.updateCmdVelTextbox)

        self.spheroLabel = QtGui.QLabel("Spheros:")
        self.spheroListWidget = QtGui.QListWidget()
        self.refreshBtn = QtGui.QPushButton("Refresh")
        self.refreshBtn.clicked.connect(self.refreshDevices)
        btnGridLayout = QtGui.QGridLayout()
        btnGridLayout.addWidget(self.refreshBtn, 0, 4)

        layout =  QtGui.QVBoxLayout()
        layout.addWidget(self.keyInstructLabel)
        layout.addWidget(self.cmdVelLabel)
        layout.addWidget(self.cmdVelTextbox)
        layout.addWidget(self.spheroLabel)
        layout.addWidget(self.spheroListWidget)
        layout.addLayout(btnGridLayout)
        self.setLayout(layout)

        self.setWindowTitle("Sphero Swarm Teleop")
        self.show()

    def keyPressEvent(self, e): 
        twist = None 

        print "key pressed"   
        selected_items = self.spheroListWidget.selectedItems()
        if len(selected_items) == 0:
            return

        print "selected"
           
        if e.key() == QtCore.Qt.Key_U:
            twist = SpheroTwist() 
            twist.linear.x = -STEP_LENGTH; twist.linear.y = STEP_LENGTH; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        elif e.key() == QtCore.Qt.Key_I:
            twist = SpheroTwist()  
            twist.linear.x = 0; twist.linear.y = STEP_LENGTH; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0     
        elif e.key() == QtCore.Qt.Key_O:
            twist = SpheroTwist()
            twist.linear.x = STEP_LENGTH; twist.linear.y = STEP_LENGTH; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        elif e.key() == QtCore.Qt.Key_J:
            twist = SpheroTwist()
            twist.linear.x = -STEP_LENGTH; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        elif e.key() == QtCore.Qt.Key_K:
            twist = SpheroTwist()
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        elif e.key() == QtCore.Qt.Key_L:
            twist = SpheroTwist()
            twist.linear.x = STEP_LENGTH; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        elif e.key() == QtCore.Qt.Key_M:
            twist = SpheroTwist()
            twist.linear.x = -STEP_LENGTH; twist.linear.y = -STEP_LENGTH; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        elif e.key() == QtCore.Qt.Key_Comma:
            twist = SpheroTwist()
            twist.linear.x = 0; twist.linear.y = -STEP_LENGTH; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        elif e.key() == QtCore.Qt.Key_Period:
            twist = SpheroTwist()
            twist.linear.x = STEP_LENGTH; twist.linear.y = -STEP_LENGTH; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 

        if twist != None:
            twist.name = str(selected_items[0].text())
            self.cmdVelPub.publish(twist)

    def cmdVelCallback(self, msg):
        cmd_vel_text = "(" + str(msg.name) + "),x=" + str(msg.linear.x) + " y=" + str(msg.linear.y)
        self.emit(QtCore.SIGNAL("sendCmdVelText(PyQt_PyObject)"), cmd_vel_text) 

    def updateCmdVelTextbox(self, value):
        self.cmdVelTextbox.moveCursor(QtGui.QTextCursor.End)
        self.cmdVelTextbox.ensureCursorVisible()
        self.cmdVelTextbox.append(str(value))
        self.cmdVelTextbox.update()

    ### called when refreshDevices is clicked.
    def refreshDevices(self):
        self.initialized = False
        self.spheroListWidget.clear()
        self.sphero_dict = rospy.get_param('/sphero_swarm/connected')
        self.numToSphero = {}
        self.spheroToNum = {}
        self.order = list()
        self.location = {}
        print(self.sphero_dict)

        for name in self.sphero_dict:
            num, ok = QtGui.QInputDialog.getInt(self, "Sphero num input", "Enter April Tag number for %s:" % name)
            self.numToSphero[num] = name
            self.spheroToNum[name] = name
            self.order[len(self.order):] = [num]
            self.location[num] = (-1,-1)
            self.spheroListWidget.addItem(name)
        self.spheroListWidget.setCurrentRow(0)
        self.initialized = True
        self.update()

    ### main body of algorithm should go here. MSG contains an id, x,y and orientation deta members
    def aprtCallback(self, msg):

        if not self.initialized: #still initializing
            return
        # if self.phase == 'initial':
        #     self.changePhase()
        #     return;
        # if self.phase == 'setup':
        #     return;
        # if self.phase == 'swing':
        #     if self.ballMoving:
        #         self.changePhase()
        #         return;
        # if self.phase == 'rolling':
        #     if not self.ballMoving:
        #         self.changePhase()
        #         return;
        spheroID = SPHERO_ID
        spheroIndex = 0
        ballID = BALL_ID
        ballIndex = 0
        goalIndex = 0
        for i in range(len(msg.id)):
            if msg.id[i] == ballID:
                ballIndex = i
            if msg.id[i] == spheroID:
                spheroIndex = i
            if msg.id[i] == GOAL_ID:
                goalIndex = i

        # set the ballfield location
        self.ballField.setX(msg.pose[ballIndex].x)
        self.ballField.setY(msg.pose[ballIndex].y)

	# detect ball moving
        if self.location[ballID][0] - msg.pose[ballIndex].x < 3 and self.location[ballID][1] - msg.pose[ballIndex].y < 3:
            self.ballMoving = False;
            print "ball not moving"
            # self.ballField.setAlpha(100);
        else:
            self.ballMoving = True;
            print "ball moving"
            print self.location[ballID]
            self.ballField.setAlpha(0)

	# setup or swing when ball not moving
        if not self.ballMoving:
            if self.phase == 'setup':
                print "Setup phase"
                goalPose = msg.pose[goalIndex]
                ballPose = msg.pose[ballIndex]
                spheroPose = msg.pose[spheroIndex]
                print "Sphero Position: " + str((spheroPose.x, spheroPose.y))
                distance = self.ballField.calculateDistance(goalPose.x,ballPose.x,goalPose.y,goalPose.y)
                theta = self.ballField.calcTheta(goalPose)
		print "Theta: " + str(theta)
                deltaX = math.cos(theta)
                deltaY = -math.sin(theta)
                multiplier = 100
                print "OffsetX & OffsetY: " + str((multiplier * deltaX, multiplier * deltaY))
                swingPos = [msg.pose[ballIndex].x + (multiplier * deltaX), msg.pose[ballIndex].y + (multiplier * deltaY)]
                print "Swing Position: " + str(swingPos)
                SetupField = AttractiveField(-1,swingPos[0], swingPos[1],110,0,5)
                setupFieldDist = SetupField.calculateDistance(SetupField.xpos, spheroPose.x, SetupField.ypos, spheroPose.y)
                if(setupFieldDist < 5):
                    self.changePhase()
                    return
                print "Setup Field Dist: " + str(SetupField.calculateDistance(SetupField.xpos, spheroPose.x, SetupField.ypos, spheroPose.y))
                deltaX = SetupField.calcVelocity(msg.pose[spheroIndex])[0]
                deltaY = SetupField.calcVelocity(msg.pose[spheroIndex])[1]
                print "DeltaX & DeltaY: " + str((deltaX, deltaY))
                twist = SpheroTwist()
                twist.linear.x = deltaX
                twist.linear.y = deltaY
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                selected_items = self.spheroListWidget.selectedItems();
                twist.name = str(selected_items[0].text())
                self.cmdVelPub.publish(twist)
            elif self.phase == 'swing':
                print "Swing phase"
                self.ballField.setX(msg.pose[ballIndex].x)
                self.ballField.setY(msg.pose[ballIndex].y)
                self.ballField.setAlpha(40)
                deltaX = self.ballField.calcVelocity(msg.pose[spheroIndex])[0]
                print "Delta X: " + str(deltaX)
                deltaY = self.ballField.calcVelocity(msg.pose[spheroIndex])[1]
                print "Delta Y: " + str(deltaY)
                # Normalize vector to only rotate the sphero for 40 frames
                if self.rotateFrames < 40:
                    deltaX /= math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
                    deltaY /= math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
                    self.rotateFrames += 1
                twist = SpheroTwist()
                twist.linear.x = deltaX
                twist.linear.y = deltaY
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                selected_items = self.spheroListWidget.selectedItems();
                twist.name = str(selected_items[0].text())
                self.cmdVelPub.publish(twist)
        else:
            twist = SpheroTwist()
            twist.linear.x = 0
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = 0
            selected_items = self.spheroListWidget.selectedItems();
            twist.name = str(selected_items[0].text())
            self.cmdVelPub.publish(twist)

        self.location[ballID] = (msg.pose[ballIndex].x, msg.pose[ballIndex].y)
        self.location[spheroID] = (msg.pose[spheroIndex].x, msg.pose[spheroIndex].y)

    #     Method to control program flow.  Initial -> Setup -> swing -> rolling -> setup -> ...
    def changePhase(self):
        self.rotateFrames = 0
        time.sleep(1)
        if self.phase == 'initial':
            self.phase = 'setup'
        elif self.phase == 'setup':
            self.phase = 'swing'
        elif self.phase == 'swing':
            self.phase = 'rolling'
        elif self.phase == 'rolling':
            self.phase = 'setup'

class Field:
    def __init__(self,id, xpos, ypos, alpha, s, r):
        self.id = id
        self.xpos = xpos
        self.ypos = ypos
        self.alpha = alpha
        self.s = s
        self.r = r

    def calculateDistance(self,x0,x1,y0,y1):
        distance = math.sqrt(math.pow(x0-x1,2) + math.pow(y0-y1,2))
        return distance
    def calcTheta(self, msg):
        return math.atan2(-self.ypos + msg.y,self.xpos - msg.x)

class AttractiveField(Field):
    def calcVelocity(self, msg):
        result = [0,0]
        distance = self.calculateDistance(msg.x, self.xpos, msg.y, self.ypos)
        theta = math.atan2(-self.ypos + msg.y,self.xpos - msg.x)
        if distance < self.r:
            return result
        result[0] = (self.alpha * math.cos(theta))
        result[1] = (self.alpha * math.sin(theta))
        return result
    def setX(self, x):
        self.xpos = x
    def setY(self, y):
        self.ypos = y
    def setAlpha(self, alpha):
        self.alpha = alpha;




if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    w = SpheroSwarmLineForm()
    w.show()
    sys.exit(app.exec_())
  
        
