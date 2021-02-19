"""
dependencies:
    selenium 
    validator
    Pillow
    requests
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import mcpi.minecraft as minecraft
import mcpi.block as block
import validators
import sys
import time
from PIL import Image
import shutil
import os
import PIL
import requests
import io

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()

def printPage(URL,size=20):
    try:
        pos = mc.player.getTilePos()
        if URL is not None and validators.url(URL):
            start = time.time()
            os.mkdir('tmp')
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=firefox_options,executable_path='C:/Users/Leonl/Desktop/AdventuresInMinecraft-PC/MyAdventures/geckodriver/geckodriver.exe')
            mc.postToChat("browser init ({})".format(driver.service))
            # to maximize the browser window
            driver.maximize_window()
            #get method to launch the URL
            driver.get(URL)
            #to refresh the browser
            driver.refresh()
            sleep(5)
            mc.postToChat("URL loaded")
            body = driver.find_element("tag name",'body')
            webpage_height = body.size["height"]

            driver.set_window_size(body.size["width"], webpage_height)
            mc.postToChat("page height: " + str(int(webpage_height)) + " px")
            #to get the screenshot of complete page
            driver.save_screenshot("tmp/website.png")
            sleep(1)
            #to close the browser
            driver.close()

            mc.postToChat("Screenshot saved")

            img = Image.open('tmp/website.png')


            mc.postToChat('resizing... (reducing by {})'.format(size))
            img = img.resize((int(img.size[0]/(int(size))), int(img.size[1]/(int(size)))))
            mc.postToChat('converting...')
            img = img.convert('RGB')

            mc.postToChat('printing...')
            width, height = img.size
            for x in range(width):
                for y in range(height):
                    r, g, b = img.getpixel((x, y))
                    print('printing at x:{} y:{} (x:{} y:{} z: {} minecraft)'.format(x, y, x + pos.x, pos.y, y + pos.z))
                    if (r < 255 and g < 255 and b < 255) and (r > 180 and g > 180 and b > 180):
                        mc.setBlock(x + pos.x, pos.y, y + pos.z, block.WOOL.id, 15)  # y => z cordinate in minecraft
                    elif (r <= 0 and g <= 0 and b <= 0) and (r > 100 and g > 100 and b > 100):
                        mc.setBlock(x + pos.x, pos.y, y + pos.z, block.WOOL.id, 0)  # y => z cordinate in minecraft
                    else:
                        mc.setBlock(x + pos.x, pos.y, y + pos.z, block.WOOL.id, 7)  # y => z cordinate in minecraft

            end = time.time()
            delta = end - start
            mc.postToChat('printed (in ~{}s)'.format(delta))
            print('printed (in ~{}s)'.format(delta))

            shutil.rmtree('tmp')#clean image in temporary folder
        else:
            mc.postToChat("given URL (" + URL + ") is invalid or null !")
    except Exception as e:
        mc.postToChat("Error: " + str(e))
        print("Error: " + str(e),file=sys.stderr)
        sys.exit(1)
def printImage(URL,size=20):
    try:
        pos = mc.player.getTilePos()
        if URL is not None and validators.url(URL):
            start = time.time()

            mc.postToChat('fetching image...')
            response = requests.get("https://i.imgur.com/ExdKOOz.png")
            image_bytes = io.BytesIO(response.content)

            img = PIL.Image.open(image_bytes)


            mc.postToChat('resizing... (reducing by {})'.format(size))
            img = img.resize((int(img.size[0]/(int(size))), int(img.size[1]/(int(size)))))
            mc.postToChat('converting...')
            img = img.convert('RGB')

            mc.postToChat('printing...')
            width, height = img.size
            for x in range(width):
                for y in range(height):
                    r,g,b = img.getpixel((x, y))
                    print('printing at x:{} y:{} (x:{} y:{} z: {} minecraft)'.format(x,y,x + pos.x, pos.y, y + pos.z))
                    if (r < 255 and g < 255 and b < 255) and (r > 180 and g > 180 and b > 180):
                        mc.setBlock(x + pos.x, pos.y, y + pos.z,block.WOOL.id,15)#y => z cordinate in minecraft
                    elif (r <= 0 and g <= 0 and b <= 0) and (r > 120 and g > 120 and b > 120):
                        mc.setBlock(x + pos.x, pos.y, y + pos.z, block.WOOL.id,0)  # y => z cordinate in minecraft
                    else:
                        mc.setBlock(x + pos.x, pos.y, y + pos.z, block.WOOL.id, 7)  # y => z cordinate in minecraft

            end = time.time()
            delta = end - start
            mc.postToChat('printed (in ~{}s)'.format(delta))
            print('printed (in ~{}s)'.format(delta))

        else:
            mc.postToChat("given URL (" + URL + ") is invalid or null !")
    except Exception as e:
        mc.postToChat("Error: " + str(e))
        print("Error: " + str(e),file=sys.stderr)
        sys.exit(1)


while True:
    chatCommands = mc.events.pollChatPosts()
    for chatCommand in chatCommands:
        if chatCommand.message[0] == "!":
            if chatCommand.message.split(" ")[0] == "!printWebpage":
                args = chatCommand.message.split(" ")
                mc.postToChat('starting printing process')
                if not args[2]: args[2] = 20
                printPage(args[1],args[2])
            elif chatCommand.message.split(" ")[0] == "!printImage":
                args = chatCommand.message.split(" ")
                mc.postToChat('starting printing process')
                if not args[2]: args[2] = 20
                printImage(args[1], args[2])
            else:
                        mc.postToChat('invalid command: ' + chatCommand.message)
                        mc.events.clearAll()
        else:
                mc.events.clearAll()
                    