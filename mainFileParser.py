from html.parser import HTMLParser
from html.entities import name2codepoint
import codecs
import cv2
import urllib
import math

import cv2
import urllib.request
class MainWebsiteHTMLParser(HTMLParser):

    htmlList = []
    imgList = []
    def handle_starttag(self, tag, attrs):
        handle = False
        for attr in attrs:
            print(attr)
            if attr[0] == 'href':
                if "http://www.animalplanet.com/wild-animals/endangered-species/" in attr[1] and attr[1] not in self.htmlList:
                    self.htmlList.append(attr[1])
            elif attr[0] == 'data-desktop-src':
                if "FRONT-PAGE" in attr[1] and attr[1] not in self.imgList:
                    self.imgList.append(attr[1])


class IndividualAnimalWebsiteHTMLParser(HTMLParser):

    animalNumList = []
    checkNum = False
    def handle_starttag(self, tag, attrs):
        handle = False
        for attr in attrs:
            pass
            #print(attr)

    def handle_data(self, data):
        #print("Data     :", data)
        if self.checkNum:
            self.checkNum = False
            nums = []
            for word in data.split():
                for subsplit in word.split('-'):
                    try:
                        num = float(subsplit.replace(',', ''))
                        nums.append(num)
                    except:
                        pass
            self.animalNumList.append(nums)
        if("Number Remaining:" in data):
            self.checkNum = True




if __name__ == "__main__":
    parser = MainWebsiteHTMLParser()
    parser.feed(codecs.open("EndangeredSpecies.htm").read())
    webpageList = parser.htmlList[2:]
    imgHTMLList = parser.imgList
    print(len(webpageList))
    print(len(imgHTMLList))
    i=0

    for page in webpageList:
        response = urllib.request.urlopen(page)
        htmlFile = response.read()
        htmlString = htmlFile.decode('utf-8')
        smallParser = IndividualAnimalWebsiteHTMLParser()
        smallParser.feed(htmlString)
        if len(smallParser.animalNumList)==i:
            smallParser.animalNumList.append(None)
        #print(imgHTMLList[i])
        i += 1;
        #print(page)
    i = 0
    numList = smallParser.animalNumList
    imageDir = []
    for imageUrl in imgHTMLList:
        imageDir.append("animalImages/{}.jpg".format('-'.join((imageUrl.split('/')[-1]).split('-')[0:-2])))
        urllib.request.urlretrieve(imageUrl, imageDir[i])
        i += 1
    i = 0
    for imagePath in imageDir:
        if numList[i] is not None:
            img = cv2.imread(imagePath)
            sum = 0
            for num in numList[i]:
                sum += num
            avg = float(sum/float(len(numList[i])))
            width = math.sqrt(avg) #width and height are the same
            width = int(math.floor(width))
            img = cv2.resize(img, (width, width))
            img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_NEAREST)
            firstStr = imageDir[i].split('/')[-1][:-4].replace('-', ' ').title()
            if(len(numList[i]) > 1):
                str = "Estimated between {} and {} remain".format(int(numList[i][0]), int(numList[i][1]))
            else:
                str = "Estimated about {} remain".format(int(numList[i][0]))

            cv2.putText(img, firstStr, (5,35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA, thickness=2)
            cv2.putText(img, str, (5,70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), lineType=cv2.LINE_AA, thickness=2)
            cv2.imwrite("outputImages/{}.jpg".format(firstStr.replace(' ','')), img)
        i += 1







