import subprocess
import random
from time import sleep

REQUEST_TIMEOUT = 10

POSTS_TO_GENERATE = 50
postsGenerated = 0

def cleanLine(data):
    data.encode('ascii', 'ignore')
    res = ''
    for i in data:
        if (i.isalpha() or i.isdigit() or i == ' ' or i == '.'):
            res += i
    return res

def isImageFromMurphy(data):
    return 'MurphyBot' in data and 'photo' in data

def isImageGenerationError(data):
    return 'MurphyBot' in data and '...' in data


def getMessageNumber(data):
    res = ''
    pos = 0
    while not data[pos].isdigit():
        pos += 1
    while data[pos].isdigit():
        res += data[pos]
        pos += 1
    return res

wordList1 = []
wordList2 = []

with open("words.txt", 'r') as f:
    for line in f:
        wordList1.append(line.strip())

with open("actor_names.txt", 'r') as f:
    for line in f:
        wordList2.append(line.strip())

def generateRequest():
    word1 = random.choice(wordList2)
    word2 = random.choice(wordList1)
    return "msg MurphyBot what if " + word1 + " was " + word2 + " ?\n"

print(generateRequest())

tg = subprocess.Popen(["tg/bin/telegram-cli", "-CWNk", "tg/tg-server.pub"],
                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)

for line in iter(tg.stdout.readline, ''):
    line = line.decode('UTF-8')
    line = cleanLine(line) #delete most of the unneeded characters
    if isImageGenerationError(line):
        print("Murphy couldnt make it")
        tg.stdin.write(bytes(generateRequest(), 'UTF-8'))
        tg.stdin.flush()
        postsGenerated -= 1
        sleep(5)

    if isImageFromMurphy(line): #if murphy sent an image download it and send a new request
        print("got an image from Murphy!")
        msgid = getMessageNumber(line)
        tg.stdin.write(bytes('load_photo ' + msgid + '\n', 'UTF-8')) #image is loaded to ~/.telegram-cli/downloads
        tg.stdin.flush()
        sleep(REQUEST_TIMEOUT)
        tg.stdin.write(bytes(generateRequest(), 'UTF-8'))
        tg.stdin.flush()
        sleep(5)
        postsGenerated += 1
        print("Generated", postsGenerated, "posts")
        if postsGenerated > POSTS_TO_GENERATE:
            tg.stdin.close()
            tg.stdout.close()
            tg.terminate()
