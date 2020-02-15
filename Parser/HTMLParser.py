from selenium import webdriver
from bs4 import BeautifulSoup
import os, shutil
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import requests

def startParser():
    dirToScrapeIn = "."
    folder = dirToScrapeIn + '/' + "Scraped"
    if(os.path.isdir(folder)):
        shutil.rmtree(folder)

    if not os.path.exists(folder):
        os.makedirs(folder)

    while True:
        inputLink = str(input("Enter the URL to scrape \nor leave the field empty to exit: "))
        print(inputLink.replace('\n', ''))
        if inputLink == '':
            print("Nothing entered!")
            exit(0)

        hostname = inputLink.split('/')
        try:
            finalDomain = hostname[2].replace('.', '_')
        except:
            finalDomain = hostname[1].replace('.', '_')
        print(finalDomain)

        # Make new directory if it doesn't exist.
        dirName = folder + "/" + finalDomain
        if not os.path.exists(dirName):
            os.makedirs(dirName)

#*******Requests**********
#! *******************************************************    
        try:    
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
            html = requests.get(inputLink, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            bodyContent = soup.body
            # Remove all script and style elements
            for script in bodyContent(["script", "style"]):
                script.decompose()
            bodyContentTxt = bodyContent.get_text()
            bodyContentStr = str(bodyContentTxt)
            bodyWithoutSpaces = bodyContentStr.replace(" ","")
            bodyWithoutSpaces = bodyContentStr.replace("\n","")
            bodyContentLength = len(bodyWithoutSpaces)
            #print(bodyWithoutSpaces)
            print("Body content length: " + str(bodyContentLength))
        except Exception as e:
            print("Exception: " + str(e))
            
#! ******************************************************* 
#********Selenium**********
        if(bodyContentLength<1000):
            print("************Running selenium**************")
            try:
                driver = webdriver.Firefox()
                driver.get(inputLink)
                print(driver.title + '\n')
                html = driver.page_source
                driver.close()
                soup = BeautifulSoup(html, 'lxml')
                # Extract entire body's content
                bodyContent = soup.body
                # print(bodyContent)
            except Exception as e:
                print("Error: " + str(e))

        # Write the sites link in a file
        try:
            fobject = open(dirName+"/"+finalDomain+"_SiteLink.txt", "w")
            fobject.write(inputLink+"\n")
            fobject.close()
        except Exception as e:
            print("Error occurred: " + str(e))

        # Extract all the scripts in body
        try:
            scripts = soup.find_all('script')
            fobject = open(dirName+"/"+finalDomain+"_scripts.txt", "w")
            for i in range(0, len(scripts)):
                fobject.write(str(scripts[i].get("src"))+"\n")
            fobject.close()
        except Exception as e:
            print("Error: " + str(e))

        #Enable to see Raw body content
        '''
        try:
            fobject = open(dirName+"/"+finalDomain+"_bodyContent.txt", "w")
            for text in bodyContent:
                fobject.write(str(text))
            fobject.close()
        except Exception as e:
            print("Error: " + str(e))
        '''

        # Extract all the links in body
        try:
            linksInBody = bodyContent.find_all('a')
            fobject = open(dirName+"/"+finalDomain+"_linksInBody.txt", "w")
            for i in range(0, len(linksInBody)):
                fobject.write(str(linksInBody[i])+"\n")
            fobject.close()
        except Exception as e:
            print("Error: " + str(e))

        # Extract entire body content without tags
        try:
            garbageCounter = 0

            # Remove all script and style elements
            for script in bodyContent(["script", "style"]):
                script.decompose()

            bodyContentWithoutTags = bodyContent.get_text()
            fobject = open(dirName+"/"+finalDomain +
                           "_bodyContentWithoutTags.txt", "w")
            for text in bodyContentWithoutTags:
                if text == '\n' or text == ' ':
                    garbageCounter += 1
                else:
                    garbageCounter = 0

                if garbageCounter <= 1:
                    fobject.write(str(text))
            fobject.close()
        except Exception as e:
            print("Error: " + str(e))

        contentCleaner(dirName, finalDomain)

def contentCleaner(dirName, finalDomain):
    print("\nCleaning..")
    cleanedString = ""
    
    fobject = open(dirName+"/"+finalDomain +"_bodyContentWithoutTags.txt", "r")
    for lineInFile in fobject:
        lineInFile = lineInFile[:-1]
        if lineInFile == '' or lineInFile == ' ':
            continue

        if len(lineInFile) < 3 or lineInFile.find(' ') == -1:
            cleanedString+=lineInFile+" "
        else:
            cleanedString+=lineInFile+"\n"
        #print(lineInFile)
    print(cleanedString)
    fobject.close()
    fobject = open(dirName+"/"+finalDomain +"_bodyContentWithoutTags.txt", "w")
    fobject.write(cleanedString)
    fobject.close()

startParser()