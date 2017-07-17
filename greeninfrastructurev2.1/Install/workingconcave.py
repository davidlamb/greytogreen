import arcpy
import math

class concaveHullSimple(object):
    #See:
    def __init__(self):
        self.pointList = []
        self.k = 30


    def createPolygon(self,points, k=3):#polygonList):
        print "Current k %s"%k
        self.pointList = []
        dataset = []
        #for poly in polygonList:
            #for part in poly:
                #for pnt in part:
                    #if pnt not in self.pointList:
                        #self.pointList.append(pnt)
                        #dataset.append(pnt)
        for pnt in points:
            self.pointList.append(pnt)
            dataset.append(pnt)

        print len(self.pointList)

        if len(self.pointList)<3:
            return None
        if k>len(self.pointList):
            return None


        firstPoint = self.findMinYPoint(self.pointList)
        print firstPoint

        hull = arcpy.Array()
        hull.append(firstPoint)
        currentPoint = firstPoint
        self.pointList.remove(firstPoint)
        previousPoint = firstPoint
        step = 2
        cutoff = math.floor(float(len(self.pointList))/2)
        while ((currentPoint != firstPoint) or (step==2)) and (len(self.pointList)>0):
            if step >1000000:
                print "loop kept going"
                break
            print "Step %s" %(step)
            if step ==cutoff:
                self.pointList.append(firstPoint)
            kNearestPoints = self.getNearestNeighbors(self.pointList,currentPoint,k)
            print "Number nearest points: %s"%(len(kNearestPoints))

            cpoints = self.sortByAngle(kNearestPoints,currentPoint,previousPoint)
            #print len(cpoints)
            cpoint = None
            its = True
            if hull.count >= 2:
                for cpoint in cpoints:
                    newEdge = arcpy.Polyline(arcpy.Array([currentPoint,cpoint]))
                    if firstPoint.equals(cpoint):
                        print "First Point matches cpoint"
                    crosses = False
                    for i in range(0,hull.count,1):
                        #try:
                        if i == hull.count-1:
                            #print "last check"
                            tempLine =arcpy.Polyline(arcpy.Array([hull[i],hull[0]]))
                            crosses = newEdge.crosses(tempLine)
                            #print "Crosses back %s"%crosses
                            break
                        tempLine =arcpy.Polyline(arcpy.Array([hull[i],hull[i+1]]))
                        crosses = newEdge.crosses(tempLine)
                        #print "Crosses %s"%(crosses)
                        if crosses == True:
                            break
                            #if cpoint.disjoint(tempLine) == True:
                                #print "Not on Edge"
                            #else:
                                #print "On Edge"
                        #except:
                            #print "error in crosses check"
                    if crosses == False:
                        its = False
                        break
            else:
                its = False
                cpoint = cpoints[0]
            if its == True:
                print "Intersects, probably should increase k"
                newk=k+1
                poly = self.createPolygon(points,newk)
                return poly
            previousPoint = currentPoint
            currentPoint = cpoint
            hull.append(cpoint)
            #for i in range(0,hull.count):
                #print "%s,%s"%(hull[i].X,hull[i].Y)
            self.pointList.remove(currentPoint)
            step+=1
        #hull.append(firstPoint)
        hullPolygon = arcpy.Polygon(hull)
        print "Part count %s" % hullPolygon.partCount
        if hullPolygon.partCount > 1:
            print "Not all points contained increasing k"
            newk=k+1
            if newk > len(points)-1:
                return None
            poly = self.createPolygon(points,newk)
            return poly
        contains = True
        #within = True
        #touches = True
        disj = False
        for pnt in dataset:
            contains = hullPolygon.contains(pnt)
            #within = pnt.within(hullPolygon)
            #touches = hullPolygon.touches(pnt)
            disj = hullPolygon.disjoint(pnt)
            #print contains
            if disj==True:
                print "Not all points contained increasing k"
                newk=k+1
                if newk > len(points)-1:
                    print "Exceeds the number of points"
                    return hullPolygon
                poly = self.createPolygon(points,newk)
                return poly
            #break

        return hullPolygon


    def findMinYPoint(self, pointList):
        minY = 10000000**10
        minPnt = arcpy.Point(0,0)
        for pnt in pointList:
            if pnt.Y < minY:
                minY = pnt.Y
                minPnt = pnt
        return minPnt

    def findMinlrPoint(self, pointList):
        minY = 10000000**10
        maxX = -(10000000**10)
        minPnt = arcpy.Point(0,0)
        for pnt in pointList:
            if pnt.Y <= minY and pnt.X >= maxX:
                minY = pnt.Y
                maxX = pnt.X
                minPnt = pnt
        return minPnt

    def getNearestNeighbors(self, pointList, point, k):
        distanceList = []
        for i, pnt in enumerate(pointList):
            distanceList.append((self.distance(point,pnt),i))
        distanceList.sort()
        nearest = []
        endLst = min(len(distanceList),k)
        for x in range(0,endLst):
            indx = distanceList[x][1]
            nearest.append(pointList[indx])
        return nearest


    def distance(self,point1,point2):
        dx = point1.X - point2.X
        dy = point1.Y - point2.Y
        return math.sqrt(dx*dx+dy*dy)

##    def sortByAngle(self,nearest,point,prevPoint):
##        angles = []
##        for indx,nearestPoint in enumerate(nearest):
##            angle1 =math.degrees(math.atan2(nearestPoint.Y - point.Y,nearestPoint.X - point.X))
##            angle2 = math.degrees(math.atan2(prevPoint.Y - point.Y,prevPoint.X - point.X))
##            #anglediff = math.atan2(nearestPoint.Y - point.Y,nearestPoint.X - point.X) - math.atan2(prevPoint.Y - point.Y,prevPoint.X - point.X)
##            #angle = math.degrees(anglediff)
##            angle1 = (angle1)%360
##            angle2 = (angle2)%360
##            angDiff=abs(angle1-angle2)
##            #angle = (angle)%360
##            angles.append((angDiff,indx))
##        angles.sort(reverse=True)
##        sortedNearest = []
##        for angle, indx in angles:
##            sortedNearest.append(nearest[indx])
##        return sortedNearest

    def sortByAngle(self,nearest,point,prevPoint):
        angles = []
        for indx,nearestPoint in enumerate(nearest):
            angle1 = math.atan2(prevPoint.Y - point.Y,prevPoint.X-point.X)
            angle2 = math.atan2(nearestPoint.Y - point.Y,nearestPoint.X-point.X)
            angleDiff = (180.0 / math.pi * (angle2-angle1))
            #angles.append((angleDiff%360,indx))
            if angleDiff>0:
                angles.append((360-angleDiff,indx))
            else:
                angles.append((-angleDiff,indx))
        angles.sort(reverse=True)
        sortedNearest = []
        for angle, indx in angles:
            sortedNearest.append(nearest[indx])
        return sortedNearest

    def AngleDegrees(self,fromPoint,toPoint):
        rad = math.atan2(toPoint.Y - fromPoint.Y,toPoint.X - fromPoint.X)
        return math.degrees(rad)



inputPointsPath = r"N:\Misc Projects\Grey_to_GreenInfrastructure\Communities\Tampa\smallsite.gdb\randomPnts50"
inputPointsPath = r"N:\Misc Projects\Grey_to_GreenInfrastructure\Communities\Tampa\smallsite.gdb\testpoints"
polygonInput =  r"N:\Misc Projects\Grey_to_GreenInfrastructure\Communities\Tampa\smallsite.gdb\squarearcprj"
outputPolygon = r"N:\Misc Projects\Grey_to_GreenInfrastructure\Communities\Tampa\smallsite.gdb\testhull"

pts = []
with arcpy.da.SearchCursor(inputPointsPath,["SHAPE@"]) as sc:
    for row in sc:
        pts.append(row[0].centroid)

with arcpy.da.SearchCursor(polygonInput,["SHAPE@"]) as sc:
    pts = []
    for row in sc:
        for part in row[0]:
            for pnt in part:
                within = False
                for test in pts:
                    if test.equals(pnt):
                        within = True
                        break
                if within == False:
                    pts.append(pnt)

conc = concaveHullSimple()
hullPoly = conc.createPolygon(pts,6)
print hullPoly.area

with arcpy.da.InsertCursor(outputPolygon,["SHAPE@"]) as ic:
    ic.insertRow([hullPoly])