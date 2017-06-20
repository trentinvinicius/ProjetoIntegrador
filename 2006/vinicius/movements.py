import XL320Class,xl320,Packet
import time
import numpy as np


R_SHOULDER_PITCH, L_SHOULDER_PITCH, \
R_SHOULDER_ROLL = range(1,4)


class Movements():
    goalPos      = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    lastReadPos  = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    jointsCenter = [228, 808, 520, 527, 525, 832, 511, 562, 511]
    jointsMax    = [800, 808, 850, 527, 830, 832, 611, 650, 650]
    jointsMin    = [228, 200, 520, 197, 525, 510, 411, 474, 372]
    def __init__(self):
        self.xl = XL320Class.XL320()
	for i in range(0,6):
	    self.goalPos[i] = self.jointsCenter[i]
	    self.setAngle(i, 0)
    	for i in range(6,9):
	    self.goalPos[i] = self.jointsCenter[i]
	    self.setAngle(i, 90)

    def getAngle(self, index):
        while True:
	    ans = self.xl.getData(xl320.XL320_PRESENT_POSITION,index)
	    receivedAngle = np.asarray(ans)
            if len(str(receivedAngle)) > 3:
                print ("Current angle: " +str(int(receivedAngle[1])))
	        return int(receivedAngle[1])
	        break
	    else:
	        print "-2 error retrieving angle"
	    #self.getAngle(index)

    def getAllAngles(self):
        for i in range(0,8):
            ans = self.xl.getData(xl320.XL320_GOAL_POSITION,index)
            print ("Current angle: " +str(ans))
    def degreeToAngle(self, index, degree):
        self.prop = (self.jointsMax[index] - self.jointsMin[index])/180.000
	if(index%2==0 and index < 5):
            return (self.prop*degree)+self.jointsMin[index]
        else:
            return self.jointsMax[index]-(self.prop*degree)
    def angleToDegree(self, index, angle):
        self.prop = (self.jointsMax[index] - self.jointsMin[index])/180.00
        if(index%2==0 and index < 5):
            return (angle - self.jointsMin[index])/self.prop
        else:
            return (self.jointsMax[index]-angle)/self.prop


    def setAngle(self, index, degree):
	if(degree <= 180 and degree >= 0):
            angle = self.degreeToAngle(index, degree)
            self.goalPos[index] = angle
            print "setando o angulo para "+str(angle)+ " da junta "+str(index)
            ans = self.xl.setData(xl320.XL320_GOAL_POSITION,int(index),int(angle))
        else :
            print "Angle out of bounds"

    def blinkLED(self, index):
        for i in range(0,9):
            ans = self.xl.setData(xl320.XL320_LED,index,i)
            time.sleep(1)
        self.xl.setData(xl320.XL320_LED,1,0)

    def enableJoint(self, index):
        ans = self.xl.setData(xl320.XL320_TORQUE_ENABLE,index,1)

    def disableJoint(self, index):
        ans = self.xl.setData(xl320.XL320_TORQUE_ENABLE,index,0)

    def enableAllJoints(self):
#         ans = self.xl.setNDataN(xl320.XL320_TORQUE_ENABLE,[[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1]])
# 	 time.sleep(0.05)
        for i in range(0,9):
            ans = self.xl.setData(xl320.XL320_TORQUE_ENABLE,i,1)

    def disableAllJoints(self):
        for i in range(0,9):
            ans = self.xl.setData(xl320.XL320_TORQUE_ENABLE,i,0)


    #def testMotor(self, index):
