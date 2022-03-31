"""
Name: Jake Bova
File: sportsbook_1.py
Date: 03/30/22
"""
import numpy
import pandas as pd
from sportsipy.ncaab.teams import Team
from sportsipy.ncaab.boxscore import Boxscore


# TEAM_1 = 'NORTH-CAROLINA'
# TEAM_2 = 'VILLANOVA'
TEAM_1 = 'DUKE'
TEAM_2 = 'KANSAS'


# returns the values of predicted scores for each team, can be used for plusMinus, moneyLine (for predicted winner), as well as combined for overUnder bet
# use tournament games from current NCAA tourney + conf tourney
def predictScore(t1, t2):
    # jake
    d1_avg_poss = 67.3
    d1_avg_off = 103.8
    filename1 = 'Data/' + t1 + '_schedule.csv'
    filename2 = 'Data/' + t2 + '_schedule.csv'
    # uncomment and run the following code to pull new data (if updated)
    # team1 = Team(t1)
    # team2 = Team(t2)
    # schedule1 = team1.schedule
    # schedule2 = team2.schedule
    # sc1_df = schedule1.dataframe
    # sc2_df = schedule2.dataframe
    # sc1_df.to_csv(filename1)
    # sc2_df.to_csv(filename2)
    sc1_df = pd.read_csv(filename1)
    sc2_df = pd.read_csv(filename2)
    sc1_adj = sc1_df[sc1_df.type != 'Reg']
    sc2_adj = sc2_df[sc2_df.type != 'Reg']
    t1_game_dates = []
    t2_game_dates = []
    t1_stats = {
        'pace': [],
        'off_eff': [],
        'def_eff': []
    }
    t2_stats = {
        'pace': [],
        'off_eff': [],
        'def_eff': []
    }

    t1_avg_stats = {
        'avg_pace': 0,
        'avg_off_eff': 0,
        'avg_def_eff': 0
    }
    t2_avg_stats = {
        'avg_pace': 0,
        'avg_off_eff': 0,
        'avg_def_eff': 0
    }
    for date in sc1_adj.boxscore_index:
        t1_game_dates.append(date)
    for date in sc2_adj.boxscore_index:
        t2_game_dates.append(date)
    t1_game_dates.pop()
    t2_game_dates.pop()
    # uncomment and run the following code to pull new data (if updated)
    # for date in t1_game_dates:
    #     filename = 'Data/' + str(date) + '_game_data.csv'
    #     game = Boxscore(date)
    #     game_df = game.dataframe
    #     game_df.to_csv(filename)
    # for date in t2_game_dates:
    #     filename = 'Data/' + str(date) + '_game_data.csv'
    #     game = Boxscore(date)
    #     game_df = game.dataframe
    #     game_df.to_csv(filename)
    for date in t1_game_dates:
        filename = 'Data/' + str(date) + '_game_data.csv'
        game = pd.read_csv(filename)
        t1_stats['pace'].append(game.pace)
        t1_stats['off_eff'].append(game.home_offensive_rating)
        t1_stats['def_eff'].append(game.home_defensive_rating)
    # review this after the next final four games are played (to see if game stats are updated and not None type)
    t1_stats['pace'].pop()
    t1_stats['off_eff'].pop()
    t1_stats['def_eff'].pop()
    for date in t2_game_dates:
        filename = 'Data/' + str(date) + '_game_data.csv'
        game = pd.read_csv(filename)
        t2_stats['pace'].append(game.pace)
        t2_stats['off_eff'].append(game.home_offensive_rating)
        t2_stats['def_eff'].append(game.home_defensive_rating)
    t2_stats['pace'].pop()
    t2_stats['off_eff'].pop()
    t2_stats['def_eff'].pop()
    t1_avg_stats['avg_pace'] = numpy.mean(t1_stats['pace'])
    t1_avg_stats['avg_off_eff'] = numpy.mean(t1_stats['off_eff'])
    t1_avg_stats['avg_def_eff'] = numpy.mean(t1_stats['def_eff'])
    t2_avg_stats['avg_pace'] = numpy.mean(t2_stats['pace'])
    t2_avg_stats['avg_off_eff'] = numpy.mean(t2_stats['off_eff'])
    t2_avg_stats['avg_def_eff'] = numpy.mean(t2_stats['def_eff'])
    adj_poss_1 = (t1_avg_stats['avg_pace'] * t2_avg_stats['avg_pace']) / d1_avg_poss
    adj_poss_2 = (t1_avg_stats['avg_pace'] - d1_avg_poss) + (t2_avg_stats['avg_pace'] - d1_avg_poss) + d1_avg_poss
    adj_off_1_t1 = (t1_avg_stats['avg_off_eff'] * t2_avg_stats['avg_def_eff']) / d1_avg_off
    adj_off_1_t2 = (t2_avg_stats['avg_off_eff'] * t1_avg_stats['avg_def_eff']) / d1_avg_off
    adj_off_2_t1 = (t1_avg_stats['avg_off_eff'] - d1_avg_off + t2_avg_stats['avg_def_eff'] - d1_avg_off) + d1_avg_off
    adj_off_2_t2 = (t2_avg_stats['avg_off_eff'] - d1_avg_off + t1_avg_stats['avg_def_eff'] - d1_avg_off) + d1_avg_off
    adj_poss = (adj_poss_1 + adj_poss_2) / 2
    adj_off_t1 = (adj_off_1_t1 + adj_off_2_t1) / 2
    adj_off_t2 = (adj_off_1_t2 + adj_off_2_t2) / 2
    t1_score = (adj_off_t1 / 100) * adj_poss
    t2_score = (adj_off_t2 / 100) * adj_poss
    return [t1_score, t2_score]


def o_u_line(scores):
    line = int(scores[0] + scores[1])
    return line + 1

def m_line(pm_scores):
    m_lines = {
        TEAM_1: pm_scores[TEAM_1],
        TEAM_2: pm_scores[TEAM_2]
    }

def p_m_line(t_scores):
    hi = 0
    lo = 0
    winner = ''
    loser = ''
    if t_scores.get(TEAM_1) > t_scores.get(TEAM_2):
        hi = t_scores.get(TEAM_1)
        lo = t_scores.get(TEAM_2)
        winner = TEAM_1
        loser = TEAM_2
    else:
        hi = t_scores.get(TEAM_2)
        lo = t_scores.get(TEAM_1)
        winner = TEAM_2
        loser = TEAM_1
    lines = {
        winner: lo - hi,
        loser: hi - lo
    }
    return lines


# line determined by combined predicted score
def overUnder(bet, choice, line):
    # jake
    pass


# money line payouts determined by ratio of score difference times a constant
def moneyLine(bet, choice, line):
    # jake
    pass


# line determined by difference in predicted scores (i.e. prediction for Duke vs Villanova is 75-72, Duke would have -3, Villa would get +3)
def plusMinus(bet, choice, line):
    # jake
    pass


#  Will (top scoring player) score more than (average + 1)?
def skilledProp1(bet, choice, line):
    # nick
    pass


# Will there be > (avg) turnovers?
def skilledProp2(bet, choice, line):
    # nick
    pass


# Will the game go to overtime? (chance determined by history of overtime games in NCAA tourney)
# take each NCAA finals game (by date, using Boxscore), check if it went to overtime, create line based on ratio
def unskilledProp1(bet, choice, line):
    # myles
    pass


# How many fouls will there be in the first half? (over/under avg fouls per game/2)
def unskilledProp2(bet, choice, line):
    # myles
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
    scores = predictScore(TEAM_1, TEAM_2)
    t_scores = {
        TEAM_1: int(scores[0]),
        TEAM_2: int(scores[1])
    }
    plusminus = p_m_line(t_scores)
    # these are the plus_minus lines
    pmdf = pd.Series(plusminus)
    print(pmdf.to_string())


if __name__ == '__main__':
    main()
