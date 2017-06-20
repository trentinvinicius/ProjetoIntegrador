import sys
sys.path.append('/home/pi/beo/movements')
from pyxl320 import xl320,Packet,ServoSerial, utils

class XL320(object):
    def __init__(self):
        self.serial = ServoSerial('/dev/ttyAMA0')#tell it what port you want to use
        #self.serial.close()
        self.serial.open()

    def setData(self,memAddress,ID,data):
        """
        Set a memory address (memAddress) from servo ID to "data"
        """
        numBytes =  Packet.dataLength(memAddress)
        if (numBytes == 2):
            pkt = Packet.makeWritePacket(ID,memAddress,Packet.le(data))
        else:
            pkt = Packet.makeWritePacket(ID,memAddress,[data])

        ans,err_num,err_str = self.serial.sendPkt(pkt)
        if ans == [] or len(ans) < 9:#In case of an empty packet arrives
            return -2
        else:
            return ans[8]#Byte of error status

    def setNDataN(self,memAddress,listOf_IDsData):
        """
        listOf_IDsData = [[id0,data0],[id1,data1],...,[idN,dataN]]
        """
        pkt = Packet.makeSyncWritePacket(memAddress,listOf_IDsData)
        ans,err_num,err_str = self.serial.sendPkt(pkt)
        if ans == []:#In case of an empty packet arrives
            return -2#This instruction doesn't return status packet


    def getData(self,memAddress,*id_list):
        """
        id_list = id0,id1,...,idN
        """
        numBytes = Packet.dataLength(memAddress)
        if(numBytes == 1):
            ans = self.getByte(memAddress,id_list)
        else:#numBytes==2
            ans = self.getWord(memAddress,id_list)
        return ans

    def setByte(self,memAddress,ID,data):
        #Already coded in setData()
        pass

    def getByte(self,memAddress,id_list):
        """
        Gets a list of IDs and return its Model Numbers
        inside a list (id0,data0,id1,data1,...idN,dataN)
        """
        if id_list == ():#Empty list
            return -1
        elif len(id_list) == 1:#Just one ID.
            pkt = Packet.makeReadPacket(id_list[0],memAddress)
        else:
            pkt = Packet.makeSyncReadPacket(memAddress,id_list)

        ans,err_num,err_str = self.serial.sendPkt(pkt)
        if ans == []:#In case of an empty packet arrives
            return -2
        else:
            data = []
            for index,val in enumerate(id_list):
                data.append(val)            #Append the ID value
                data.append(ans[index*12+9])#Append the respective ID's data
            return data


    def setWord(self,memAddress,ID,data):
        #Already coded in setData()
        pass

#   def setWord(self,memAddress,listOf_IDsData):
#        """
#        listOf_IDsData = [[id0,data0],[id1,data1],...,[idN,dataN]]
#        """
#        if listOf_IDsData == ():#Empty list
#            return -1
#        elif len(listOf_IDsData) == 2:#Just one ID and its respectively data
#            pkt = Packet.makeWritePacket(listOf_IDsData[0],memAddress,listOf_IDsData[1])
#        else:#more than one ID
#            pkt = Packet.makeSyncWritePacket(memAddress,listOf_IDsData)
#
#        ans,err_num,err_str = self.serial.sendPkt(pkt)
#        if ans == []:#In case of an empty packet arrives
#            return -2 #OBS.: There's no status packet for "makeSyncWritePacket()"
#        else:
#            return ans[8]#Byte of error status

    def getWord(self,memAddress,id_list):
        """
        Gets a list of IDs and return its Model Numbers
        inside a list (id0,data0,id1,data1,...idN,dataN)
        """
        if id_list == ():#Empty list
            return -1
        elif len(id_list) == 1:#Just one ID.
            pkt = Packet.makeReadPacket(id_list[0],memAddress)
        else:
            pkt = Packet.makeSyncReadPacket(memAddress,id_list)

        ans,err_num,err_str = self.serial.sendPkt(pkt)
        if ans == []:#In case of an empty packet arrives
            return -2
        else:
            data = []
            for index,val in enumerate(id_list):
                #print (index,val)
                data.append(val)                                    #Append the ID value
		#print str(index*13+10)
		#print str(index*13+9)
		try:
		    data.append(ans[index*13+9]+(ans[index*13+10] << 8))#Append the respective ID's data
            	except IndexError:
		    print 'Index Error: '+str(len(ans))
		return data

    """def getModelNumber(self, *id_list):
        print (id_list)
        print (type(id_list))
        if id_list == ():
            return -2
        if len(id_list) == 1:#Just one ID.
            pkt = Packet.makeReadPacket(id_list,xl320.XL320_MODEL_NUMBER)
            ans,err_num,err_str = self.serial.sendPkt(pkt)
            if ans == []:#In case of an empty packet arrives
                return -1
            else:
                return (ans[9]+(ans[10] << 8))
        else:
            pkt = Packet.makeSyncReadPacket(xl320.XL320_MODEL_NUMBER,id_list)
            ans,err_num,err_str = self.serial.sendPkt(pkt)
            if ans == []:
                return -1
            else:
                data = []
                for index,val in enumerate(id_list):
                    #print (index,val)
                    data.append(val)                                    #Append the ID value
                    data.append(ans[index*13+9]+(ans[index*13+10] << 8))#Append the respective ID's data
                return data"""


    def getModelNumber(self, *id_list):
        """
        Gets a list of IDs and return its Model Numbers
        inside a list (id0,data0,id1,data1,...idN,dataN)
        """
        if id_list == ():#Empty list
            return -1
        elif len(id_list) == 1:#Just one ID.
            pkt = Packet.makeReadPacket(id_list[0],xl320.XL320_MODEL_NUMBER)
        else:
            pkt = Packet.makeSyncReadPacket(xl320.XL320_MODEL_NUMBER,id_list)

        ans,err_num,err_str = self.serial.sendPkt(pkt)
        if ans == []:#In case of an empty packet arrives
            return -2
        else:
            data = []
            for index,val in enumerate(id_list):
                #print (index,val)
                data.append(val)                                    #Append the ID value
                data.append(ans[index*13+9]+(ans[index*13+10] << 8))#Append the respective ID's data
            return data

    def getFirmwareVersion(self, *id_list):
        """
        Gets a list of IDs and return its Firmware Version
        inside a list (id0,data0,id1,data1,...idN,dataN)
        """
        if id_list == ():#Empty list
            return -1
        elif len(id_list) == 1:#Just one ID.
            pkt = Packet.makeReadPacket(id_list[0],xl320.XL320_FIRMWARE_VERSION)
        else:
            pkt = Packet.makeSyncReadPacket(xl320.XL320_FIRMWARE_VERSION,id_list)

        ans,err_num,err_str = self.serial.sendPkt(pkt)
        if ans == []:#In case of an empty packet arrives
            return -2
        else:
            data = []
            for index,val in enumerate(id_list):
                #print (index,val)
                data.append(val)                                    #Append the ID value
                data.append(ans[index*12+9])#Append the respective ID's data
            return data

    def setID(self,curr_id,new_id):
        pkt = Packet.makeWritePacket(curr_id,xl320.XL320_ID,[new_id])
        ans,err_num,err_str = self.serial.sendPkt(pkt)
        if ans == []:#In case of an empty packet arrives
            return -2
        else:
            return ans[8]#Byte of error status

    def getID(self):
        pass

    def setBaudRate(self,ID,new_baudrate):
        pass
