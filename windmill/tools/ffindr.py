from windmill.tools.models import Team, Tournament
import csv
import itertools
import logging

def isin(division,team_name):
    # Get an instance of a logger
    logger = logging.getLogger('windmill.tools')

    logger.info('checking team {0}'.format(team_name))
    # returns a Boolean value whether the team with name team_name is accepted to division
    payinfo=csv.reader(open('windmill/regdata/'+division+'_in.csv'))
    for team in payinfo:
        if team[0]==str(team_name):
            if team[1]=='Y':
                logger.info('is in')
                return True
            else:
                logger.info('is not in')
                return False
            break
    
    logger.error('team {0} not found'.format(team_name))
    return False

def ffindr_import():
    # import teams from ffindr into local model
    
#    urls={}
#    urls['open': 'https://docs.google.com/spreadsheet/pub?key=0Ana-uXOgDVsrdEthclk3VDRwOE5uVmp4MjdRc0p2VkE&single=true&gid=2&range=B2:F62&output=csv',
#         'women': 'https://docs.google.com/spreadsheet/pub?key=0Ana-uXOgDVsrdEthclk3VDRwOE5uVmp4MjdRc0p2VkE&single=true&gid=1&range=B2:F20&output=csv',
#         'mixed': 'https://docs.google.com/spreadsheet/pub?key=0Ana-uXOgDVsrdEthclk3VDRwOE5uVmp4MjdRc0p2VkE&single=true&gid=0&range=B2:F63&output=csv']
    
    for division in ['open', 'mixed', 'women']: 
        div,create=Tournament.objects.get_or_create(name=division)
                   
        teams=csv.reader(open('windmill/regdata/'+division+'.csv'))

        seed=1
        for team in itertools.islice(teams,1,100):
            # First check if team with this name already exists, otherwise create it
            t,created=Team.objects.get_or_create(name=team[0],tournament=div)
            
            if isin(division,team[0]):
                t.seed=seed
                seed += 1
            else:    
                t.seed = None
        
            t.short_name = team[0]
            t.team_email = team[1]
            t.contact_name = team[2]
            t.contact_email = team[3]
            t.sec_contact_name = team[4]
            t.sec_contact_email = team[5]
            if division == 'women': # due to different order in ffindr-data...
                t.city = team[13]
                t.country = team[6]
            else:
                t.city = team[6]
                t.country = team[7]                
            t.mobile1 = team[9]
            t.mobile2 = team[10]
            t.mobile3 = team[11]
            t.mobile4 = team[12]
            t.mobile5 = team[13]
            t.comment = team[14]
            t.tournament=div
            t.save()
        
 