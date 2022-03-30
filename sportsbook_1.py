"""
Name: Jake Bova
File: sportsbook_1.py
Date: 03/30/22
"""
import math
import pandas as pd
from sportsipy.ncaab.teams import Team


team1 = 'duke'  # 'north-carolina'
team2 = 'kansas'  # 'villanova'


# returns the values of predicted scores for each team, can be used for plusMinus and moneyLine (for predicted winner), as well as combined for overUnder bet
# to predict score, use NCAA games
def predictScore(t1, t2):
    pass


# line determined by combined predicted score
def overUnder(bet, choice, line):
    pass


# money line payouts determined by ratio of score difference times a constant
def moneyLine(bet, choice, line):
    pass


# line determined by difference in predicted scores (i.e. prediction for Duke vs Villanova is 75-72, Duke would have -3, Villa would get +3)
def plusMinus(bet, choice, line):
    pass


#  Will (top scoring player) score more than (average + 1)?
def skilledProp1(bet, choice, line):
    pass


# Will there be > (avg) turnovers?
def skilledProp2(bet, choice, line):
    pass


# Will the game go to overtime? (chance determined by history of overtime games in NCAA final)
# take each NCAA finals game (by date, using Boxscore), check if it went to overtime, create line based on ratio
def unskilledProp1(bet, choice, line):
    pass


# How many fouls will there be in the first half? (over/under avg fouls per game/2)
def unskilledProp2(bet, choice, line):
    pass


# makes an exotic prop 1 bet
def exoticProp1(bet, choice, line):
    pass


# makes an exotic prop 1 bet
def exoticProp2(bet, choice, line):
    pass


# outputs the betting info in sportsbook format
def displayData():
    pass


def makeBet(b_type, bet, choice):
    line = 0
    match b_type:
        case 0:
            # set line here
            plusMinus(bet, choice, line)
        case 1:
            # set line here
            moneyLine(bet, choice, line)
        case 2:
            # set line here
            overUnder(bet, choice, line)
        case 3:
            # set line here
            skilledProp1(bet, choice, line)
        case 4:
            # set line here
            skilledProp2(bet, choice, line)
        case 5:
            # set line here
            unskilledProp1(bet, choice, line)
        case 6:
            # set line here
            unskilledProp2(bet, choice, line)
        case 7:
            # set line here
            exoticProp1(bet, choice, line)
        case 8:
            # set line here
            exoticProp2(bet, choice, line)
        case _:
            print("No bet selected")


def main():
    # 10% vig taken
    vig = 0.1
    money = 1000
    min_bet = 50
    bet_types = ['plus_minus', 'money_line', 'over_under', 'skilled_prop_1', 'skilled_prop_2', 'unskilled_prop_1', 'unskilled_prop_2', 'exotic_prop_1', 'exotic_prop_2']
    print('Choose a bet type (number)')
    for i in range(len(bet_types)):
        print('{}\t{}'.format(i, bet_types[i]))


if __name__ == '__main__':
    main()
