"""
Name: Jake Bova
File: sportsbook_1.py
Date: 03/30/22
"""
from datetime import datetime

import math
import numpy
import pandas as pd
from sportsipy.ncaab.roster import Player
from sportsipy.ncaab.teams import Team
from sportsipy.ncaab.boxscore import Boxscore
from sportsipy.ncaab.boxscore import Boxscores

pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.options.display.max_colwidth = 200

TEAM_1 = 'KANSAS'
TEAM_2 = 'NORTH-CAROLINA'

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
            'TEAM': ['KANSAS', 'NORTH-CAROLINA'],
            'MOD': [Team('KANSAS').strength_of_schedule,
                    Team('NORTH-CAROLINA').strength_of_schedule]
        }
    )

    TEAM_MODS.to_csv('Data/team_mods.csv')
else:
    TEAM_MODS = {
        'KANSAS': 11.21,
        'NORTH-CAROLINA': 8.53
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
        "Choice": ["TEAM", "TEAM", "TEAM", "TEAM", "TEAM", "TEAM", "TEAM", "TEAM", "TEAM"],
        "Possible Winnings": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Description": ["FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME", "FIXME"],
        "Sportsbook Cut": [0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
)

BETTING_INFO.to_csv('Data/betting_info.csv')


def updateBettingInfo(bet_type, bet, choice):
    BETTING_INFO.at[bet_type, 'Bet Amount'] = bet
    BETTING_INFO.at[bet_type, 'Choice'] = choice


def getTourneyGames():
    # Pulls all games between and including March 17, 2022 to April 3, 2022
    games = Boxscores(datetime(2022, 3, 17), datetime(2022, 4, 3))
    dates = ['3-17-2022', '3-18-2022', '3-19-2022', '3-20-2022', '3-21-2022', '3-22-2022', '3-23-2022', '3-24-2022',
             '3-25-2022', '3-26-2022', '3-27-2022', '3-28-2022', '3-29-2022', '3-30-2022', '3-31-2022', '4-1-2022',
             '4-2-2022', '4-3-2022', ]
    game_data = []
    for date in dates:
        for game in games.games[date]:
            if game['top_25']:
                g_box = Boxscore(game['boxscore'])
                game_data.append(g_box)
    return game_data


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
    scores = {
        TEAM_1: t1_score,
        TEAM_2: t2_score
    }
    return scores


def o_u_line(scores):
    line = int(scores[TEAM_1] + scores[TEAM_2]) - 0.5
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
        winner: round((lo - hi) - 0.5, 1),
        loser: round((hi - lo) + 0.5, 1)
    }
    BETTING_INFO.at[0, 'Description'] = lines
    return lines


def sp1_line():
    ochai_agbaji = Player('ochai-agbaji-1')
    player_data = ochai_agbaji.dataframe

    total_points = player_data.points['2021-22']
    total_games = player_data.games_played['2021-22']
    points_per_game = total_points / total_games
    line = math.ceil(points_per_game)
    BETTING_INFO.at[3, 'Description'] = line


def sp2_line():
    # K_team = Team("KANSAS")
    # N_team = Team("NORTH-CAROLINA")
    #
    # total_gamesK = K_team.games_played
    # total_gamesN = N_team.games_played
    #
    # total_turnoversK = K_team.turnovers
    # total_turnoversN = N_team.turnovers
    #
    #
    # avg_turnovers = ((total_turnoversK / total_gamesK) + (total_turnoversN / total_gamesN)) / 2
    line = 12  # math.ceil(avg_turnovers)
    BETTING_INFO.at[4, 'Description'] = line


def usp1_line():
    chance = 8 / 80  # 8 overtime finals in 80 tournaments, 10% chance, 900 odds = 10%, -900 = 90% for no overtime
    line = 900
    BETTING_INFO.at[5, 'Description'] = line

    # games = getTourneyGames()
    # for game in games:
    #    if game.overtimes < 0:
    #        ot += 1
    #    else:
    #        reg_finish += 1
    # line = reg_finish/ot
    # BETTING_INFO.at[5, 'Description'] = line


def usp2_line():
    # fouls = 0
    # games = getTourneyGames()
    # for game in games:
    #     fouls += game.away_personal_fouls + game.home_personal_fouls
    line = 16  # round((fouls / len(games)) / 2)
    BETTING_INFO.at[6, 'Description'] = line


def ex2_line():
    pass


# make a plus minus bet
def plusMinusBet(bet, choice, b_type):
    winnings = 0.9 * bet
    line = BETTING_INFO.at[b_type, 'Description']
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)
    BETTING_INFO.at[b_type, 'Sportsbook Cut'] = bet * 0.1
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
    winnings = 0.9 * bet
    line = BETTING_INFO.at[b_type, 'Description']
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)
    BETTING_INFO.at[b_type, 'Sportsbook Cut'] = bet * 0.1


#  Will (top scoring player) score more than (average)?
def skilledProp1Bet(bet, choice, b_type):
    winnings = 0.9 * bet
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)
    BETTING_INFO.at[b_type, 'Sportsbook Cut'] = bet * 0.1


# Will there be > (avg) turnovers?
def skilledProp2Bet(bet, choice, b_type):
    winnings = 0.9 * bet
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)
    BETTING_INFO.at[b_type, 'Sportsbook Cut'] = bet * 0.1


# Will the game go to overtime? (chance determined by history of overtime games in NCAA tourney)
# take each NCAA finals game (by date, using Boxscore), check if it went to overtime, create line based on ratio
def unskilledProp1Bet(bet, choice, b_type):
    # myles
    line = BETTING_INFO.at[b_type, 'Description']
    if choice == 'yes':
        winnings = ((abs(line) / 100) * bet)
    else:
        winnings = ((100 / abs(line)) * bet)
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)

    # games = getTourneyGames()
    # line = BETTING_INFO.at[5, 'Description']
    # ot = False
    # championship = Boxscores(datetime.today())
    # if championship.overtimes > 0:
    #    ot = True
    # if ot:
    #    if choice == 'yes':
    #        winnings = (line * bet) / 100
    #    else:
    #        winnings = (100 * bet) / line
    # else:
    #    if choice == 'yes':
    #        winnings = (100 * bet) / line
    #    else:
    #        winnings = (line * bet) / 100
    # BETTING_INFO.at[b_type, 'Possible Winnings'] = winnings


# How many fouls will there be in the first half? (over/under avg fouls per game/2)
def unskilledProp2Bet(bet, choice, b_type):
    # myles
    winnings = 0.9 * bet
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)
    BETTING_INFO.at[b_type, 'Sportsbook Cut'] = bet * 0.1


# makes an exotic prop 1 bet
# will it rain on gameday? (night)
def exoticProp1Bet(bet, choice, b_type):
    pass


# makes an exotic prop 1 bet
# will the final combined score be odd or even?
def exoticProp2Bet(bet, choice, b_type):
    winnings = 0.9 * bet
    BETTING_INFO.at[b_type, 'Possible Winnings'] = round(winnings, 2)
    BETTING_INFO.at[b_type, 'Sportsbook Cut'] = bet * 0.1
    pass


# import betting info csv and check if each choice is winner or not, keep winnings if winner/choice is correct, else reset winnings cell before saving csv
def payoutBets():
    pass


def makeBet(b_type, bet, choice):
    match b_type:
        case 0:
            updateBettingInfo(b_type, bet, choice)
            plusMinusBet(bet, choice, b_type)
        case 1:
            updateBettingInfo(b_type, bet, choice)
            moneyLineBet(bet, choice, b_type)
        case 2:
            updateBettingInfo(b_type, bet, choice)
            overUnderBet(bet, choice, b_type)
        case 3:
            updateBettingInfo(b_type, bet, choice)
            skilledProp1Bet(bet, choice, b_type)
        case 4:
            updateBettingInfo(b_type, bet, choice)
            skilledProp2Bet(bet, choice, b_type)
        case 5:
            updateBettingInfo(b_type, bet, choice)
            unskilledProp1Bet(bet, choice, b_type)
        case 6:
            updateBettingInfo(b_type, bet, choice)
            unskilledProp2Bet(bet, choice, b_type)
        case 7:
            exoticProp1Bet(bet, choice, b_type)
        case 8:
            updateBettingInfo(b_type, bet, choice)
            exoticProp2Bet(bet, choice, b_type)
        case _:
            print("No bet selected")


def generateLines():
    sp1_line()
    sp2_line()
    usp1_line()
    usp2_line()
    ex2_line()


def main():
    scores = predictScore(TEAM_1, TEAM_2)
    plus_minus = pd.Series(p_m_line(scores)).to_string().strip() + '(-110)'
    over_under = "over {} (-110)".format(o_u_line(scores))
    money_line = m_line(p_m_line(scores))
    generateLines()
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
                "will Agbaji score over/under {} points? ({})".format(BETTING_INFO.at[3, 'Description'], "-110"),
                "will there be over/under {} turnovers in the first half? ({})".format(
                    BETTING_INFO.at[4, 'Description'], "-110"),
                "will the game go to overtime? yes/no odds ({},{})".format(BETTING_INFO.at[5, 'Description'],
                                                                           -BETTING_INFO.at[5, 'Description']),
                "will there be over/under {} fouls in the first half? ({})".format(BETTING_INFO.at[6, 'Description'],
                                                                                   "-110"),
                "",
                "will the final combined score be odd or even? (odd/even) (-110)",
            ]
        }
    )
    user_bet_type = 99
    while user_bet_type != -1:
        print(display_df)
        print('Please select your bet (#) (-1 to quit):')
        user_bet_type = int(input())
        if user_bet_type == -1:
            break
        print('Please enter amount (ex. $500 would be entered as 500)')
        user_bet_amount = int(input())
        if user_bet_type == 0 or user_bet_type == 1:
            print('Please enter the team: {} or {}'.format(TEAM_1, TEAM_2))
            user_choice = str(input())
        if user_bet_type == 2 or user_bet_type == 3 or user_bet_type == 4 or user_bet_type == 6:
            print("Over or under?")
            user_choice = str(input())
        if user_bet_type == 5:
            print("yes or no?")
            user_choice = str(input())
        if user_bet_type == 8:
            print("odd or even?")
            user_choice = str(input())
        makeBet(user_bet_type, user_bet_amount, user_choice)
        BETTING_INFO.to_csv('Data/betting_info.csv')
        print(BETTING_INFO)


if __name__ == '__main__':
    main()
