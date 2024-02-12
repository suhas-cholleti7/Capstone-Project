import collections
import json
import time
import numpy as np
import pandas as pd
import random
from datetime import timedelta, datetime

"""
This program is a simulator that simulates how a virus spreads across a community.
In this program, the initial set of infections is assigned and the algorithm propagates the virus further.
The propagation is governed by probabilities provided by the users (This functionality is not implemented yet).

Author: Ravikiran Jois Yedur Prabhakar
Advisor: Dr. Thomas B. Kinsman
"""

class Simulate:
    def __init__(self):
        random.seed(10)
        self.infected_set = set()
        self.recovery_time_probability = [2*7, 2*7, 2*7, 2*7, 2*7, 2*7, 2*7, 2*7, 3*7, 4*7, 5*7, 6*7]
        self.day_list = []
        self.new_infection_date_dict = collections.Counter()
        self.recovery_date_dict = collections.Counter()
        self.susceptible_dict = collections.Counter()
        self.quarantined_dates_info = collections.defaultdict(set)
        self.contagious_dates_info = collections.defaultdict(set)
        self.total_infections = 0
        self.mask_prob_equal = [1, 0]
        self.day_counter = 0
        self.school_prob = 0.6
        self.work_prob = 0.5
        self.dog_walk_prob = 0.7
        self.prayer_group_prob = 0.4
        self.volunteer_prob = 0.4
        self.play_sports_prob = 0.5
        self.grocery_prob = 0.5
        self.gas_prob = 0.5
        self.mask_00 = 0.1
        self.mask_01 = 0.6
        self.mask_10 = 0.3
        self.mask_11 = 0.9
        self.contact = []

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

    def initialize_infections(self, people_df):
        """
        This function initializes the infection for 5 random people. This function also defines the incubation period,
        infection date, contagious period, recovery date for these 5 people.
        :param people_df: The dataset with date, person and family data joined together
        :return: The updated people_df dataframe
        """
        random_infected_df = people_df.loc[(people_df["date"] == str(datetime(2020, 1, 1).date())) & (people_df["age"] > 4)].sample(n=5)
        day = datetime(2020, 1, 1).date()
        self.day_counter = 1
        for index, infected in random_infected_df.iterrows():
            self.new_infection_date_dict[self.day_counter] += 1
            """An incubation period is randomly chosen between 2 and 15 days"""
            incubation_period = random.randint(2, 15)
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
            range_of_contagious_dates = set([infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
            people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
        people_df = people_df.replace(np.nan, 0)
        self.susceptible_dict[self.day_counter] = 10000 - len(self.infected_set)
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
                cont_person = contagious_queue.popleft()
                merged_without_infected = merged_data_df.loc[~merged_data_df["person_id"].isin(self.infected_set) & (merged_data_df["date"] == str(day))]
                newly_exposed_set = self.virus_check(cont_person, merged_without_infected)
                self.infected_set = set.union(self.infected_set, newly_exposed_set)
                newly_exposed_df = merged_data_df.loc[(merged_data_df["person_id"].isin(newly_exposed_set)) & (merged_data_df["date"] == str(day))]
                counter = 0
                for index, infected in newly_exposed_df.iterrows():
                    """Similar to the initial dataset of contagious people, the incubation, recovery and contagious dates
                    are defined and simulated here."""
                    counter += 1
                    incubation_period = random.randint(2, 15)
                    exposed_date = day
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
                    self.quarantined_dates_info[infected["person_id"]] = range_of_recovery_dates
                print(counter)
                newly_contagious = merged_data_df.loc[(~merged_data_df["person_id"].isin(self.infected_set)) & (merged_data_df["contagious"].isin([1])) & (merged_data_df["date"].isin([day]))]
                if not newly_contagious.empty:
                    contagious_queue.append(newly_contagious)

            self.susceptible_dict[self.day_counter] = 10000 - len(self.infected_set)
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
        curr_day_person_df = curr_day_person_df.loc[~curr_day_person_df["person_id"].isin(self.infected_set)]
        df = curr_day_person_df.merge(cont_person, on=["date"], how="inner", suffixes=['_1', '_2'])

        """
        To filter out people who are already infected
        """
        df = df.loc[~df["person_id_1"].isin(self.infected_set)]
        df = df.loc[df["person_id_1"] != df["person_id_2"]]

        # TODO: Integrate this with the family/person and multiply to generate joint probabilities
        """
        To generate the probabilities of people wearing masks
        """
        df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([0])), "mask_condition_1"] = np.random.uniform(0, 1)
        df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([1])), "mask_condition_1"] = np.random.uniform(0, 1)
        df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([0])), "mask_condition_1"] = np.random.uniform(0, 1)

        """
        To check the probabilities of people for different activities
        """
        df.loc[(df["in_school_1"].isin([1]) & df["in_school_2"].isin([1])) & (df["school_type_1"] == df["school_type_2"]), "school_meetup_1"] = np.random.uniform(0, 1)
        df.loc[(df["attend_work_1"].isin([1]) & df["attend_work_2"].isin([1])) & (df["work_type_1"] == df["work_type_2"]), "work_meetup_1"] = np.random.uniform(0, 1)
        df.loc[(df["dog_walk_1"].isin([1]) & df["dog_walk_2"].isin([1])) & (df["dog_walk_type_1"] == df["dog_walk_type_2"]), "dog_walk_meetup_1"] = np.random.uniform(0, 1)
        df.loc[(df["prayer_group_1"].isin([1]) & df["prayer_group_2"].isin([1])) & (df["prayer_group_type_1"] == df["prayer_group_type_2"]), "prayer_meetup_1"] = np.random.uniform(0, 1)
        df.loc[(df["play_sports_1"].isin([1]) & df["play_sports_2"].isin([1])) & (df["sports_type_1"] == df["sports_type_2"]), "sports_meetup_1"] = np.random.uniform(0, 1)
        df.loc[(df["volunteering_1"].isin([1]) & df["volunteering_2"].isin([1])) & (df["volunteering_type_1"] == df["volunteering_type_2"]), "volunteer_meetup_1"] = np.random.uniform(0, 1)
        df.loc[(df["grocery_visitor_1"].isin([1]) & df["grocery_visitor_2"].isin([1])) & (df["grocery_store_type_1"] == df["grocery_store_type_2"]), "grocery_meetup_1"] = np.random.uniform(0, 1)
        df.loc[(df["gas_visitor_1"].isin([1]) & df["gas_visitor_2"].isin([1])) & (df["gas_store_type_1"] == df["gas_store_type_2"]), "gas_meetup_1"] = np.random.uniform(0, 1)

        """
        To calculate average contact rate
        """
        school_meetup = df.loc[df["school_meetup_1"] > 0]
        work_meetup = df.loc[df["work_meetup_1"] > 0]
        dog_walk_meetup = df.loc[df["dog_walk_meetup_1"] > 0]
        prayer_meetup = df.loc[df["prayer_meetup_1"] > 0]
        sports_meetup = df.loc[df["sports_meetup_1"] > 0]
        volunteer_meetup = df.loc[df["volunteer_meetup_1"] > 0]
        grocery_meetup = df.loc[df["grocery_meetup_1"] > 0]
        gas_meetup = df.loc[df["gas_meetup_1"] > 0]
        self.contact.append(len(set(school_meetup["person_id_1"]).union(set(work_meetup["person_id_1"]), set(dog_walk_meetup["person_id_1"]), set(prayer_meetup["person_id_1"]),
                            set(sports_meetup["person_id_1"]), set(volunteer_meetup["person_id_1"]), set(grocery_meetup["person_id_1"]), set(gas_meetup["person_id_1"]))))

        # TODO: Implement this part

        """
        To filter data from the dataframe for mask conditions based on the probabilities given.
        """
        df_mask_90 = df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([1])) & (df["mask_condition_1"] >= self.mask_11)]
        df_mask_70 = df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([0])) & (df["mask_condition_1"] >= self.mask_10)]
        df_mask_50 = df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([1])) & (df["mask_condition_1"] >= self.mask_01)]
        df_mask_30 = df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([0])) & (df["mask_condition_1"] >= self.mask_00)]
        df = None

        df_res = pd.concat([df_mask_90, df_mask_70, df_mask_50, df_mask_30], axis=0)

        """
        To filter the dataframe based on the people who match the activities' criteria.
        """
        df_res = df_res.loc[((df_res["in_school_1"].isin([1]) & df_res["in_school_2"].isin([1])) & (df_res["school_type_1"] == df_res["school_type_2"]) & (df_res["school_meetup_1"] >= self.school_prob)) |
                            ((df_res["attend_work_1"].isin([1]) & df_res["attend_work_2"].isin([1])) & (df_res["work_type_1"] == df_res["work_type_2"]) & (df_res["work_meetup_1"] >= self.work_prob)) |
                            ((df_res["dog_walk_1"].isin([1]) & df_res["dog_walk_2"].isin([1])) & (df_res["dog_walk_type_1"] == df_res["dog_walk_type_2"]) & (df_res["dog_walk_meetup_1"] >= self.dog_walk_prob)) |
                            ((df_res["prayer_group_1"].isin([1]) & df_res["prayer_group_2"].isin([1])) & (df_res["prayer_group_type_1"] == df_res["prayer_group_type_2"]) & (df_res["prayer_meetup_1"] >= self.prayer_group_prob)) |
                            ((df_res["play_sports_1"].isin([1]) & df_res["play_sports_2"].isin([1])) & (df_res["sports_type_1"] == df_res["sports_type_2"]) & (df_res["sports_meetup_1"] >= self.play_sports_prob)) |
                            ((df_res["volunteering_1"].isin([1]) & df_res["volunteering_2"].isin([1])) & (df_res["volunteering_type_1"] == df_res["volunteering_type_2"]) & (df_res["volunteer_meetup_1"] >= self.volunteer_prob)) |
                            ((df_res["grocery_visitor_1"].isin([1]) & df_res["grocery_visitor_2"].isin([1])) & (df_res["grocery_store_type_1"] == df_res["grocery_store_type_2"]) & (df_res["grocery_meetup_1"] >= self.grocery_prob)) |
                            ((df_res["gas_visitor_1"].isin([1]) & df_res["gas_visitor_2"].isin([1])) & (df_res["gas_store_type_1"] == df_res["gas_store_type_2"]) & (df_res["gas_meetup_1"] >= self.gas_prob))]

        df_res = df_res.loc[~df_res["person_id_1"].isin(self.infected_set)]
        set_of_exposed_people = set(df_res["person_id_1"])
        df_res = None
        return set_of_exposed_people


if __name__ == '__main__':
    start = time.time()
    sim = Simulate()
    fully_merged_data = pd.read_csv("../Results/merged.csv", dtype={"work_type": "string", "volunteering_type": "string", "prayer_group_type": "string", "sports_type": "string", "dog_walk_type": "string"})
    sim.generate_dates()
    fully_merged_data["mask_condition_1"] = 0
    fully_merged_data["school_meetup_1"] = 0
    fully_merged_data["work_meetup_1"] = 0
    fully_merged_data["dog_walk_meetup_1"] = 0
    fully_merged_data["prayer_meetup_1"] = 0
    fully_merged_data["sports_meetup_1"] = 0
    fully_merged_data["volunteer_meetup_1"] = 0
    fully_merged_data["grocery_meetup_1"] = 0
    fully_merged_data["gas_meetup_1"] = 0
    fully_merged_data_df = sim.initialize_infections(fully_merged_data)
    fully_merged_data_df = sim.start_simulations(fully_merged_data_df)
    with open('../Results/new_infection_date_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.new_infection_date_dict))
    with open('../Results/recovery_date_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.recovery_date_dict))
    with open('../Results/susceptible_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(sim.susceptible_dict))
    print(sum(sim.contact)/len(sim.contact))
    fully_merged_data_df.to_csv("../Results/simulated_df.csv", index=False)
    print("Total time taken:", (time.time() - start)/60)