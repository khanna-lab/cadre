from numpy import random
import pycadre.load_params as load_params
import csv

# read parameters

class Person():
    def __init__(self, name=None):

        MIN_AGE = load_params.params_list['MIN_AGE']
        MAX_AGE = load_params.params_list['MAX_AGE']+1
        RACE_CATS = load_params.params_list['RACE_CATS']
        FEMALE_PROP = load_params.params_list['FEMALE_PROP']
        RD = load_params.params_list['RACE_DISTRIBUTION']
        RACE_DISTRIBUTION = [
            RD['White'],
            RD['Black'],
            RD['Hispanic'], 
            RD['Asian']]
        AU_PROPS = load_params.params_list['ALC_USE_PROPS']
        ALC_USE_PROPS = [AU_PROPS['A'], AU_PROPS['O'], AU_PROPS['R'], AU_PROPS['D']]   

        self.name = name    
        self.age = random.randint(MIN_AGE, MAX_AGE)
        self.race = random.choice(RACE_CATS, p=RACE_DISTRIBUTION)
        self.female = random.binomial(1, FEMALE_PROP)
        self.alc_use_status = random.choice(range(0, len(ALC_USE_PROPS)), p=ALC_USE_PROPS)
        self.current_incarceration_status = 0
        self.last_incarceration_time = -1
        self.incarceration_duration = -1
        self.last_release_time = -1
        self.dur_cat = -1
        self.sentence_duration = -1
        self.n_incarcerations = 0
        self.assign_smoker_status() #note self.smoker = self.assign_smoker_status() was giving all smoking statuses as None. but this works


    def aging(self):
        TICK_TO_YEAR_RATIO = load_params.params_list['TICK_TO_YEAR_RATIO']
        self.age += 1/TICK_TO_YEAR_RATIO

    def transition_alc_use(self):

        # level up
        ALC_USE_STATES = load_params.params_list['ALC_USE_STATES']
        TRANS_PROB_0_1 = ALC_USE_STATES['TRANS_PROB_0_1']
        TRANS_PROB_1_2 = ALC_USE_STATES['TRANS_PROB_1_2']
        TRANS_PROB_2_3 = ALC_USE_STATES['TRANS_PROB_2_3']
        # LEVEL DOWN
        TRANS_PROB_1_0 = ALC_USE_STATES['TRANS_PROB_1_0']
        TRANS_PROB_2_1 = ALC_USE_STATES['TRANS_PROB_2_1']
        TRANS_PROB_3_2 = ALC_USE_STATES['TRANS_PROB_3_2']

        prob = random.uniform(0, 1)
        if self.alc_use_status == 0:
            if (prob <= TRANS_PROB_0_1):
                self.alc_use_status += 1


        elif self.alc_use_status == 1:
            if (prob <= TRANS_PROB_1_2):
                self.alc_use_status += 1

            elif (prob > 1-TRANS_PROB_1_0):
                self.alc_use_status -= 1

        
        elif self.alc_use_status == 2:
            if (prob <= TRANS_PROB_2_3):
                self.alc_use_status += 1

            elif (prob > 1-TRANS_PROB_2_1):
                self.alc_use_status -= 1

        elif self.alc_use_status == 3:
            if (prob > 1-TRANS_PROB_3_2):
                self.alc_use_status -= 1

    def update_attributes_at_incarceration_time(self, time):
        self.current_incarceration_status = 1 
        self.last_incarceration_time = time  
        self.incarceration_duration = 0   
        self.n_incarcerations += 1
        self.assign_sentence_duration_cat()
        self.assign_sentence_duration()

    def simulate_incarceration(self, time, probability_daily_incarceration):
        
        prob = random.uniform(0, 1)

        if self.current_incarceration_status == 0:
            if self.n_incarcerations == 0:
                if prob < probability_daily_incarceration:
                    self.update_attributes_at_incarceration_time(time=time)
                   
    def simulate_recidivism(self, time, probability_daily_recidivism_females, probability_daily_recidivism_males):

        prob = random.uniform(0, 1)
        
        if self.current_incarceration_status == 0:
            if self.n_incarcerations > 0:
                if self.female == 1:
                    if prob < probability_daily_recidivism_females:
                            self.update_attributes_at_incarceration_time(time=time)
            
            elif self.female == 0:
                if prob < probability_daily_recidivism_males:
                         self.update_attributes_at_incarceration_time(time=time)

    def simulate_release(self, time):
                      
        if self.sentence_duration >= 0:
            if self.incarceration_duration >= self.sentence_duration:
                    self.current_incarceration_status = 0
                    self.last_release_time = time
                    self.incarceration_duration = -1

    def assign_sentence_duration_cat(self):
            ALL_SDEMP = load_params.params_list['SENTENCE_DURATION_EMP']
            FEMALE_SDEMP =  ALL_SDEMP['females']
            MALE_SDEMP = ALL_SDEMP['males']
            FEMALE_SDEMP_DURATIONS = list(FEMALE_SDEMP.keys())
            FEMALE_SDEMP_PROPS = list(FEMALE_SDEMP.values())
            MALE_SDEMP_DURATIONS = list(MALE_SDEMP.keys())
            MALE_SDEMP_PROPS = list(MALE_SDEMP.values())

            if self.female == 1:
                if self.current_incarceration_status == 1: 
                    self.dur_cat = random.choice(FEMALE_SDEMP_DURATIONS, p=FEMALE_SDEMP_PROPS)


            elif self.female == 0:
                if self.current_incarceration_status == 1: 
                    self.dur_cat = random.choice(MALE_SDEMP_DURATIONS, p=MALE_SDEMP_PROPS)    
                
               

    def assign_sentence_duration(self):
            
            if self.dur_cat == 0:
                self.sentence_duration = random.randint(7, 29) #IN DAILY UNITS, CHANGE IF UNITS CHANGE
            elif self.dur_cat == 1:
                self.sentence_duration = random.randint(29, 183)
            elif self.dur_cat == 2:
                self.sentence_duration = random.randint(183, 366)
            elif self.dur_cat == 3:
                self.sentence_duration = random.randint(366, 1096)
            elif self.dur_cat == 4:
                self.sentence_duration = random.randint(1096, 2191)

    def assign_smoker_status(self):

        SMOKING_CATS = load_params.params_list['SMOKING_CATS']
        SMOKING_PREV = load_params.params_list['SMOKING_PREV']
        
        SMOKING_PREV_WHITE_MALE = [SMOKING_PREV['WHITE_MALE_CURRENT'], SMOKING_PREV['WHITE_MALE_FORMER'], SMOKING_PREV['WHITE_MALE_NEVER']]
        SMOKING_PREV_WHITE_FEMALE = [SMOKING_PREV['WHITE_FEMALE_CURRENT'], SMOKING_PREV['WHITE_FEMALE_FORMER'], SMOKING_PREV['WHITE_FEMALE_NEVER']]
        SMOKING_PREV_BLACK_MALE = [SMOKING_PREV['BLACK_MALE_CURRENT'], SMOKING_PREV['BLACK_MALE_FORMER'], SMOKING_PREV['BLACK_MALE_NEVER']]
        SMOKING_PREV_BLACK_FEMALE = [SMOKING_PREV['BLACK_FEMALE_CURRENT'], SMOKING_PREV['BLACK_FEMALE_FORMER'], SMOKING_PREV['BLACK_FEMALE_NEVER']]
        SMOKING_PREV_HISPANIC_MALE = [SMOKING_PREV['HISPANIC_MALE_CURRENT'], SMOKING_PREV['HISPANIC_MALE_FORMER'], SMOKING_PREV['HISPANIC_MALE_NEVER']]
        SMOKING_PREV_HISPANIC_FEMALE = [SMOKING_PREV['HISPANIC_FEMALE_CURRENT'], SMOKING_PREV['HISPANIC_FEMALE_FORMER'], SMOKING_PREV['HISPANIC_FEMALE_NEVER']]
        SMOKING_PREV_ASIAN_MALE = [SMOKING_PREV['ASIAN_MALE_CURRENT'], SMOKING_PREV['ASIAN_MALE_FORMER'], SMOKING_PREV['ASIAN_MALE_NEVER']]
        SMOKING_PREV_ASIAN_FEMALE = [SMOKING_PREV['ASIAN_FEMALE_CURRENT'], SMOKING_PREV['ASIAN_FEMALE_FORMER'], SMOKING_PREV['ASIAN_FEMALE_NEVER']]

 
        if self.race == 'White':
            if self.female == 0:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_WHITE_MALE)
            elif self.female == 1:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_WHITE_FEMALE)    

        elif self.race == 'Black':
            if self.female == 0:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_BLACK_MALE)            
            elif self.female == 1:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_BLACK_FEMALE)    

        elif self.race == 'Hispanic':
            if self.female == 0:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_HISPANIC_MALE)            
            elif self.female == 1:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_HISPANIC_FEMALE)  

        elif self.race == 'Asian':
            if self.female == 0:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_ASIAN_MALE)            
            elif self.female == 1:
                self.smoker = random.choice(SMOKING_CATS, p=SMOKING_PREV_ASIAN_FEMALE) 
  
   
    def step(self, time):
            self.aging()
            self.transition_alc_use()

            self.simulate_incarceration(time=time, probability_daily_incarceration=load_params.params_list['PROBABILITY_DAILY_INCARCERATION'])
            
            if(self.current_incarceration_status == 1):
                self.incarceration_duration += 1

            self.simulate_release(time=time)
            self.simulate_recidivism(time=time, probability_daily_recidivism_females=load_params.params_list['PROBABILITY_DAILY_RECIDIVISM']['FEMALES'], probability_daily_recidivism_males=load_params.params_list['PROBABILITY_DAILY_RECIDIVISM']['MALES'])


        
            


