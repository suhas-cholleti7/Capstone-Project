import time

import pandas as pd
import random
from v_1.populator import Populator
from datetime import timedelta, datetime
from collections import deque


class Simulate:
    def __init__(self):
        random.seed(10)
        self.infected_set = set()
        self.recovery_time_probability = [2*7, 2*7, 2*7, 2*7, 2*7, 2*7, 2*7, 2*7, 3*7, 4*7, 5*7, 6*7, 0]
        self.day_list = []

    def select_infected(self, people_df):
        """
        To select random infected people - 20
        :param people_df: input merged dataframe
        :return: potential_infects_df
        """
        # Infecting 20 people randomly on day 1.
        random_infected_df = people_df.loc[people_df["date"] == str(datetime(2020, 1, 1).date())].sample(n=20)
        random_infected_df["exposed"] = 1
        random_infected_df["quarantined"] = 0
        for index, infected in random_infected_df.iterrows():
            """
            This block defines the incubation period and the date of infection of the virus for the people who have been infected on day 1 by the developer.
            The incubation period is based on the infection date. Once the person comes out of the incubation period, the person should come out of the recovery
            phase. The recovery date is based on the date of infection. During this time, the person cannot infect others. The person also quarantines.
            """
            incubation_period = random.randint(2, 15)
            self.infected_set.add(infected["person_id"])
            infected["incubation_period"] = incubation_period
            exposed_date = datetime.strptime(infected["date"], '%Y-%m-%d').date()
            infection_date = exposed_date + timedelta(days=incubation_period)
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(datetime(2020, 1, 1).date())), "new_infection"] = 1
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(datetime(2020, 1, 1).date())), ["exposed", "quarantined"]] = [1, 0]
            random_infected_df.loc[(random_infected_df["person_id"] == infected["person_id"]) & (random_infected_df["date"] == str(datetime(2020, 1, 1).date())), ["exposed", "quarantined"]] = [1, 0]
            incubation_date_list = []
            recovery_date_list = []
            start_date = datetime(2020, 1, 1).date()
            delta_incubation = infection_date - start_date
            for i in range(delta_incubation.days + 1):
                incubation_date_list.append(start_date + timedelta(days=i))
            for day in incubation_date_list:
                people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(day)), ["quarantined", "exposed"]] = [0, 1]
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(infection_date)), "quarantined"] = 1
            random_infected_df.loc[(random_infected_df["person_id"] == infected["person_id"]) & (random_infected_df["date"] == str(infection_date)), "quarantined"] = 1
            recovery_time = int(random.choice(self.recovery_time_probability))
            date_of_recovery = infection_date + timedelta(days=recovery_time)
            delta_recovery = date_of_recovery - infection_date
            for i in range(delta_recovery.days + 1):
                recovery_date_list.append(infection_date + timedelta(days=i))
            for day in recovery_date_list:
                people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(day)), ["quarantined", "exposed"]] = [1, 0]
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(date_of_recovery)), ["quarantined", "exposed"]] = [0, 0]
            # Might have to include family members as exposed - haven't done the same in the report yet
            self.infected_set.add(infected["person_id"])
        return people_df, random_infected_df

    def simulate_infections(self, family_info, people_df, random_infected_df):
        """
        To simulate the spread of infections
        :param family_info: dictionary with family information
        :param potential_infects_df: Dataframe with potentially infected people
        :param random_infected_df: Randomly infected people dataframe
        :return:
        """
        # For each day, get all the people with 1 for exposed. Compare this with all others.
        # Family members are also exposed the next day
        # If the exposed wears a mask and the exposee wears a mask, then NO transmission
        # If the exposed doesn't wear a mask and the exposee wears a mask, then transmission
        # If the exposed and the exposee doesn't wear masks, then transmission
        # Following should be included in the checking condition:
        #   1. mask
        #   2. dog_walk
        #   3. in_school
        #   4. attend_work
        #   5. prayer_group
        #   6. play_sports
        #   7. volunteering
        #   8. grocery_visit
        #   9. gasoline_visit
        # All the above are to be checked only if the infected is Exposed and the person in main data is not Exposed
        start_date = datetime(2020, 1, 1).date()
        end_date = datetime(2020, 12, 31).date()
        delta_dates = end_date - start_date
        for i in range(delta_dates.days + 1):
            self.day_list.append(start_date + timedelta(days=i))
        for curr_date in self.day_list:
            # To get all the people infected on curr_date
            curr_day_infected_df = people_df.loc[(people_df["date"] == str(curr_date)) & (people_df["exposed"] == 1)]
            curr_day_infected_deque = deque(curr_day_infected_df.to_dict('index').values())
            print("_____________________________________________________")
            # To get all the people on people_df
            # people_list = people_df.to_dict('index').values()
            while curr_day_infected_deque:
                """
                Do the comparison, adding to the deque and removing the compared row from the infected_df
                """
                infected_person = curr_day_infected_deque.popleft()
                print(curr_date)
                curr_day_people = people_df.loc[people_df["date"] == str(curr_date)]
                curr_day_people_list = curr_day_people.to_dict('index').values()
                for new_person in curr_day_people_list:
                    if new_person["person_id"] not in self.infected_set and infected_person["person_id"] != new_person["person_id"]:
                        self.infected_set.add(new_person["person_id"])
                        infection = self.check_infection(infected_person, new_person)
                        """
                        This block is to assign an incubation period based on the date of infection that is generated based on the contact with the infected person.
                        The date of recovery is randomly generated between 2 weeks and 6 weeks. During this period, the person is quarantined and cannot infect others..
                        """
                        if infection:
                            people_df.loc[(people_df["person_id"] == new_person["person_id"]) & (people_df["date"] == str(curr_date)), ["exposed", "quarantined", "new_infection"]] = [1, 0, 1]
                            curr_day_infected_deque.append(people_df.loc[(people_df["person_id"] == new_person["person_id"]) & (people_df["date"] == str(curr_date))].to_dict('index'))
                            incubation_period = random.randint(2, 15)
                            infection_date = curr_date + timedelta(days=incubation_period)
                            incubation_date_list = []
                            recovery_date_list = []
                            delta_incubation = infection_date - curr_date
                            for i in range(delta_incubation.days + 1):
                                incubation_date_list.append(start_date + timedelta(days=i))
                            for day in incubation_date_list:
                                people_df.loc[(people_df["person_id"] == new_person["person_id"]) & (people_df["date"] == str(day)), ["quarantined", "exposed"]] = [0, 1]
                            people_df.loc[(people_df["person_id"] == new_person["person_id"]) & (people_df["date"] == str(infection_date)), "quarantined"] = 1
                            recovery_time = int(random.choice(self.recovery_time_probability))
                            date_of_recovery = infection_date + timedelta(days=recovery_time)
                            delta_recovery = date_of_recovery - infection_date
                            for i in range(delta_recovery.days + 1):
                                recovery_date_list.append(infection_date + timedelta(days=i))
                            for day in recovery_date_list:
                                people_df.loc[(people_df["person_id"] == new_person["person_id"]) & (people_df["date"] == str(day)), ["quarantined", "exposed"]] = [1, 0]
                            people_df.loc[(people_df["person_id"] == new_person["person_id"]) & (people_df["date"] == str(date_of_recovery)), ["quarantined", "exposed"]] = [0, 0]
        return people_df

    def check_infection(self, infected_person, new_person):
        """
        To check if the person has come in contact with a person who is infected
        :param infected_person: Infected person details
        :param new_person: Healthy person details
        :return: If the healthy person is infected or not
        """
        if (infected_person["date"] == new_person["date"]) and \
            ((infected_person["mask"] == 0 and new_person["mask"] == 0) or (infected_person["mask"] == 0 and new_person["mask"] == 1) or (infected_person["mask"] == 1 and new_person["mask"] == 0)) and \
            ((infected_person["dog_walk"] == 1 and new_person["dog_walk"] == 1) or
             (infected_person["school_type"] == new_person["school_type"] and (infected_person["in_school"] == 1 and new_person["in_school"] == 1)) or
             (infected_person["attend_work"] == 1 and new_person["attend_work"] == 1) or
             (infected_person["prayer_group"] == 1 and new_person["prayer_group"] == 1) or
             (infected_person["play_sports"] == 1 and new_person["play_sports"] == 1) or
             (infected_person["volunteering"] == 1 and new_person["volunteering"] == 1) or
             (infected_person["grocery_visit"] == 1 and new_person["grocery_visit"] == 1) or
             (infected_person["gasoline_visit"] == 1 and new_person["gasoline_visit"] == 1)):
            return True
        return False


if __name__ == '__main__':
    start_time = time.time()
    people_data_df = pd.read_csv("merged.csv")
    sim = Simulate()
    potential_infects_df, random_infected_df = sim.select_infected(people_data_df)
    potential_infects_df.to_csv("potential_infects.csv", index=False)
    random_infected_df.to_csv("infected.csv", index=False)
    pop = Populator()
    family_info = pop.family_data
    updated_people_df = sim.simulate_infections(family_info, potential_infects_df, random_infected_df)
    updated_people_df.to_csv("updated_people.csv", index=False)
    print("The time taken is:", (time.time()-start_time)/60)