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

# Change to true to fetch new data
GET_NEW_DATA = False
GET_MODS = False

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
    line = int(scores[0] + scores[1])
    return line - 0.5


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
        winner: int(pm_scores[winner] * w_mod * 10),
        loser: int(pm_scores[loser] * w_mod * 10)
    }
    ml = pd.Series(m_lines).to_string()
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
    return lines


# line determined by combined predicted score
def overUnderBet(bet, choice, line):
    # jake
    pass


# money line payouts determined by ratio of score difference times a constant
def moneyLineBet(bet, choice, line):
    # jakes
    pass


# line determined by difference in predicted scores (i.e. prediction for Duke vs Villanova is 75-72, Duke would have -3, Villa would get +3)
def plusMinusBet(bet, choice, lines):
    # jake
    pass


#  Will (top scoring player) score more than (average + 1)?
def skilledProp1Bet(bet, choice, line):
    # nick
    pass


# Will there be > (avg) turnovers?
def skilledProp2Bet(bet, choice, line):
    # nick
    pass


# Will the game go to overtime? (chance determined by history of overtime games in NCAA tourney)
# take each NCAA finals game (by date, using Boxscore), check if it went to overtime, create line based on ratio
def unskilledProp1Bet(bet, choice, line):
    # myles
    pass


# How many fouls will there be in the first half? (over/under avg fouls per game/2)
def unskilledProp2Bet(bet, choice, line):
    # myles
    pass


# makes an exotic prop 1 bet
def exoticProp1Bet(bet, choice, line):
    pass


# makes an exotic prop 1 bet
def exoticProp2Bet(bet, choice, line):
    pass


# outputs the betting info in sportsbook format
def displayData():
    pass


def makeBet(b_type, bet, choice, scores):
    match b_type:
        case 0:
            # set line here
            lines = scores
            plusMinusBet(bet, choice, lines)
        case 1:
            # set line here
            moneyLineBet(bet, choice, line)
        case 2:
            lines = o_u_line(scores)
            overUnderBet(bet, choice, lines)
        case 3:
            # set line here
            skilledProp1Bet(bet, choice, line)
        case 4:
            # set line here
            skilledProp2Bet(bet, choice, line)
        case 5:
            # set line here
            unskilledProp1Bet(bet, choice, line)
        case 6:
            # set line here
            unskilledProp2Bet(bet, choice, line)
        case 7:
            # set line here
            exoticProp1Bet(bet, choice, line)
        case 8:
            # set line here
            exoticProp2Bet(bet, choice, line)
        case _:
            print("No bet selected")


def main():
    # 10% vig taken
    vig = 0.1
    # these are the plus_minus lines
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
    print(display_df)
    print('Please select your bet (#):')
    user_bet_type = int(input())
    print('Please enter amount (ex. $500 would be entered as 500)')
    user_bet_amount = int(input())
    print('Please enter the team: {} or {}'.format(TEAM_1, TEAM_2))
    user_team = str(input())
    makeBet(user_bet_type, user_bet_amount, user_team, plus_minus)


if __name__ == '__main__':
    main()
