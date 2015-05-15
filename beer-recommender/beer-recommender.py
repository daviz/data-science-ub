# -*- coding: utf-8 -*-
"""
Created on Wed May 13 20:23:40 2015

@author: daviz
"""


def distEuclid(x, y):
    sum_of_squares=float(math.sqrt(sum(pow((x-y),2))))
    return 1.0/(1.0+sum_of_squares)

def SimEuclid(DataFrame,User1,User2,min_common_items=10):
    # GET Beers OF user1
    beers_user1=DataFrame[DataFrame['review_profilename'] == User1 ]
    # GET Beers OF user2
    beers_user2=DataFrame[DataFrame['review_profilename'] == User2 ]
    # FIND beers
    rep=pd.merge(beers_user1, beers_user2,on='beer_beerid')    
    if len(rep)==0:
        return 0
    if(len(rep)<min_common_items):
        return 0
    return distEuclid(rep['review_overall_x'],rep['review_overall_y']) 

class CollaborativeFiltering:
    """ Collaborative filtering using a custom sim(u,u'). """
    
    def __init__(self,DataFrame, similarity=SimEuclid):
        """ Constructor """
        self.sim_method=similarity#re Gets recommendations for a person by using a weighted average
        self.df=DataFrame
        self.sim = pd.DataFrame(np.sum([0]),columns=self.df.review_profilename.unique(), index=self.df.review_profilename.unique())

    def learn(self):
        """ Prepare data structures for estimation. Similarity matrix for users """
        allUsers=set(self.df['review_profilename'])
        self.sim = {}
        for person1 in allUsers:
            self.sim.setdefault(person1, {})
            for person2 in allUsers:
                # no es comparem am nosalres mateixos
                if person1==person2: continue
                
                self.sim.setdefault(person2, {})
                if(self.sim[person2].has_key(person1)):continue # since is a simetric matrix
                sim=self.sim_method(self.df,person1,person2)
                if(sim<0):
                    self.sim[person1][person2]=0
                    self.sim[person2][person1]=0
                else:
                    self.sim[person1][person2]=sim
                    self.sim[person2][person1]=sim
                
                
    def estimate(self, user_id, beer_id):
        totals={}
        beer_users = self.df[self.df['beer_beerid'] == beer_id]
        rating_num = 0.0
        rating_den = 0.0
        allUsers=set(beer_users['review_profilename'])
        for other in allUsers:
            if user_id == other: continue 
            rating_num += self.sim[user_id][other] * float(beer_users[beer_users['review_profilename']==other]['review_overall'])
            rating_den += self.sim[user_id][other]
        if rating_den==0: 
            if self.df.review_overall[self.df['beer_beerid'] == beer_id].mean() > 0:
                # return the mean movie rating if there is no similar for the computation
                return self.df.review_overall[self.df['beer_beerid'] == beer_id].mean()
            else:
                # else return mean user rating 
                return self.df.review_overall[self.df['review_profilename'] == user_id].mean()
        return rating_num/rating_den

reco = CollaborativeFiltering(df)
reco.learn

reco.estimate(user_id='stcules',beer_id=47969 )