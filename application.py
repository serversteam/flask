import flask
from flask import render_template, redirect, request, session, url_for
import os
import json
from flask import render_template_string,Markup
import collections
import csv
import datetime
import pandas as pd
from operator import itemgetter

application = flask.Flask(__name__)

#-----DATA FOR FILTER PAGE
data = []
with open('metadataBet.csv', 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
            data.append(row)
f.close()

pandaData = pd.DataFrame(data)

filterStrings = []

for x in range(len(data)):
    filterStrings.append(data[x][0])

#-----DATA FOR POSITION PAGE
data = []
with open('metadataPos.csv', 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
            data.append(row)
f.close()

pandaData = pd.DataFrame(data)

positionStrings = []

for x in range(len(data)):
    positionStrings.append(data[x][0])


@application.route('/', methods = ['GET', 'POST'])
def result():
    global userInput
    userInput = []
    global response
    response = []
    global filteredData
    filteredData = []
    global dataResponse
    dataResponse = {'location': [], 'gameDate':[], 'series':[], 'court':[], 'surface':[],
                   'tournamentRound': [], 'bestOf':[], 'player':[], 'opponent':[], 'outcome':[],
                    'playerScore': [], 'opponentScore':[], 'comment':[], 'avgOddsPlayer':[], 'avgOddsOpponent':[]}

    if flask.request.method == 'POST':
        userInput = []
        userInput = request.form

        e = dict([(int(x), userInput[str(x)]) for x  in range(1,len(userInput))])

        userInput = [i[1].encode('ascii') for i in e.items()]

        for x in range(len(userInput)):
            response.append(userInput[x]) 

        if 1 == 1:  #just doing this to be able to minimize this section
            #CREATE LIST OF ALGOS
            jsonString = {}
            jsonColumn = {}
            jsonType = {}
            jsonAction = {}
            jsonStringCheck = {}
            jsonYN = {}

            data = []

            with open('metadataBet.csv', 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            f.close()

            for x in range(len(data)):
                jsonString[x] = data[x][0]
                jsonColumn[x] = data[x][1]
                jsonType[x] = data[x][2]
                jsonAction[x] = data[x][3]
                jsonStringCheck[x] = data[x][4]
            
            algos = len(jsonType)

            #RUN EACH ALGO
            tempData = []

            with open('temp.csv', 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    tempData.append(row)
            f.close()

            games = len(tempData)

            jsonInput = {}

            for x in range(algos - 1): #gather all inputs
                jsonInput[x] = response[x]
                if len(jsonInput[x]) > 0:
                    jsonYN[x] = "y"
                else:
                    jsonYN[x] = "n"

            #print datetime.datetime.now()

            for x in range(algos - 1): #check and/or convert input type
                i = jsonInput[x]
                t = jsonType[x]
                #print x
                #print jsonString[x]
                #print i
                #print t
                #print '------'

                if t == "integer" and len(i) > 0:
                    jsonInput[x] = int(i)
                elif t == "string" and len(i) > 0:
                    jsonInput[x] = str(i)
                elif t == "float" and len(i) > 0:
                    jsonInput[x] = float(i)
                elif t == "leftmatch" and len(i) > 0:
                    jsonInput[x] = str(i)

            gameNumbers = []

            ctn = 0
            totalCtn = 0
            fulfilled = []

            for y in range(games):
                fulfilled.append(0)

            for x in range(algos - 1): #go algo by algo and get the data
                c = int(jsonColumn[x])
                t = jsonType[x]
                i = jsonInput[x] # this doesnt work
                a = jsonAction[x]
                tc = jsonStringCheck[x]
                yn = jsonYN[x]
                
                if yn == "y": #check input > 0
                    
                    ctn = ctn + 1

                    for y in range(games):
                        
                        toCheck = tempData[y][c]
                        doIt = False

                        if t == "integer":
                            toCheck = int(toCheck)
                        elif t == "string":
                            ii = i.lower()
                            i = ii
                            toCheck = toCheck.lower()
                            toCheck = str(toCheck)
                        elif t == "float":
                            toCheck = float(toCheck)
                        
                        if a == "exact" and toCheck == i:
                            doIt = True
                        elif a == "higher" and toCheck > i:
                            doIt = True
                        elif a == "lower" and toCheck < i:
                            doIt = True
                        elif a == "exclude" and toCheck <> tc:
                            doIt = True
                        elif a == "leftexact":
                            q = len(i)
                            cutToCheck = str(toCheck[:q])
                            if str(cutToCheck) == str(i):
                                doIt = True                
                        elif a == "leftmatch":
                            q = len(i) + 1
                            cutToCheck = str(toCheck[1:q])
                            if str(cutToCheck) == str(i):
                                doIt = True
                        else:
                            doIt = False

                        if doIt == True:
                            fulfilled[y] = fulfilled[y] + 1


            for x in range(games):
                if fulfilled[x] == ctn:
                    filteredData.append([tempData[x][0], tempData[x][1], tempData[x][2], tempData[x][3], tempData[x][4], tempData[x][5], tempData[x][6], tempData[x][7], 
                    tempData[x][8], tempData[x][9], tempData[x][10], tempData[x][11], tempData[x][12], tempData[x][13], tempData[x][14], 
                    tempData[x][15], tempData[x][16], tempData[x][17], tempData[x][18], tempData[x][19], tempData[x][20], tempData[x][21], 
                    tempData[x][22], tempData[x][23], tempData[x][24], tempData[x][25], tempData[x][26], tempData[x][27], tempData[x][28], 
                    tempData[x][29], tempData[x][30], tempData[x][31], tempData[x][32], tempData[x][33], tempData[x][34], tempData[x][35], 
                    tempData[x][36], tempData[x][37],
                    tempData[x][38], tempData[x][39],
                    tempData[x][40], tempData[x][41],
                    tempData[x][42], tempData[x][43], tempData[x][44], tempData[x][45],
                    ])

                    totalCtn = totalCtn + 1

            #WRITE THE DATA INTO TEMP
            with open('tempUser.csv', "wb") as f:
                writer = csv.writer(f)
                writer.writerows(filteredData)
            f.close()

            #WRITE THE DATA INTO JSON
            dataResponse = {'location': [], 'gameDate':[], 'series':[], 'court':[], 'surface':[],
                            'tournamentRound': [], 'bestOf':[], 'player':[], 'opponent':[], 'outcome':[],
                            'playerScore': [], 'opponentScore':[], 'comment':[], 'avgOddsPlayer':[], 'avgOddsOpponent':[],
                            'playerWorldRank': [], 'opponentWorldRank':[] }


            #for x in range(10):
            for x in range(len(filteredData)):
                dataResponse['location'].append(filteredData[x][2])
                dataResponse['gameDate'].append(filteredData[x][3])
                dataResponse['series'].append(filteredData[x][4])
                dataResponse['court'].append(filteredData[x][5])
                dataResponse['surface'].append(filteredData[x][6])
                dataResponse['tournamentRound'].append(filteredData[x][7])
                dataResponse['bestOf'].append(filteredData[x][8])
                dataResponse['player'].append(filteredData[x][9])
                dataResponse['opponent'].append(filteredData[x][10])
                dataResponse['outcome'].append(filteredData[x][11])
                dataResponse['playerScore'].append(filteredData[x][26])
                dataResponse['opponentScore'].append(filteredData[x][27])
                dataResponse['comment'].append(filteredData[x][28])
                dataResponse['avgOddsPlayer'].append(filteredData[x][29])
                dataResponse['avgOddsOpponent'].append(filteredData[x][33])
                dataResponse['playerWorldRank'].append(filteredData[x][12])
                dataResponse['opponentWorldRank'].append(filteredData[x][13])

            #print ctn
            #print totalCtn

            print datetime.datetime.now()
          
        #return redirect(url_for('outcomeDataFilter'))
        return redirect(url_for('inputPositions'))

    return render_template("criteriaFilter.html",lt = filterStrings)


@application.route('/betDataOutput',methods = ['GET', 'POST']) #do we need this?
def outcomeDataFilter():
    if flask.request.method == 'POST':
        return redirect(url_for('result'))
    else:
        k = pd.DataFrame(dataResponse)[['gameDate', 'series', 'location', 'surface', 'court', 'tournamentRound', 'bestOf', 
            'player', 'opponent', 'outcome', 
            'playerScore', 'opponentScore', 'comment', 'avgOddsPlayer',
            'avgOddsOpponent', 'playerWorldRank', 'opponentWorldRank']].to_html(index = False)
        return render_template("betDataOutput.html",outcome = k)


@application.route('/posDataInput',methods = ['GET', 'POST'])
def inputPositions():
    global marketData
    marketData = []
    global posResponse
    posResponse = {'capitalBefore':[], 'bet':[], 'price':[], 'outcome':[], 'profit':[], 'capitalAfter':[],
                    'gameDatePos': [], 'playerPos':[], 'opponentPos':[], 'playerScorePos':[], 'opponentScorePos':[],
                    'tournamentPos':[],'surfacePos':[]}
    
    if flask.request.method == 'POST':
        userInput = []
        userInput = request.form

        e = dict([(int(x), userInput[str(x)]) for x  in range(1,len(userInput) + 1)])

        userInput = [i[1].encode('ascii') for i in e.items()]

        response = []
        for x in range(len(userInput)):
            response.append(userInput[x])

        if 1 == 1:  #just doing this to be able to minimize this section
            data = []
            jsonInputs = {}
            jsonString = {}
            jsonType = {}
            jsonRequired = {}

            with open('metadataPos.csv', 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            f.close()

            for x in range(len(data)):
                jsonString[x] = data[x][0]
                jsonType[x] = data[x][1]
                jsonRequired[x] = data[x][2]

            errorMessage = False

            for x in range(len(data)):
                y = response[x]

                if jsonRequired[x] == "y" and len(y) == 0:
                    errorMessage = True
                elif jsonRequired[x] == "n" and len(y) == 0:
                    jsonInputs[x] = 0

                if jsonType[x] == "string"  and len(y) > 0:
                    jsonInputs[x] = str(y)
                    lowerString = y.lower()
                    jsonInputs[x] = lowerString
                elif jsonType[x] == "integer" and len(y) > 0:
                    jsonInputs[x] = int(y)
                elif jsonType[x] == "float" and len(y) > 0:
                    jsonInputs[x] = float(y)

            #GATHER DATA
            marketData = []
            with open('tempUser.csv', 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    marketData.append(row)
            f.close()

            #DETERMINE STARTING BET
            #print errorMessage
            if errorMessage == False:
                startCapital = jsonInputs[0]
                capitalBefore = startCapital
                baseBetType = jsonInputs[5]

                if baseBetType == "f":
                    baseBet = jsonInputs[6]
                elif baseBetType == "p":
                    betPct = jsonInputs[6]
                    baseBet = startCapital * betPct
                else:
                    errorMessage = True
                
                priceType = jsonInputs[2]

            
            #CREATE POSITIONS
            useMultWin = False #identify multipliers----------------
            useMultLoss = False
            useMaxMult = False

            if jsonInputs[7] <> 0:
                multWin = jsonInputs[7]
                useMultWin = True

            if jsonInputs[8] <> 0:
                multLose = jsonInputs[8]
                useMultLoss = True

            if (useMultWin == True or useMultLoss == True) and jsonInputs[9] <> 0:
                maxMult = jsonInputs[9]
                useMaxMult = True

            if jsonInputs[10] <> 0:
                multAction = jsonInputs[10]

            for x in range(len(marketData)):

                if x > 0: #stop when you have lost all your money
                    if capitalAfter <= 0:
                        print 'aaaaa'
                        break

                if x == 0: #define capital------------------------------
                    capitalBefore = startCapital
                    lastOutcome = "flat"
                else:
                    if capitalAfter > capitalBefore:
                        lastOutcome = "won"
                    else:
                        lastOutcome = "lost"
                    capitalBefore = capitalAfter

                if x == 0 and baseBetType == "f": #define bet----------------------
                    bet = baseBet
                if x == 0 and baseBetType == "p":
                    bet = startCapital * betPct
                if x > 0 and baseBetType == "f" and useMultWin == False and useMultLoss == False:
                    bet = baseBet
                if x > 0 and baseBetType == "p" and useMultWin == False and useMultLoss == False:
                    bet = capitalBefore * betPct
                if x > 0 and baseBetType == "f" and (useMultWin == True or useMultLoss == True):
                    bet = bet
                if x > 0 and baseBetType == "p" and (useMultWin == True or useMultLoss == True):
                    bet = bet
                
                lastBet = bet

                if useMultWin == True: #adjust bet by multiplier winner
                    if lastOutcome == "won":
                        bet = lastBet * multWin

                        if baseBetType == "f" and useMaxMult == True:
                            maxBetAmount = baseBet * maxMult
                        elif baseBetType == "p" and useMaxMult == True:
                            maxBetAmount = betPct * maxMult * capitalAfter
                        else:
                            maxBetAmount = startCapital * 100000

                        if bet > maxBetAmount and multAction == "r":
                            if baseBetType == "f":
                                bet = baseBet
                            elif baseBetType == "p":
                                bet = capitalAfter * betPct
                        elif bet > maxBetAmount and multAction == "c":
                            bet = lastBet
                        elif bet < startCapital * 0.0001:
                            print 'aaaaa'
                            break
                        elif bet <= maxBetAmount:
                            bet = bet

                    elif lastOutcome == "lost" or lastOutcome == "flat":
                        if baseBetType == "f":
                            bet = baseBet
                        elif baseBetType == "p":
                            bet = capitalBefore * betPct


                if useMultLoss == True: #adjust bet by multiplier loser
                    if lastOutcome == "lost":
                        bet = lastBet * multLose

                        if baseBetType == "f" and useMaxMult == True:
                            maxBetAmount = baseBet * maxMult
                        elif baseBetType == "p" and useMaxMult == True:
                            maxBetAmount = capitalAfter * betPct * maxMult
                        else:
                            maxBetAmount = startCapital * 100000

                        if bet > maxBetAmount and multAction == "r":
                            if baseBetType == "f":
                                bet = baseBet
                            elif baseBetType == "p":
                                bet = capitalAfter * betPct
                        elif bet > maxBetAmount and multAction == "c":
                            bet = lastBet
                        elif bet < startCapital * 0.0001:
                            print 'aaaaa'
                            break
                        elif bet <= maxBetAmount:
                            bet = bet

                    elif lastOutcome == "won" or lastOutcome == "flat":
                        if baseBetType == "f":
                            bet = baseBet
                        elif baseBetType == "p":
                            bet = capitalBefore * betPct

                if x > 0: #don't bet more money than you have in the account
                    if bet > capitalAfter:
                        bet = capitalAfter
                elif x == 0 and bet > capitalBefore:
                    bet = capitalBefore

                if jsonInputs[3] <> 0: #define the spread----------------
                    spread = jsonInputs[3]
                else:
                    spread = 0

                spread = float(spread)

                if jsonInputs[4] <> 0: #define commission----------------
                    fee = 1 - jsonInputs[4]
                else:
                    fee = 1

                fee = float(fee)

                if jsonInputs[2] == 1: #define price---------------------
                    price = marketData[x][29]
                elif jsonInputs[2] == 2:
                    price = marketData[x][30]
                elif jsonInputs[2] == 3:
                    price = marketData[x][31]
                elif jsonInputs[2] == 4:
                    price = marketData[x][32]
                
                price = float(price) + spread
                
                if price < 1:
                    price = 1

                outcome = marketData[x][11] #get outcome----------------

                betDirection = jsonInputs[1]#get bet direction----------

                if outcome == "w" and betDirection == "back": #define profit and apply fee----------------
                    profit = (bet * price - bet) * fee
                elif outcome == "l" and betDirection == "lay":
                    profit = bet * fee
                elif outcome == "w" and betDirection == "lay":
                    profit = - bet * price + bet
                elif outcome == "l" and betDirection == "back":
                    profit = - bet

                capitalAfter = capitalBefore + profit #define capital after----------------      

                posResponse['capitalBefore'].append(capitalBefore)
                posResponse['bet'].append(bet)
                posResponse['price'].append(price)
                if betDirection == "lay" and outcome == "w":
                    posResponse['outcome'].append("l")
                elif betDirection == "lay" and outcome == "l":
                    posResponse['outcome'].append("w")
                else:
                    posResponse['outcome'].append(outcome)

                posResponse['profit'].append(profit)
                posResponse['capitalAfter'].append(capitalAfter)
                posResponse['gameDatePos'].append(marketData[x][3]) #to be reviewed
                posResponse['playerPos'].append(marketData[x][9]) #to be reviewed
                posResponse['opponentPos'].append(marketData[x][10]) #to be reviewed
                posResponse['playerScorePos'].append(marketData[x][26]) #to be reviewed
                posResponse['opponentScorePos'].append(marketData[x][27]) #to be reviewed
                posResponse['tournamentPos'].append(marketData[x][2]) #to be reviewed
                posResponse['surfacePos'].append(marketData[x][6]) #to be reviewed
            
            #print json.dumps(posResponse,indent=4, separators=(',', ': '))
            return redirect(url_for('outcomePosition'))

    #elif flask.request.method == 'GET':
    #    return redirect(url_for('userGivesPositionInputs'))

    return render_template("criteriaPosition.html",lt = positionStrings)

@application.route('/posDataOutput',methods = ['GET', 'POST'])
def outcomePosition():
    if flask.request.method == 'POST':
        return redirect(url_for('result'))#
    else:
        k = pd.DataFrame(posResponse)[['capitalBefore', 'bet', 'price', 'outcome', 'profit', 'capitalAfter',
         'gameDatePos', 'playerPos','opponentPos', 'playerScorePos', 'opponentScorePos',
         'tournamentPos', 'surfacePos']].to_html(index = False)
        return render_template("betDataOutput.html",outcome = k)


if __name__ == '__main__':
   application.run(debug = True)