import collections
import json
import sys
import time
import numpy as np
import pandas as pd
import random
from datetime import timedelta, datetime
# from visualizer_v3 import sir_emulation
# from memory_profiler import profile

"""
This program is a simulator that simulates how a virus spreads across a community during a complete lockdown.
Only the essential functions of people are taken into consideration here.
In this program, the initial set of infections is assigned and the algorithm propagates the virus further.
The propagation is governed by probabilities provided by the users (This functionality is not implemented yet).

Author: Ravikiran Jois Yedur Prabhakar
Advisor: Dr. Thomas B. Kinsman
"""

class Simulate:
    def __init__(self):
        """
        All the important parameters and global variables are introduced and declared here
        Many probabilities that are to be satisfied in order to contract the virus are also mentioned here
        """
        random.seed(10)
        self.infected_set = set()
        self.recovery_time_probability = [random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 28), random.randint(2, 28), random.randint(2, 28),
                                          random.randint(2, 28), random.randint(2, 35), random.randint(2, 42)]
        self.day_list = []
        self.new_infection_date_dict = collections.Counter()
        self.recovery_date_dict = collections.Counter()
        self.susceptible_dict = collections.Counter()
        self.quarantined_dates_info = collections.defaultdict(set)
        self.contagious_dates_info = collections.defaultdict(set)
        self.death_dict = collections.Counter()
        self.total_infections = 0
        self.mask_prob_equal = [1, 0]
        self.dog_walk_prob = float(sys.argv[2])
        self.volunteer_prob = float(sys.argv[3])
        self.grocery_prob = float(sys.argv[4])
        self.gas_prob = float(sys.argv[5])
        # Left is healthy and not wearing mask - 0, Right is contagious - not wearing mask - 0
        self.mask_00 = float(sys.argv[6])
        # Left healthy and not wearing mask - 0, Right contagious - wearing mask - 1
        self.mask_01 = float(sys.argv[7])
        # Left healthy and wearing mask - 1, Right contagious - not wearing mask - 0
        self.mask_10 = float(sys.argv[8])
        # When both people wear mask - Left 1 and Right 1
        self.mask_11 = float(sys.argv[9])
        # Probability of the person being removed from the population if recovered between 2 and 4 weeks of infection.
        self.prob_death_4_weeks = float(sys.argv[10])
        # Probability of the person being removed from the population if recovered after 4 weeks of infection.
        self.prob_death_gt4_weeks = float(sys.argv[11])
        self.contact = []
        self.probability_list = [0.1 * x for x in range(1, 10)]
        self.counter_date = dict()


    def generate_dates(self):
        """
        The method generates the dates for the simulation and adds it to a list
        :return: None
        """
        start_date = datetime(2020, 1, 1).date()
        end_date = datetime(2020, 5, 31).date()
        delta_dates = end_date - start_date
        for i in range(delta_dates.days + 1):
            self.day_list.append(start_date + timedelta(days=i))
            self.death_dict[str(start_date + timedelta(days=i))] = 0

    def initialize_infections(self, people_df):
        """
        This function initializes the infection for 5 random people. This function also defines the incubation period,
        infection date, contagious period, recovery date for these 5 people.
        :param people_df: The dataset with date, person and family data joined together
        :return: The updated people_df dataframe
        """
        random_infected_df = people_df.loc[(people_df["date"] == str(datetime(2020, 1, 1).date())) & (people_df["age"]>4)].sample(n=10)
        day = datetime(2020, 1, 1).date()
        self.day_counter = 1
        if str(datetime(2020, 1, 1).date()) not in self.death_dict:
            self.death_dict[str(datetime(2020, 1, 1).date())] = 0
        for index, infected in random_infected_df.iterrows():
            self.new_infection_date_dict[self.day_counter] += 1
            """An incubation period is randomly chosen between 2 and 15 days"""
            incubation_period = random.randint(5, 15)
            self.infected_set.add(infected["person_id"])
            exposed_date = datetime.strptime(infected["date"], '%Y-%m-%d').date()
            infection_date = exposed_date + timedelta(days=incubation_period)
            """The dates when the person who is infected spreads the virus are calculated using the exposed and the incubation periods"""
            contagious_date = infection_date - timedelta(days=2)
            range_of_contagious_dates = [str(contagious_date + timedelta(days=x)) for x in range((infection_date - contagious_date).days)]
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(exposed_date)), ["exposed", "quarantined", "new_infection"]] = [1, 0, 1]
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [1, 0, 0, 1]
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(infection_date)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
            """The recovery date is calculated based on the recovery time that has been generated using random valurs."""
            recovery_time = int(random.choice(self.recovery_time_probability))
            date_of_recovery = infection_date + timedelta(days=recovery_time)
            self.recovery_date_dict[str(date_of_recovery)] += 1
            prob_death = random.choice(self.probability_list)
            if (14 < recovery_time <= 28 and prob_death >= self.prob_death_4_weeks) or \
                    (recovery_time > 28 and prob_death >= self.prob_death_gt4_weeks):
                # If here, it is to check the date of removal from the population.
                if str(date_of_recovery) not in self.death_dict:
                    self.death_dict[str(date_of_recovery)] = 1
                else:
                    self.death_dict[str(date_of_recovery)] += 1
                death_day_idx = index + incubation_period + recovery_time
                people_df.at[death_day_idx, "death"] = 1
            range_of_quarantined_dates = set([infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"].isin(range_of_quarantined_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
        people_df = people_df.replace(np.nan, 0)
        self.counter_date[str(day)] = len(self.infected_set)
        self.susceptible_dict[self.day_counter] = int(sys.argv[1]) - len(self.infected_set)
        return people_df

    def start_simulations(self, merged_data_df):
        """
        This method is to start the simulation of the spread of the virus based on the nature of the initially
        infected's contagiousness and dates. The method keeps track of the daily counts for the number of the infected,
        the recovered and the susceptible population. The method also helps in spreading the virus via the chain reaction.
        :param merged_data_df: The data of the entire population along with the information of the initially contagious
        people
        :return: The updated dataframe
        """
        """A queue is initialized to handle the chain reactions. Every day, the people who are infected meet with other 
        people according ton their daily actions and thus, spread the virus"""
        contagious_queue = collections.deque()
        for day in self.day_list:
            print(day)
            self.day_counter += 1
            contagious_pot = merged_data_df.loc[(merged_data_df["date"] == str(day)) & (merged_data_df["contagious"].isin([1]))]
            if not contagious_pot.empty:
                contagious_queue.append(contagious_pot)
            """
            The tail of the queue is emptied every day to check the population that is contagious and has the ability to
            spread the virus.
            """
            while contagious_queue:
                # If here, it is to spread the virus by checking the contact between the infected and the healthy.
                cont_person = contagious_queue.popleft()
                cont_person_df = merged_data_df.loc[(merged_data_df["person_id"].isin(set(cont_person["person_id"]))) & (merged_data_df["date"] == str(day)) & (merged_data_df["contagious"].isin([1]))]
                merged_without_infected = merged_data_df.loc[~merged_data_df["person_id"].isin(self.infected_set) & (merged_data_df["date"] == str(day))  & (~merged_data_df["contagious"].isin([1]))]
                newly_exposed_set = self.virus_check(cont_person_df, merged_without_infected)
                self.infected_set = set.union(self.infected_set, newly_exposed_set)
                newly_exposed_df = merged_data_df.loc[(merged_data_df["person_id"].isin(newly_exposed_set)) & (merged_data_df["date"] == str(day))]
                counter = 0
                for index, infected in newly_exposed_df.iterrows():
                    """Similar to the initial dataset of contagious people, the incubation, recovery and contagious dates
                    are defined and simulated here."""
                    counter += 1
                    incubation_period = random.randint(5, 15)
                    exposed_date = day
                    merged_data_df.at[index, "new_infection"] = 1
                    infection_date = exposed_date + timedelta(days=incubation_period)
                    contagious_date = infection_date - timedelta(days=2)
                    range_of_contagious_dates = set([contagious_date + timedelta(days=x) for x in range((infection_date - contagious_date).days)])
                    self.new_infection_date_dict[self.day_counter] += 1
                    self.contagious_dates_info[infected["person_id"]] = range_of_contagious_dates
                    contagious_date_index = [d for d in range(index + incubation_period - 2, index + incubation_period)]
                    # Assign the contagious property on the mentioned dates
                    for c_date_idx in contagious_date_index:
                        merged_data_df.at[c_date_idx, "contagious"] = 1
                    recovery_time = int(random.choice(self.recovery_time_probability))
                    date_of_recovery = infection_date + timedelta(days=recovery_time)
                    self.recovery_date_dict[str(date_of_recovery)] += 1
                    range_of_recovery_dates = set([infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
                    prob_death = random.choice(self.probability_list)
                    if (14 < recovery_time < 28 and prob_death > self.prob_death_4_weeks) or (recovery_time > 28 and prob_death > self.prob_death_gt4_weeks):
                        # If here, it is to check the date of removal from the population.
                        if str(date_of_recovery) not in self.death_dict:
                            self.death_dict[str(date_of_recovery)] = 1
                        else:
                            self.death_dict[str(date_of_recovery)] += 1
                        death_day_idx = index + incubation_period + recovery_time
                        merged_data_df.at[death_day_idx, "death"] = 1
                    if recovery_time < 14:
                        # If here, the person is not to be removed from the population and will successfully recover
                        recovery_day_idx = index + incubation_period + recovery_time
                        merged_data_df.at[recovery_day_idx, "recovery"] = 1
                    self.quarantined_dates_info[infected["person_id"]] = range_of_recovery_dates

                newly_contagious = merged_data_df.loc[(~merged_data_df["person_id"].isin(self.infected_set)) & (merged_data_df["contagious"].isin([1])) & (merged_data_df["date"].isin([day]))]
                if not newly_contagious.empty:
                    contagious_queue.append(newly_contagious)
            self.counter_date[str(day)] = len(self.infected_set)
            print(len(self.infected_set))
            self.susceptible_dict[self.day_counter] = int(sys.argv[1]) - len(self.infected_set)
            print("next day")

        return merged_data_df

    def virus_check(self, cont_person, curr_day_person_df):
        """
        This method is used to filter the people who are involved in the spread of the virus. The attributes and
        actions of people involved in the contact are examined and the people who match the constraints contribute to the
        spread of the virus.
        :param cont_person: The person who is contagious.
        :param curr_day_person_df: The dataframe of people who can get infected.
        :return: Set of person_ids of the people who have caught the infection.
        """
        # curr_day_person_df = curr_day_person_df.loc[~curr_day_person_df["person_id"].isin(self.infected_set)]
        # merged_df is a temporary dataframe
        merged_df = curr_day_person_df.merge(cont_person, on=["date"], how="inner", suffixes=['_1', '_2'])
        del curr_day_person_df

        # To filter out people who are already infected
        merged_df = merged_df.loc[merged_df["person_id_1"] != merged_df["person_id_2"]]

        # To get the joint probabilities of people for different activities
        merged_df["mask_condition_1"] = merged_df["mask_exposure_1"] * merged_df["mask_exposure_2"]
        merged_df["dog_walk_meetup_1"] = merged_df["dog_walk_exposure_1"] * merged_df["dog_walk_exposure_2"]
        merged_df["volunteer_meetup_1"] = merged_df["volunteering_exposure_1"] * merged_df["volunteering_exposure_2"]
        merged_df["grocery_meetup_1"] = merged_df["grocery_exposure_1"] * merged_df["grocery_exposure_2"]
        merged_df["gas_meetup_1"] = merged_df["gas_exposure_1"] * merged_df["gas_exposure_2"]

        # To filter data from the dataframe for mask conditions based on the probabilities given. This is a temporary dataframe
        merged_filtered_df = pd.concat([merged_df.loc[(merged_df["mask_1"].isin([1])) & (merged_df["mask_2"].isin([1])) & (merged_df["mask_condition_1"] >= self.mask_11)],
                            merged_df.loc[(merged_df["mask_1"].isin([1])) & (merged_df["mask_2"].isin([0])) & (merged_df["mask_condition_1"] >= self.mask_10)],
                            merged_df.loc[(merged_df["mask_1"].isin([0])) & (merged_df["mask_2"].isin([1])) & (merged_df["mask_condition_1"] >= self.mask_01)],
                            merged_df.loc[(merged_df["mask_1"].isin([0])) & (merged_df["mask_2"].isin([0])) & (merged_df["mask_condition_1"] >= self.mask_00)]], axis=0)

        del merged_df

        # To filter the dataframe based on the people who match the activities' criteria.
        merged_filtered_df = merged_filtered_df.loc[((merged_filtered_df["dog_walk_1"].isin([1]) & merged_filtered_df["dog_walk_2"].isin([1])) & (merged_filtered_df["dog_walk_type_1"] == merged_filtered_df["dog_walk_type_2"]) & (merged_filtered_df["dog_walk_meetup_1"] >= self.dog_walk_prob)) |
                            ((merged_filtered_df["volunteering_1"].isin([1]) & merged_filtered_df["volunteering_2"].isin([1])) & (merged_filtered_df["volunteering_type_1"] == merged_filtered_df["volunteering_type_2"]) & (merged_filtered_df["volunteer_meetup_1"] >= self.volunteer_prob)) |
                            ((merged_filtered_df["grocery_visitor_1"].isin([1]) & merged_filtered_df["grocery_visitor_2"].isin([1])) & (merged_filtered_df["grocery_store_type_1"] == merged_filtered_df["grocery_store_type_2"]) & (merged_filtered_df["grocery_meetup_1"] >= self.grocery_prob)) |
                            ((merged_filtered_df["gas_visitor_1"].isin([1]) & merged_filtered_df["gas_visitor_2"].isin([1])) & (merged_filtered_df["gas_store_type_1"] == merged_filtered_df["gas_store_type_2"]) & (merged_filtered_df["gas_meetup_1"] >= self.gas_prob))]

        set_of_exposed_people = set(merged_filtered_df["person_id_1"])
        del merged_filtered_df
        return set_of_exposed_people


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: python3 birthdays_v3.py [Argument_1] [Argument_2] [Argument_3] [Argument_4] [Argument_5] [Argument_6] [Argument_7] [Argument_8] [Argument_9] [Argument_10] [Argument_11]")
        print("     Argument_1: Number of people in the population")
        print("     Argument_2: Dog-walk Going Probability")
        print("     Argument_3: Volunteering Probability")
        print("     Argument_4: Grocery shop Going Probability")
        print("     Argument_5: Gas-store Going Probability")
        print("     Argument_6: Probability of Nobody Wearing Masks")
        print("     Argument_7: Probability of Healthy person Wearing Mask")
        print("     Argument_8: Probability of Contagious person Wearing Mask")
        print("     Argument_9: Probability of Both Healthy and Contagious Persons Wearing Masks")
        print("     Argument_10: Probability of Person Dying in the First 4 Weeks")
        print("     Argument_11: Probability of Person Dying After 4 Weeks of Infection")
        sys.exit()
    start = time.time()
    sim = Simulate()
    fully_merged_data = pd.read_csv("../Results/Data/merged.csv", dtype={"work_type": "string", "volunteering_type": "string", "prayer_group_type": "string", "sports_type": "string", "dog_walk_type": "string"})
    sim.generate_dates()
    fully_merged_data_df = sim.initialize_infections(fully_merged_data)
    fully_merged_data_df = sim.start_simulations(fully_merged_data_df)
    # print("The simulator count is:", sim.simulator_count)
    print("The number of infected people are:", len(sim.infected_set))
    print(sim.counter_date)
    with open('../Results/Data/Lockdown/infections.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.counter_date))
    with open('../Results/Data/Lockdown/new_infection_date_ld_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.new_infection_date_dict))
    with open('../Results/Data/Lockdown/recovery_date_ld_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.recovery_date_dict))
    with open('../Results/Data/Lockdown/susceptible_ld_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.susceptible_dict))
    with open('../Results/Data/Lockdown/death_ld_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.death_dict))
    fully_merged_data_df.to_csv("../Results/Data/Lockdown/total_lockdown.csv", index=False)
    print("Total time taken:", (time.time() - start)/60)