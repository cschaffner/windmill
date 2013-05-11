'''
Created on 27 Jun 2012
@author: Christian Schaffner, huebli@gmail.com
'''
from django.conf import settings
from numpy import savez,savetxt,asarray,arange
from scipy.sparse import coo_matrix, linalg as splinalg
#from pylab import plot,show
#import matplotlib.pyplot as plt
import networkx as nx
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.powerrank')


def strength(games,output_path):
    '''
    Takes a list of games and returns a dictionary with the "strength" of the involved teams
    "strength" is computed as solution to the linear least-square problem A*strength=margins
    '''
    from datetime import datetime
        
    # create a list of all team_ids involved in "games"
    tlist=[]
    tnamelist=[]
    for game in games:
        if game['team_1_score']>0 or game['team_2_score']>0:
            if game['team_1_id'] not in tlist:
                tlist.append(game['team_1_id'])
                tnamelist.append(game['team_1']['name'])
            if game['team_2_id'] not in tlist:
                tlist.append(game['team_2_id'])
                tnamelist.append(game['team_2']['name'])
    
    # set up least-square problem
    nrteams=len(tlist)
    row=[]
    col=[]
    val=[]
    margins=[]
    igame=0
    for game in games:
        if game['team_1_score']>0 or game['team_2_score']>0:
            row.append(igame)
            col.append(tlist.index(game['team_1_id']))
            val.append(1)
            row.append(igame)
            col.append(tlist.index(game['team_2_id']))
            val.append(-1)        
            margins.append(game['team_1_score']-game['team_2_score'])
            igame += 1
    
    nrgames=igame
    logger.info('nr of games taken into account: {0}'.format(nrgames))
    Asp=coo_matrix((val,(row,col)), shape=(nrgames,nrteams))
    # convert margins - list to ndarray
    margins=asarray(margins)
    
#    savez('data',Asp=Asp,margins=margins)
#    savetxt('A.out', Asp.todense() , delimiter=',',fmt='%i')
#    savetxt('m.out', margins, delimiter=',',fmt='%i')
    
    # use iterative method for sparse least-square problem: Asp * strength = margins
    result = splinalg.lsqr(Asp,margins)
    logger.info(result)
    
    strength=result[0]
    residues = Asp.dot(strength)-margins
    logger.info(pformat(strength))
    logger.info(pformat(residues))
    
    # give indices to teams, sorted according to strength
    indsort=sorted(arange(nrteams),key=lambda x:strength[x],reverse=True)
    
    standings=[]
    for rank,i in enumerate(indsort,1):
        logger.info(u'rk:{2}  {0:<20}: {1:f}'.format(tnamelist[i],strength[i],rank))
        standings.append({'ranking': rank, 'team_id': tlist[i], 'strength': strength[i], 'team': {'name': tnamelist[i]}})
    
    # create connectivity graph
    G=nx.MultiGraph()
    for t in tlist:
        G.add_node(t)
        
    for i in arange(nrgames):
        Arow=Asp.getrow(i)
        G.add_weighted_edges_from([(tlist[Arow.indices[0]],tlist[Arow.indices[1]],Arow.dot(strength).item())])
    
    plt.clf()
    nx.draw_spring(G)
    plt.savefig("{0}/graph_{1}.png".format(output_path,nrgames))
    plt.clf()
    
    # the histogram of the data
    n, bins, patches = plt.hist(residues, normed=1, facecolor='green')
    #
    ## add a 'best fit' line
    #y = mlab.normpdf( bins, mu, sigma)
    #l = plt.plot(bins, y, 'r--', linewidth=1)
    
    plt.xlabel('Residue')
    plt.ylabel('Probability')
    plt.title(r'Histogram of residues:')
    plt.axis([-15, 15, 0, max(n)*1.05])
    plt.grid(True)
    plt.savefig('{0}/histogram_{1}.png'.format(output_path,nrgames))
    
    return standings
