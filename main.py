import cv2
import time
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        # white rectangle:
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (225, 225, 225),
                      cv2.FILLED)
        # black border
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)

        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        # check if index finger is inside any boxes x1 < x < x1+width, y1 < y < y1+height
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            #lighter white rectangle
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            # black border
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)

            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0),
                        5)
            return True
        else:
            return False
# Webcam
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
#cap.set(5, 60) #sets framerate target

detector = HandDetector(detectionCon=0.8, maxHands=1)


#creating buttons
buttonsListValues = [['7', '8', '9', '*'],
                     ['4', '5', '6', '-'],
                     ['1', '2', '3', '+'],
                     ['0', '/', '.', '=']]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x*100 + 800
        ypos = y*100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonsListValues[y][x]))

# variables
myEquation = ''
delayCounter = 0

# frame rate
pTime = 0
cTime = 0
# loop for webcam detection
while True:
    success, img = cap.read()
    # flip image horizontally
    img = cv2.flip(img, 1)

    # detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # draw the output bar and all buttons
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (225, 225, 225),
                  cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (50, 50, 50), 3)
    for button in buttonList:
        button.draw(img)

    #find the distance between fingers
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[4], img) #index finger and thumb
        cv2.putText(img, str(int(length)), (1100, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255),
                    3)
        x, y = lmList[8]
        if length < 50:
            for i, button in enumerate(buttonList): #gives the loop index so that we know which button is clicked
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = buttonsListValues[int(i%4)][int(i/4)] #column row format
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

    #Avoid duplicate inputs: make a counter that starts counting when click is true
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    #Display the equation
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    #display framerates
    cTime = time.time()
    fps = 1 / (cTime - pTime)  # calculate frames per second
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255),
                3)  # on top of object, number converted to integer, position, font, size, color, thickness

    # display image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''