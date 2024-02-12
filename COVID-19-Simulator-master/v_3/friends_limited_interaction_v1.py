import collections
import json
import math
import sys
import time
import pandas as pd
from datetime import timedelta, datetime
import random
import numpy as np
low_memory=False

"""
This program is a simulator that simulates how a virus spreads across a community.
In this program, every week, a family meets another family randomly. 
In this program, the initial set of infections is assigned and the algorithm propagates the virus further.
The propagation is governed by probabilities provided by the users (This functionality is not implemented yet).

Author: Ravikiran Jois Yedur Prabhakar
Advisor: Dr. Thomas B. Kinsman
"""

class FriendsInteraction:
    def __init__(self):
        """
        This method is to introduce the several parameters and datastructures that are required to run the
        simulation.
        """
        random.seed(10)
        self.friends_list = []
        self.friends_set_index = dict()
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
        self.dict_of_people = collections.defaultdict(set)
        self.set_of_all_families = set()
        self.total_infections = 0
        self.mask_prob_equal = [1, 0]
        self.school_prob = 0.4
        self.work_prob = 0.4
        self.dog_walk_prob = 0.6
        self.prayer_group_prob = 0.5
        self.volunteer_prob = 0.6
        self.play_sports_prob = 0.6
        self.grocery_prob = 0.4
        self.gas_prob = 0.4
        self.mall_prob = 0.4
        # Left is healthy and not wearing mask - 0, Right is contagious - not wearing mask - 0
        self.mask_00 = 0.2
        # Left healthy and not wearing mask - 0, Right contagious - wearing mask - 1
        self.mask_01 = 0.6
        # Left healthy and wearing mask - 1, Right contagious - not wearing mask - 0
        self.mask_10 = 0.3
        # When both people wear mask - Left 1 and Right 1
        self.mask_11 = 0.9
        # Probability of the person being removed from the population if recovered between 2 and 4 weeks of infection.
        self.prob_death_4_weeks = 0.6
        # Probability of the person being removed from the population if recovered after 4 weeks of infection.
        self.prob_death_gt4_weeks = 0.2
        self.contact = []
        self.probability_list = [0.1 * x for x in range(1, 10)]
        self.weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        # Probability for picking the number of people to be infected in the family
        self.family_people_picker = [(0.1 * x) for x in range(4, 8)]
        self.simulator_count = 0
        self.date_done = set()
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

    def create_friends(self, family_df, person_df):
        """
        This method is to create the friends of families
        :param family_df: The family dataframe that contains information of the family unit
        :return: None
        """
        self.set_of_all_families = set(family_df["fam_id"])
        for index, person in person_df.iterrows():
            self.dict_of_people[person["fam_id"]].add(person["person_id"])
        # _friends = set()
        # counter = 0
        # for _fam in set_of_all_families:
        #     if counter < 4:
        #         # If here, the friends are added to the set
        #         _friends.add(_fam)
        #         counter += 1
        #     else:
        #         # If here, the last friend will be added to the set of friends and a new friends group is to be created.
        #         _friends.add(_fam)
        #         self.friends_list.append(_friends)
        #         _friends = set()
        #         counter = 0
        #
        # for index, friend_set in enumerate(self.friends_list):
        #     # To have a list that contains the index of the friends' group for each child.
        #     for each_person in friend_set:
        #         self.friends_set_index[each_person] = index

    def initialize_infections(self, merged_df):
        """
        This function initializes the infection for 5 random people. This function also defines the incubation period,
        infection date, contagious period, recovery date for these 5 people.
        :param merged_df: The dataset with date, person and family data joined together
        :return: The updated people_df dataframe
        """
        random_infected_df = merged_df.loc[(merged_df["date"] == str(datetime(2020, 1, 1).date())) & (merged_df["age"] > 4)].sample(n=10)
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
            merged_df.loc[(merged_df["person_id"] == infected["person_id"]) & (merged_df["date"] == str(exposed_date)), ["exposed", "quarantined", "new_infection"]] = [1, 0, 1]
            merged_df.loc[(merged_df["person_id"] == infected["person_id"]) & (merged_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [1, 0, 0, 1]
            merged_df.loc[(merged_df["person_id"] == infected["person_id"]) & (merged_df["date"] == str(infection_date)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
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
                merged_df.at[death_day_idx, "death"] = 1
            range_of_quarantined_dates = set([infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
            merged_df.loc[(merged_df["person_id"] == infected["person_id"]) & (merged_df["date"].isin(range_of_quarantined_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
        merged_df = merged_df.replace(np.nan, 0)
        self.counter_date[day] = len(self.infected_set)
        self.susceptible_dict[self.day_counter] = int(sys.argv[1]) - len(self.infected_set)
        return merged_df

    def join_tables(self, family_df, date_df):
        # Joining the date and the family table
        family_df["tmp"] = 1
        date_df["tmp"] = 1
        merged_df = pd.merge(family_df, date_df, on='tmp')
        del merged_df["tmp"]
        del family_df["tmp"]
        del date_df["tmp"]

        return merged_df

    def start_simulation(self, altered_merged_df, family_df, date_df, family_date_merged_df):
        contagious_queue = collections.deque()
        day_counter = 0
        week_counter = 1
        infected_people_df = pd.DataFrame(columns=altered_merged_df.columns)
        for day in self.day_list:
            print(day)
            self.date_done.add(str(day))
            counter = 0
            day_counter += 1
            if day_counter == 6:
                day_counter = 0
                week_counter += 1
                choose_day = random.choice(self.weekdays)
                # TODO: Insert a command line argument to choose how many families meet on this day (Replace 10 by sys arg)
                contagious_people = set(altered_merged_df.loc[(altered_merged_df["date"] == str(day)) & (altered_merged_df["day_of_week"] == choose_day) & altered_merged_df["contagious"].isin([1])]["person_id"])
                # families_on_day = family_date_merged_df.loc[(family_date_merged_df["day_of_week"] == choose_day) & (family_date_merged_df["week_no"] == week_counter)]
                # families_that_meet = random.sample(list(set(families_on_day["fam_id"])), 10)
                # Get families of these people and then, all the people in those families
                families_that_meet = set(altered_merged_df.loc[altered_merged_df["person_id"].isin(contagious_people)]["fam_id"])
                people_of_families = set()
                for fam in families_that_meet:
                    fam_friend = random.choice(list(self.dict_of_people.keys()))
                    while fam_friend in families_that_meet:
                        fam_friend = random.choice(list(self.dict_of_people.keys()))
                    people_of_families = set.union(people_of_families, self.dict_of_people[fam], self.dict_of_people[fam_friend])
                people_of_families = people_of_families.difference(self.infected_set)
                size_of_infected = int(math.ceil(len(people_of_families) * random.choice(self.family_people_picker)))
                infected_people = random.sample(list(people_of_families), size_of_infected)
                infected_people_df = altered_merged_df.loc[(altered_merged_df["person_id"].isin(infected_people)) & (altered_merged_df["date"] == str(day))]

            # Getting the contagious people from the dataframe
            contagious_people_pot = altered_merged_df.loc[(altered_merged_df["date"] == str(day)) & (altered_merged_df["contagious"].isin([1]))]

            if not contagious_people_pot.empty:
                contagious_queue.append(contagious_people_pot)
                del contagious_people_pot
            if not infected_people_df.empty:
                altered_merged_df, counter = self.calculate_infection_metrics(day, counter, infected_people_df, altered_merged_df)
                contagious_queue.append(infected_people_df)
                # del infected_people_df

            while contagious_queue:
                # If here, it is to spread the virus by checking the contact between the infected and the healthy.
                cont_person = contagious_queue.popleft()
                # Get all the people who are contagious on this day
                cont_person_df = altered_merged_df.loc[(altered_merged_df["person_id"].isin(set(cont_person["person_id"]))) & (altered_merged_df["date"] == str(day)) & (altered_merged_df["contagious"].isin([1]))]
                # Get all people who are not infected and are potential victims on the current day
                merged_without_infected = altered_merged_df.loc[~altered_merged_df["person_id"].isin(self.infected_set) & (altered_merged_df["date"] == str(day)) & (~altered_merged_df["contagious"].isin([1]))]
                newly_exposed_set = self.virus_check(cont_person_df, merged_without_infected)
                # New trial starts
                newly_exposed_set = newly_exposed_set.difference(self.infected_set)
                self.simulator_count += len(newly_exposed_set)
                # New trial ends
                self.infected_set = set.union(self.infected_set, newly_exposed_set)
                newly_exposed_df = altered_merged_df.loc[(altered_merged_df["person_id"].isin(newly_exposed_set)) & (altered_merged_df["date"] == str(day))]
                altered_merged_df, counter = self.calculate_infection_metrics(day, counter, newly_exposed_df, altered_merged_df)
                newly_contagious = altered_merged_df.loc[(~altered_merged_df["person_id"].isin(self.infected_set)) & (altered_merged_df["contagious"].isin([1])) & (altered_merged_df["date"].isin([day]))]

                if not newly_contagious.empty:
                    contagious_queue.append(newly_contagious)
                    del newly_contagious
            # print(counter)
            print(len(self.infected_set))
            self.counter_date[str(day)] = len(self.infected_set)
            self.susceptible_dict[str(day)] = int(sys.argv[1]) - len(self.infected_set)
            print("next day")

        return altered_merged_df


    def calculate_infection_metrics(self, day, counter, infected_people_df, altered_merged_df):
        for index, infected in infected_people_df.iterrows():
            counter += 1
            # incubation_period = 10
            incubation_period = random.randint(5, 15)
            exposed_date = day
            altered_merged_df.at[index, "new_infection"] = 1
            infection_date = exposed_date + timedelta(days=incubation_period)
            contagious_date = infection_date - timedelta(days=2)
            range_of_contagious_dates = set(
                [contagious_date + timedelta(days=x) for x in range((infection_date - contagious_date).days)])
            self.new_infection_date_dict[str(day)] += 1
            self.contagious_dates_info[infected["person_id"]] = range_of_contagious_dates
            contagious_date_index = [d for d in range(index + incubation_period - 2, index + incubation_period)]
            # Assign the contagious property on the mentioned dates
            for c_date_idx in contagious_date_index:
                altered_merged_df.at[c_date_idx, "contagious"] = 1
            recovery_time = int(random.choice(self.recovery_time_probability))
            date_of_recovery = infection_date + timedelta(days=recovery_time)
            self.recovery_date_dict[str(date_of_recovery)] += 1
            range_of_recovery_dates = set(
                [infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
            prob_death = random.choice(self.probability_list)
            if (14 < recovery_time < 28 and prob_death > self.prob_death_4_weeks) or (
                    recovery_time > 28 and prob_death > self.prob_death_gt4_weeks):
                # If here, it is to check the date of removal from the population.
                if str(date_of_recovery) not in self.death_dict:
                    self.death_dict[str(date_of_recovery)] = 1
                else:
                    self.death_dict[str(date_of_recovery)] += 1
                death_day_idx = index + incubation_period + recovery_time
                altered_merged_df.at[death_day_idx, "death"] = 1
            if recovery_time < 14:
                # If here, the person is not to be removed from the population and will successfully recover
                recovery_day_idx = index + incubation_period + recovery_time
                altered_merged_df.at[recovery_day_idx, "recovery"] = 1
            self.quarantined_dates_info[infected["person_id"]] = range_of_recovery_dates
        return altered_merged_df, counter

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
        merged_df["school_meetup_1"] = merged_df["school_exposure_1"] * merged_df["school_exposure_2"]
        merged_df["work_meetup_1"] = merged_df["work_exposure_1"] * merged_df["work_exposure_2"]
        merged_df["dog_walk_meetup_1"] = merged_df["dog_walk_exposure_1"] * merged_df["dog_walk_exposure_2"]
        merged_df["prayer_meetup_1"] = merged_df["prayer_group_exposure_1"] * merged_df["prayer_group_exposure_2"]
        merged_df["sports_meetup_1"] = merged_df["sports_exposure_1"] * merged_df["sports_exposure_2"]
        merged_df["volunteer_meetup_1"] = merged_df["volunteering_exposure_1"] * merged_df["volunteering_exposure_2"]
        merged_df["grocery_meetup_1"] = merged_df["grocery_exposure_1"] * merged_df["grocery_exposure_2"]
        merged_df["gas_meetup_1"] = merged_df["gas_exposure_1"] * merged_df["gas_exposure_2"]
        merged_df["mall_meetup_1"] = merged_df["mall_exposure_1"] * merged_df["mall_exposure_2"]

        # To filter data from the dataframe for mask conditions based on the probabilities given. This is a temporary dataframe
        merged_filtered_df = pd.concat([merged_df.loc[(merged_df["mask_1"].isin([1])) & (merged_df["mask_2"].isin([1])) & (merged_df["mask_condition_1"] >= self.mask_11)],
                            merged_df.loc[(merged_df["mask_1"].isin([1])) & (merged_df["mask_2"].isin([0])) & (merged_df["mask_condition_1"] >= self.mask_10)],
                            merged_df.loc[(merged_df["mask_1"].isin([0])) & (merged_df["mask_2"].isin([1])) & (merged_df["mask_condition_1"] >= self.mask_01)],
                            merged_df.loc[(merged_df["mask_1"].isin([0])) & (merged_df["mask_2"].isin([0])) & (merged_df["mask_condition_1"] >= self.mask_00)]], axis=0)

        del merged_df

        # To filter the dataframe based on the people who match the activities' criteria.
        merged_filtered_df = merged_filtered_df.loc[((merged_filtered_df["in_school_1"].isin([1]) & merged_filtered_df["in_school_2"].isin([1])) & (merged_filtered_df["school_type_1"] == merged_filtered_df["school_type_2"]) & (merged_filtered_df["school_meetup_1"] >= self.school_prob)) |
                            ((merged_filtered_df["attend_work_1"].isin([1]) & merged_filtered_df["attend_work_2"].isin([1])) & (merged_filtered_df["work_type_1"] == merged_filtered_df["work_type_2"]) & merged_filtered_df["work_meetup_1"] >= self.work_prob) |
                            ((merged_filtered_df["dog_walk_1"].isin([1]) & merged_filtered_df["dog_walk_2"].isin([1])) & (merged_filtered_df["dog_walk_type_1"] == merged_filtered_df["dog_walk_type_2"]) & (merged_filtered_df["dog_walk_meetup_1"] >= self.dog_walk_prob)) |
                            ((merged_filtered_df["prayer_group_1"].isin([1]) & merged_filtered_df["prayer_group_2"].isin([1])) & (merged_filtered_df["prayer_group_type_1"] == merged_filtered_df["prayer_group_type_2"]) & (merged_filtered_df["prayer_meetup_1"] > self.prayer_group_prob)) |
                            ((merged_filtered_df["play_sports_1"].isin([1]) & merged_filtered_df["play_sports_2"].isin([1])) & (merged_filtered_df["sports_type_1"] == merged_filtered_df["sports_type_2"]) & (merged_filtered_df["sports_meetup_1"] >= self.play_sports_prob)) |
                            ((merged_filtered_df["volunteering_1"].isin([1]) & merged_filtered_df["volunteering_2"].isin([1])) & (merged_filtered_df["volunteering_type_1"] == merged_filtered_df["volunteering_type_2"]) & (merged_filtered_df["volunteer_meetup_1"] >= self.volunteer_prob)) |
                            ((merged_filtered_df["grocery_visitor_1"].isin([1]) & merged_filtered_df["grocery_visitor_2"].isin([1])) & (merged_filtered_df["grocery_store_type_1"] == merged_filtered_df["grocery_store_type_2"]) & (merged_filtered_df["grocery_meetup_1"] >= self.grocery_prob)) |
                            ((merged_filtered_df["gas_visitor_1"].isin([1]) & merged_filtered_df["gas_visitor_2"].isin([1])) & (merged_filtered_df["gas_store_type_1"] == merged_filtered_df["gas_store_type_2"]) & (merged_filtered_df["gas_meetup_1"] >= self.gas_prob))]

        set_of_exposed_people = set(merged_filtered_df["person_id_1"])
        del merged_filtered_df
        return set_of_exposed_people


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: python3 friends_limited_interaction_v1.py [Argument_1]")
        print("     Argument_1: Number of people in the population")
        sys.exit()
    start = time.time()
    frnd = FriendsInteraction()
    frnd.generate_dates()
    people_df = pd.read_csv("../Results/Data/people.csv")
    family_df = pd.read_csv("../Results/Data/family.csv")
    date_df = pd.read_csv("../Results/Data/dates.csv")
    merged_df = pd.read_csv("../Results/Data/merged.csv")
    frnd.create_friends(family_df, people_df)
    altered_merged_df = frnd.initialize_infections(merged_df)
    family_date_merged_df = frnd.join_tables(family_df, date_df)
    altered_merged_df = frnd.start_simulation(altered_merged_df, family_df, date_df, family_date_merged_df)
    print("The simulator count is:", frnd.simulator_count)
    print("The number of infected people are:", len(frnd.infected_set))
    print(frnd.counter_date)
    with open('../Results/Data/Friends_Ltd/infections.json', 'w') as convert_file:
        convert_file.write(json.dumps(frnd.counter_date))
    with open('../Results/Data/Friends_Ltd/new_infection_date_friends_ltd_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(frnd.new_infection_date_dict))
    with open('../Results/Data/Friends_Ltd/recovery_date_friends_ltd_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(frnd.recovery_date_dict))
    with open('../Results/Data/Friends_Ltd/susceptible_friends_ltd_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(frnd.susceptible_dict))
    with open('../Results/Data/Friends_Ltd/death_friends_ltd_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(frnd.death_dict))
    altered_merged_df.to_csv("../Results/Data/Friends_Ltd/friends_ltd_df.csv", index=False)

    print("Time taken is:", (time.time() - start)/60)