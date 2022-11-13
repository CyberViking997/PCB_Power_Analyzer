import json
import copy

def parserJSONFile(filename):
    file = None
    zeroOffset = [0,0]

    ELEMENTS = {}

    TRACKS = []
    VIAS = []

    #########################################################################################
    file = open(filename, encoding="utf8")
    PCBData = json.load(file)

    # Save the offset of the points
    zeroOffset[0] = float(PCBData['head']['x'])
    zeroOffset[1] = float(PCBData['head']['y'])

    for i in PCBData['shape']:
        objType = i.split("~")[0]
        if objType == "VIA":
            VIAS.append(decodeVIA(i, zeroOffset))
        elif objType == "TRACK":
            TRACKS.append(decodeTRACK(i, zeroOffset))
        elif objType == "COPPERAREA":
            print("THIS IS COPPERAREA")
        elif objType == "PAD":
            print("THIS IS PAD")
        elif objType == "LIB":
            print("THIS IS LIB")
            decodeLIB(i,zeroOffset)
        else:
            print(i.split("~"))

    file.close()

    ELEMENTS['VIAS'] = VIAS
    ELEMENTS['TRACKS'] = TRACKS

    return ELEMENTS


def decodeVIA(VIA_string, offset):

    data = VIA_string.split("~")

    viaData = {}
    viaData['CENTER_POSITION'] = [float(data[1]) - offset[0], float(data[2]) - offset[1]]
    viaData['PAD_RADIUS'] = float(data[3])/2
    viaData['HOLE_RADIUS'] = float(data[5])
    viaData['NET'] = data[4]
    viaData['ID'] = data[6]
    viaData['IS_LOCKED'] = data[7]

    return viaData

def decodeTRACK(TRACK_string, offset):
    data = TRACK_string.split("~")

    trackData = {}
    trackData['WIDTH'] = float(data[1])
    trackData['LAYER'] = int(data[2])
    trackData['NET'] = data[3]
    trackData['ID'] = data[-2]
    trackData['IS_LOCKED'] = data[-1]

    pointList = []
    p = data[4].split(' ')
    for i in range(0,len(p),2):
        pointList.append([float(p[i]) - offset[0], float(p[i + 1]) - offset[1]])

    trackData['POINT_LIST'] = copy.deepcopy(pointList)


    return trackData

def decodeLIB(LIB_string, offset):
    for s in LIB_string.split("~"):
        print(s)