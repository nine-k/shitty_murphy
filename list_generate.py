from readchar import readchar

allWords = open("allWords.txt", 'r')
words = open("words.txt", 'w')

for line in allWords:
    for word in line.split():
        print(word)
        ans = readchar()
        if (ans ==  'y' or ans == 'Y'):
            words.write(word + ' ')
            print("addedd to words")
words.write('\n')
