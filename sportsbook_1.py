"""
Name: Jake Bova
File: sportsbook_1.py
Date: 03/30/22
"""
from datetime import datetime

import numpy
import pandas as pd
from sportsipy.ncaab.teams import Team
from sportsipy.ncaab.boxscore import Boxscore
from sportsipy.ncaab.boxscore import Boxscores

pd.set_option("display.max_rows", None, "display.max_columns", None)

TEAM_1 = 'NORTH-CAROLINA'
TEAM_2 = 'KANSAS'

# change these to the winning teams after the game, will be used to check against user choice to give out winnings
WINNER = TEAM_1
LOSER = TEAM_2

# Change to true to fetch new data
GET_NEW_DATA = False
GET_MODS = False

# TEAM_MODS used to adjust moneyline bet
if GET_MODS:
    TEAM_MODS = pd.DataFrame(
        {
            'TEAM': ['DUKE', 'KANSAS', 'NORTH-CAROLINA', 'VILLANOVA'],
            'MOD': [Team('DUKE').strength_of_schedule, Team('KANSAS').strength_of_schedule,
                    Team('NORTH-CAROLINA').strength_of_schedule, Team('VILLANOVA').strength_of_schedule, ]
        }
    )

    TEAM_MODS.to_csv('Data/team_mods.csv')
else:
    TEAM_MODS = {
        'DUKE': 7.04,
        'KANSAS': 10.98,
        'NORTH-CAROLINA': 8.25,
        'VILLANOVA': 10.01
    }

# use this DF to add betting info to write to CSV later
BETTING_INFO = pd.DataFrame(
    {
        "Bet Type": [
            "plus and minus",
            "money line",
            "over/under",
            "skilled prop 1",
            "skilled prop 2",
            "unskilled prop 1",
            "unskilled prop 2",
            "exotic prop 1",
            "exotic prop 2"
        ],
        "Bet Amount": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Choice": [TEAM_1, TEAM_1, TEAM_1, TEAM_1, TEAM_1, TEAM_1, TEAM_1, TEAM_1, TEAM_1],
        "Possible Winnings": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Description": ["FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME"]
    }
)


def updateBettingInfo(bet_type, bet, choice):
    BETTING_INFO.at[bet_type, 'Bet Amount'] = bet
    BETTING_INFO.at[bet_type, 'Choice'] = choice


def getGamesInRange():
    # Pulls all games between and including March 15, 2022 to April 3, 2022
    games = Boxscores(datetime(2022, 3, 15), datetime(2022, 4, 3))
    dates = ['3-15-2022', '3-16-2022', '3-17-2022', '3-18-2022', '3-19-2022', '3-20-2022', '3-21-2022', '3-22-2022', '3-23-2022', '3-24-2022', '3-25-2022', '3-26-2022', '3-27-2022', '3-28-2022', '3-29-2022', '3-30-2022', '3-31-2022', '4-1-2022', '4-2-2022', '4-3-2022', ]
    game_data = []
    for date in dates:
        for game in games.games[date]:
            g_box = Boxscore(game['boxscore'])
            print(g_box.home_turnovers + g_box.away_turnovers)
            if g_box.home_turnovers + g_box.away_turnovers == 22:
                print('here')
            game_data.append(g_box)
    print(game_data)


# returns the values of predicted scores for each team, can be used for plusMinus, moneyLine (for predicted winner), as well as combined for overUnder bet
# use tournament games from current NCAA tourney + conf tourney
def predictScore(t1, t2):
    # jake
    d1_avg_poss = 67.3
    d1_avg_off = 103.8
    filename1 = 'Data/' + t1 + '_schedule.csv'
    filename2 = 'Data/' + t2 + '_schedule.csv'
    if GET_NEW_DATA:
        team1 = Team(t1)
        team2 = Team(t2)
        schedule1 = team1.schedule
        schedule2 = team2.schedule
        sc1_df = schedule1.dataframe
        sc2_df = schedule2.dataframe
        sc1_df.to_csv(filename1)
        sc2_df.to_csv(filename2)
    if not GET_NEW_DATA:
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
    if GET_NEW_DATA:
        for date in t1_game_dates:
            filename = 'Data/' + str(date) + '_game_data.csv'
            game = Boxscore(date)
            game_df = game.dataframe
            game_df.to_csv(filename)
        for date in t2_game_dates:
            filename = 'Data/' + str(date) + '_game_data.csv'
            game = Boxscore(date)
            game_df = game.dataframe
            game_df.to_csv(filename)
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
    line = int(scores[0] + scores[1]) - 0.5
    BETTING_INFO.at[2, 'Description'] = line
    return line


def m_line(pm_scores):
    t1_mod = TEAM_MODS[TEAM_1]
    t2_mod = TEAM_MODS[TEAM_2]
    if pm_scores.get(TEAM_1) > pm_scores.get(TEAM_2):
        winner = TEAM_1
        loser = TEAM_2
    else:
        winner = TEAM_2
        loser = TEAM_1
    if t1_mod > t2_mod:
        w_mod = t1_mod - t2_mod
    else:
        w_mod = t2_mod - t1_mod

    m_lines = {
        winner: int(pm_scores[winner] * w_mod * 5),
        loser: int(pm_scores[loser] * w_mod * 5)
    }
    ml = pd.Series(m_lines).to_string()
    BETTING_INFO.at[1, 'Description'] = m_lines
    return ml


def p_m_line(t_scores):
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
        winner: (lo - hi) - 0.5,
        loser: (hi - lo) + 0.5
    }
    BETTING_INFO.at[0, 'Description'] = lines
    return lines


# make a plus minus bet
def plusMinusBet(bet, choice):
    # jake
    pass


# make money line bet
def moneyLineBet(bet, choice, b_type):
    # jake
    line = BETTING_INFO.at[b_type, 'Description']
    if line[choice] < 0:
        winnings = ((100 / abs(line[choice])) * bet)
    else:
        winnings = ((abs(line[choice]) / 100) * bet)
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)


# make over under bet
def overUnderBet(bet, choice, b_type):
    # jake
    pass


#  Will (top scoring player) score more than (average + 1)?
def skilledProp1Bet(bet, choice):
    # nick
    pass


# Will there be > (avg) turnovers?
def skilledProp2Bet(bet, choice):
    # nick
    pass


# Will the game go to overtime? (chance determined by history of overtime games in NCAA tourney)
# take each NCAA finals game (by date, using Boxscore), check if it went to overtime, create line based on ratio
def unskilledProp1Bet(bet, choice):
    # myles
    pass


# How many fouls will there be in the first half? (over/under avg fouls per game/2)
def unskilledProp2Bet(bet, choice):
    # myles
    pass


# makes an exotic prop 1 bet
# which team will score first?
def exoticProp1Bet(bet, choice):
    pass


# makes an exotic prop 1 bet
# will the final combined score be odd or even?
def exoticProp2Bet(bet, choice):
    pass


# outputs the betting info in sportsbook format
# use the BETTING_INFO df to do this
def displayData():
    pass


def makeBet(b_type, bet, choice):
    match b_type:
        case 0:
            updateBettingInfo(b_type, bet, choice)
            plusMinusBet(bet, choice)
        case 1:
            updateBettingInfo(b_type, bet, choice)
            moneyLineBet(bet, choice, b_type)
        case 2:
            updateBettingInfo(b_type, bet, choice)
            overUnderBet(bet, choice, b_type)
        case 3:
            # set line here
            skilledProp1Bet(bet, choice)
        case 4:
            # set line here
            skilledProp2Bet(bet, choice)
        case 5:
            # set line here
            unskilledProp1Bet(bet, choice)
        case 6:
            # set line here
            unskilledProp2Bet(bet, choice)
        case 7:
            # set line here
            exoticProp1Bet(bet, choice)
        case 8:
            # set line here
            exoticProp2Bet(bet, choice)
        case _:
            print("No bet selected")


def main():
    # 10% vig taken
    vig = 0.1
    getGamesInRange()
    scores = predictScore(TEAM_1, TEAM_2)
    t_scores = {
        TEAM_1: int(scores[0]),
        TEAM_2: int(scores[1])
    }
    plus_minus = pd.Series(p_m_line(t_scores)).to_string().strip()
    over_under = "under {}".format(o_u_line(scores))
    money_line = m_line(p_m_line(t_scores))
    display_df = pd.DataFrame(
        {
            "Bet Type": [
                "plus and minus",
                "money line",
                "over/under",
                "skilled prop 1",
                "skilled prop 2",
                "unskilled prop 1",
                "unskilled prop 2",
                "exotic prop 1",
                "exotic prop 2",
            ],
            "Details": [
                plus_minus,
                money_line,
                over_under,
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        }
    )
    user_bet_type = 99
    while user_bet_type != -1:
        print(display_df)
        print('Please select your bet (#) (-1 to quit):')
        user_bet_type = int(input())
        print('Please enter amount (ex. $500 would be entered as 500)')
        user_bet_amount = int(input())
        if user_bet_type == 2:
            print("Over or under?")
            user_choice = str(input())
        else:
            print('Please enter the team: {} or {}'.format(TEAM_1, TEAM_2))
            user_choice = str(input())
        makeBet(user_bet_type, user_bet_amount, user_choice)
        print(BETTING_INFO)


if __name__ == '__main__':
    main()
