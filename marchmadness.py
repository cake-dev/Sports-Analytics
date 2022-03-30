"""
Name: Jake Bova
File: marchmadness.py
Date: 03/16/22
"""
import math

import pandas as pd
from sportsipy.ncaab.teams import Team

pd.set_option("display.max_rows", None, "display.max_columns", None)


def teamRating(srs, sos, efg, off, wp, g):
    """
    teamRating uses several factors to calculate a team 'rating'.  A higher rating indicates a better team / a team that has played stronger opponents.
    The difference in team ratings is used to add additional score to the better team in the predictScore calculation.
    """
    # take log base 2 of srs and add to score (to prevent too large of rating  & add negative value for low ( < 1) SRS teams)
    if srs > 0:
        mod_srs = math.log(srs, 2)
    else:
        mod_srs = -10
    score = mod_srs + sos * 2 + (efg * off) + (wp * g)
    return score


def predictScore(t1_poss, t2_poss, t1_off, t2_off, t1_def, t2_def, t1_rating, t2_rating):
    """
    predictScore uses the score prediction method we used in class, plus another method used to calculate effeciency and possessions
    take the average off the effeciencies and tempo to get the adj_off_eff avg and adj_poss avg
    """
    d1_avg_poss = 67.3
    d1_avg_off = 103.8
    adj_poss_1 = (t1_poss * t2_poss) / d1_avg_poss
    adj_poss_2 = (t1_poss - d1_avg_poss) + (t2_poss - d1_avg_poss) + d1_avg_poss
    adj_poss = (adj_poss_1 + adj_poss_2) / 2
    adj_off_1 = (t1_off * t2_def) / d1_avg_off
    adj_off_2 = (t2_off * t1_def) / d1_avg_off
    adj_off_1_2 = (t1_off - d1_avg_off + t2_def - d1_avg_off) + d1_avg_off
    adj_off_2_2 = (t1_off - d1_avg_off + t2_def - d1_avg_off) + d1_avg_off
    adj_off_avg_1 = (adj_off_1 + adj_off_1_2) / 2
    adj_off_avg_2 = (adj_off_2 + adj_off_2_2) / 2
    t1_score = (adj_off_avg_1 / 100) * adj_poss
    t2_score = (adj_off_avg_2 / 100) * adj_poss
    # add rating modifier for teams with better opponents
    rating_diff = abs(t1_rating - t2_rating) * 0.25
    if t1_rating > t2_rating:
        t1_score += rating_diff
    elif t2_rating > t1_rating:
        t2_score += rating_diff
    return [t1_score, t2_score]


def poss(fga, fta, orb, tov):
    return fga + (0.475 * fta) - orb + tov


def effeciency(pts, pos):
    return (100 / pos) * pts


def getWP(wins, losses, h_win, a_win, h_loss, a_loss, c_wins, c_loss):
    # using old RPI rating system caluclation for win percentage (different weights for home/away)
    hw = 0.6 * h_win
    aw = 1.4 * a_win
    hl = 1.4 * h_loss
    al = 0.6 * a_loss
    adj_win_p = (hw + aw) / (hl + al + hw + aw)
    # take the average of the weighted win percentage and conference win percentage for a more realistic winrate
    conf_win_p = c_wins / (c_wins + c_loss)
    wp = ((conf_win_p + adj_win_p) / 2)

    return wp


def getTeamsInfo(team1, team2):
    """
    getTeamsInfo uses the sportsipy API to fetch the Team info for the provided teams
    """
    t1 = Team(team1)
    wp1 = getWP(t1.wins, t1.losses, t1.home_wins, t1.away_wins, t1.home_losses, t1.away_losses, t1.conference_wins,
                t1.conference_losses)
    t2 = Team(team2)
    wp2 = getWP(t2.wins, t2.losses, t2.home_wins, t2.away_wins, t2.home_losses, t2.away_losses, t2.conference_wins,
                t2.conference_losses)
    t1_games = t1.games_played
    t2_games = t2.games_played

    data = {
        'Team': [team1, team2],
        'SRS': [t1.simple_rating_system, t2.simple_rating_system],
        'SOS': [t1.strength_of_schedule, t2.strength_of_schedule],
        'Win%': [wp1, wp2],
        'FGA/g': [t1.field_goal_attempts / t1_games, t2.field_goal_attempts / t2_games],
        'FTA/g': [t1.free_throw_attempts / t1_games, t2.free_throw_attempts / t2_games],
        'ORB/g': [t1.offensive_rebounds / t1_games, t2.offensive_rebounds / t2_games],
        'TOV/g': [t1.turnovers / t1_games, t2.turnovers / t2_games],
        'eFG%': [t1.effective_field_goal_percentage, t2.effective_field_goal_percentage],
        'Pts/g': [t1.points / t1_games, t2.points / t2_games],
        'o_FGA/g': [t1.opp_field_goal_attempts / t1_games, t2.opp_field_goal_attempts / t2_games],
        'o_FTA/g': [t1.opp_free_throw_attempts / t1_games, t2.opp_free_throw_attempts / t2_games],
        'o_ORB/g': [t1.opp_offensive_rebounds / t1_games, t2.opp_offensive_rebounds / t2_games],
        'o_TOV/g': [t1.opp_turnovers / t1_games, t2.opp_turnovers / t2_games],
        'o_eFG%': [t1.opp_effective_field_goal_percentage, t2.opp_effective_field_goal_percentage],
        'o_Pts/g': [t1.opp_points / t1_games, t2.opp_points / t2_games]
    }

    info = pd.DataFrame(data)
    info['Poss'] = poss(info['FGA/g'], info['FTA/g'], info['ORB/g'], info['TOV/g'])
    info['o_Poss'] = poss(info['o_FGA/g'], info['o_FTA/g'], info['o_ORB/g'], info['o_TOV/g'])
    info['Off. Eff'] = effeciency(info['Pts/g'], info['Poss'])
    info['Def. Eff'] = effeciency(info['o_Pts/g'], info['o_Poss'])
    score1 = teamRating(info.at[0, 'SRS'], info.at[0, 'SOS'], info.at[0, 'eFG%'], info.at[0, 'Off. Eff'],
                        info.at[0, 'Win%'], t1_games)
    score2 = teamRating(info.at[1, 'SRS'], info.at[1, 'SOS'], info.at[1, 'eFG%'], info.at[1, 'Off. Eff'],
                        info.at[1, 'Win%'], t2_games)
    info['RATING'] = [score1, score2]
    scores = predictScore(info.at[0, 'Poss'], info.at[1, 'Poss'], info.at[0, 'Off. Eff'], info.at[1, 'Off. Eff'],
                          info.at[0, 'Def. Eff'], info.at[1, 'Def. Eff'], info.at[0, 'RATING'], info.at[1, 'RATING'])
    info['PREDICTED SCORE'] = scores

    return info


def getInput():
    print("Team 1: ", end='')
    team1 = input().upper()
    print("Team 2: ", end='')
    team2 = input().upper()
    team_info = getTeamsInfo(team1, team2)
    print(team_info)


def main():
    getInput()


if __name__ == "__main__":
    main()
