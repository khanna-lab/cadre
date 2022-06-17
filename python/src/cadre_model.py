print("This is the Model file")

## model release processes

from numpy import random
import numpy as np
import pandas as pd
import cadre_person

class Model:
    RACE_DISTRIBUTION = [
        71.4/100, #white alone
        8.5/100, #black alone
        16.3/100, #hispanic alone
        3.8/100 #asian alone (increased by 0.1 to sum to 1)
        # REF: https://censusreporter.org/profiles/04000US44-rhode-island/
    ]

    RACE_CATS = ["white", "black", "hispanic", "other"]
    
    SMOKING_PREV = 0.13 #REF: https://www.cdc.gov/tobacco/data_statistics/fact_sheets/adult_data/cig_smoking/index.htm
    
    FEMALE_PROP = 51.3/100 # REF: https://www.census.gov/quickfacts/RI
    
    ALC_USE_PROPS = [8.3/100, 72.9/100, 13.2/100, 5.6/100] #see derivation in file:///Volumes/GoogleDrive/My%20Drive/code/cadre/r/explain-population-initialization.nb.html


    def __init__(self, n, verbose=True):
        self.my_persons = [] 
        
        age_sum = 0
        race = []
        females = 0
        alc_use_status = [] 
        smokers = 0 
        n_current_incarcerated = 0
        last_incarceration_time = []
        
        
        # initialize agents and attributes
        for i in range(n):
            person = Person.Person(age=random.randint(18, 65), 
                            race=random.choice(Model.RACE_CATS, p=Model.RACE_DISTRIBUTION),
                            female=random.binomial(1, Model.FEMALE_PROP),
                            alc_use_status=random.choice(range(0, 4), p=Model.ALC_USE_PROPS),
                            smoker=random.binomial(1, Model.SMOKING_PREV),
                            current_incarceration_status=0,
                            last_incarceration_time = -1
                            ) 

            self.my_persons.append(person)
            age_sum = person.age + age_sum
            race.append(person.race) 
            females = person.female + females 
            alc_use_status.append(person.alc_use_status)
            smokers = person.smoker + smokers
            n_current_incarcerated = person.current_incarceration_status + n_current_incarcerated
            last_incarceration_time.append(last_incarceration_time)

            if verbose == True:
                print(person.name)
                print(person.age)
                print(person.alc_use_status, "\n")

        if verbose == True:
            race_dist = pd.value_counts(np.array(race))/len(race)*100
            alc_use_status_dist = pd.value_counts(np.array(alc_use_status))/len(alc_use_status)*100

            print("Number of agents is: " + 
                str(len(self.my_persons)))
            print("Mean agent age is: " + 
                str(('{:.2f}'.format(age_sum/len(self.my_persons)))))
            print("Distribution of race categories is ", "\n" + 
                str(race_dist.round(decimals=2)), "%")
            print("Number of females is: " + 
                str(females))
    
    def run(self, MAXTIME=10):
        
        ages = []
        current_incarceration_statuses = []
        last_incarceration_times = []

        for time in range(MAXTIME):
            
            #if time % 1 == 0:
            print("Timestep = " + str(time))
            print("Mean age at time " + str(time) + " is " + str(('{:.4f}'.format(np.mean(ages)))))
            #print("Ages at time " + str(time) + " is " + str(ages)) 
            #print("Incarcerated persons at time " + str(time) + " is " + str(current_incarceration_statuses))
            print("Number of incarcerated persons at time " + str(time) + " is " + 
                str(sum(current_incarceration_statuses)) + " out of a total " + str(len(ages)))
            print("Last incarceration times are " + str(last_incarceration_times)) 
        
            # ensure that these vectors only hold the agent attributes at the current time 
            # (as opposed to appending) values from all times 
            ages = [] 
            current_incarceration_statuses = []
            last_incarceration_times = []
            
            for person in self.my_persons:
                person.aging()
                ages.append(person.age)
                person.transition_alc_use()
                person.simulate_incarceration(time=time)
                current_incarceration_statuses.append(person.current_incarceration_status)
                last_incarceration_times.append(person.last_incarceration_time)
    
def main():
    model = Model(n=100, verbose=True)
    model.run(MAXTIME=50)
  
if __name__ == "__main__":
    main()
    
        
