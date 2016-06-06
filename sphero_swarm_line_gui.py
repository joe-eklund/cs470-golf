#!/usr/bin/python

import sys, rospy, math
from PyQt4 import QtGui, QtCore

from sphero_swarm_node.msg import SpheroTwist, SpheroColor
from multi_apriltags_tracker.msg import april_tag_pos
STEP_LENGTH = 100
FOLLOW_SPPED = 75
RADIUS = 150
BALL_ID = 17
SPHERO_ID = 6

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
        self.ballField = AttractiveField(20,-1,-1,0,0,10)

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
        spheroID = SPHERO_ID
        spheroIndex = 0
        ballID = BALL_ID
        ballIndex = 0
        for i in range(len(msg.id)):
            if msg.id[i] == ballID:
                ballIndex = i
            if msg.id[i] == spheroID:
                spheroIndex = i

        if self.location[ballID][0] - msg.pose[ballIndex].x < 3 and self.location[ballID][1] - msg.pose[ballIndex].y < 3:
            self.ballMoving = False;
            print "ball not moving"
            self.ballField.setAlpha(100);
        else:
            self.ballMoving = True;
            print "ball moving"
            print self.location[ballID]
            self.ballField.setAlpha(0)

        if not self.ballMoving:
            self.ballField.setX(msg.pose[ballIndex].x)
            self.ballField.setY(msg.pose[ballIndex].y)
            self.ballField.setAlpha(100)
            deltaX = self.ballField.calcVelocity(msg.pose[spheroIndex])[0]
            print "Delta X: " + str(deltaX)
            deltaY = self.ballField.calcVelocity(msg.pose[spheroIndex])[1]
            print "Delta Y: " + str(deltaY)
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
        # for i in range(0,len(msg.id)):
        #     self.location[msg.id[i]] = (msg.pose[i].x, msg.pose[i].y)

        # for key in self.location:
        #     self.location[key] = (-1,-1)
        #

        #
        # for key in msg.id:
        #     toHere = self.location[key]
        #     if toHere[0] == -1:
        #         continue
        #     nextIndx = self.order.index(key) + 1
        #     if nextIndx >= len(self.order):
        #         continue
        #     nextSpher = self.order[nextIndx]
        #     fromHere = self.location[nextSpher]
        #     if fromHere[0] == -1:
        #         continue
        #     diffX = toHere[0] - fromHere[0]
        #     diffY = toHere[1] - fromHere[1]
        #
        #     distance = math.sqrt((diffX * diffX) + (diffY * diffY))
        #     twist = SpheroTwist()
        #     twist.name = self.numToSphero[nextSpher]
        #     print distance
        #     if distance < RADIUS:
        #         twist.linear.x = 0;
        #         twist.linear.y = 0;
        #         twist.linear.z = 0
        #         twist.angular.x = 0;
        #         twist.angular.y = 0;
        #         twist.angular.z = 0
        #     else:
        #         omega = math.atan2(diffY, diffX)
        #         deltaX = FOLLOW_SPPED * math.cos(omega)
        #         deltaY = -FOLLOW_SPPED * math.sin(omega)
        #         twist.linear.x = deltaX
        #         twist.linear.y = deltaY
        #         twist.linear.z = 0
        #         twist.angular.x = 0;
        #         twist.angular.y = 0;
        #         twist.angular.z = 0
        #     self.cmdVelPub.publish(twist) # how to tell sphero to move. all fields in twist must be explicitly set.

class Field:
    def __init__(self,id, xpos, ypos, alpha, s, r):
        self.id = id
        self.xpos = xpos
        self.ypos = ypos
        self.alpha = alpha
        self.s = s
        self.r = r

    def calculateDistance(self,x0,x1,y0,y1):
        distance = math.sqrt(math.pow(int(x0)-x1,2) + math.pow(int(y0)-y1,2))
        return distance

class AttractiveField(Field):
    def calcVelocity(self, msg):
        result = [0,0]
        distance = self.calculateDistance(int(msg.x), self.xpos, int(msg.y), self.ypos)
        theta = math.atan2(-self.ypos + int(msg.y),self.xpos - int(msg.x))
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
  
        
