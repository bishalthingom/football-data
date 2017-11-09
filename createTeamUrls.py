
teams_file = open('whoscored_teams.csv','r')
teams = teams_file.readlines()

output = open('team_urls.txt','a+')

for team in teams:
    team_data = team.split(',')
    'https://www.whoscored.com/Teams/15/Archive/England-Chelsea'
    url = 'https://www.whoscored.com/Teams/' + team_data[0] + '/Archive/' + team_data[2] + '-' + team_data[1]
    output.write(url + '\n')
