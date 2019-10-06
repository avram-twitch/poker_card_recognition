# handIdentifier
# Evan Parry
# October 6, 2019
# Last updated October 6, 2019
# Designed for HackTheU Hackathon
#
# This program lets the user input values to create a poker hand file.


fileName = raw_input("What do you want to call this file? (do not include .txt extension): ")
fileName += ".txt"
f = open(fileName, "w")

#Creates five lines for five cards.
for i in range(5):
    print("Creating card " + str(i+1))
    cardRank = raw_input("What is this card's rank? ")
    cardSuit = raw_input("what is this card's suit? ")
    inputString = str(cardRank)+","+str(cardSuit)
    f.write(inputString + "\n")
    
f.close()
    