import collections
import json
import math
import sys
import time
import pandas as pd
import numpy as np
from numpy import random
from datetime import timedelta, datetime
pd.options.mode.chained_assignment = None
import random
low_memory=False


class Birthdays:
    def __init__(self):
        """
        All the important parameters and global variables are introduced and declared here
        Many probabilities that are to be satisfied in order to contract the virus are also mentioned here
        """
        self.children_not_toddlers = set([age for age in range(5, 19)])
        self.children_friends_list = []
        self.friends_set_index = dict()
        self.day_list = []
        self.new_infection_date_dict = collections.Counter()
        self.recovery_date_dict = collections.Counter()
        self.susceptible_dict = collections.Counter()
        self.quarantined_dates_info = collections.defaultdict(set)
        self.contagious_dates_info = collections.defaultdict(set)
        self.death_dict = collections.Counter()
        self.infected_set = set()
        self.counter_date = dict()
        self.probability_list = [0.1 * x for x in range(1, 10)]
        self.recovery_time_probability = [random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 28), random.randint(2, 28), random.randint(2, 28),
                                          random.randint(2, 28), random.randint(2, 35), random.randint(2, 42)]
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
        self.prob_death_gt4_weeks = 0.1
        self.day_counter = 0
        # Probability for picking the number of people to be infected in the family
        self.family_people_picker = [(0.1 * x) for x in range(4, 8)]
        self.simulator_count = 0
        self.date_done = set()

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

    def create_friends(self, people_df):
        """
        To create the sets of friends of children
        :param people_df: The people dataframe
        :return: None
        """
        children = people_df.loc[people_df["age"].isin(self.children_not_toddlers)]
        list_of_children = list(children["person_id"])
        _friends = set()
        counter = 0
        for child in list_of_children:
            if counter < 20:
                # If here, the friends are added to the set
                _friends.add(child)
                counter += 1
            else:
                # If here, the last friend will be added to the set of friends and a new friends group is to be created.
                _friends.add(child)
                self.children_friends_list.append(_friends)
                _friends = set()
                counter = 0

        for index, friend_set in enumerate(self.children_friends_list):
            # To have a list that contains the index of the friends' group for each child.
            for each_person in friend_set:
                self.friends_set_index[each_person] = index

    def initialize_infections(self, merged_df, children_df):
        """
        This function initializes the infection for 5 random people. This function also defines the incubation period,
        infection date, contagious period, recovery date for these 5 people.
        :param merged_df: The dataset with date, person and family data joined together
        :param children_df: The dataset that is a subset of merged_df which with only children in it
        :return: The updated people_df dataframe
        """
        _day = None
        for day in self.day_list:
            birth_day_kids_df = children_df.loc[(children_df["bir_day"] == day.day) & (children_df["bir_month"] == day.month)]
            birth_day_kids_df = birth_day_kids_df.loc[children_df["date"] == str(day)]
            self.day_counter += 1
            _day = day
            if birth_day_kids_df.shape[0] > 0:
                break

        if birth_day_kids_df.iloc[0]["date"] not in self.death_dict:
            self.death_dict[birth_day_kids_df.iloc[0]["date"]] = 0
        for index, bd_kid in birth_day_kids_df.iterrows():
            self.new_infection_date_dict[str(_day)] += 1
            """An incubation period is randomly chosen between 2 and 15 days"""
            incubation_period = random.randint(5, 15)
            # incubation_period = 10
            self.infected_set.add(bd_kid["person_id"])
            exposed_date = datetime.strptime(bd_kid["date"], '%Y-%m-%d').date()
            infection_date = exposed_date + timedelta(days=incubation_period)
            """The dates when the person who is infected spreads the virus are calculated using the exposed and the incubation periods"""
            contagious_date = infection_date - timedelta(days=2)
            range_of_contagious_dates = [str(contagious_date + timedelta(days=x)) for x in range((infection_date - contagious_date).days)]
            merged_df.loc[(merged_df["person_id"] == bd_kid["person_id"]) & (merged_df["date"] == str(exposed_date)), ["exposed", "quarantined", "new_infection"]] = [1, 0, 1]
            merged_df.loc[(merged_df["person_id"] == bd_kid["person_id"]) & (merged_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [1, 0, 0, 1]
            merged_df.loc[(merged_df["person_id"] == bd_kid["person_id"]) & (merged_df["date"] == str(infection_date)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
            """The recovery date is calculated based on the recovery time that has been generated using random values."""
            recovery_time = int(random.choice(self.recovery_time_probability))
            date_of_recovery = infection_date + timedelta(days=recovery_time)
            self.recovery_date_dict[str(date_of_recovery)] += 1
            range_of_quarantined_dates = set([str(infection_date + timedelta(days=x)) for x in range((date_of_recovery - infection_date).days)])
            merged_df.loc[(merged_df["person_id"] == bd_kid["person_id"]) & (merged_df["date"].isin(range_of_quarantined_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
        merged_df = merged_df.replace(np.nan, 0)
        self.counter_date[str(_day)] = len(self.infected_set)
        self.susceptible_dict[str(_day)] = int(sys.argv[1]) - len(self.infected_set)
        return merged_df

    def initiate_birthdays(self, altered_merged_df, children_df, people_df):
        contagious_queue = collections.deque()
        for day in self.day_list:
            print(day)
            counter = 0
            self.date_done.add(str(day))
            self.day_counter += 1
            contagious_people_pot = altered_merged_df.loc[(altered_merged_df["date"] == str(day)) & (altered_merged_df["contagious"].isin([1]))]
            # Calculate who all had birthdays that day and if they are not in infected set
            bday_kids = children_df.loc[(altered_merged_df["bir_day"] == day.day) & (altered_merged_df["bir_month"] == day.month)]
            unique_kids_df = bday_kids.loc[bday_kids["date"] == str(day)]
            kids_at_risk_set = set(contagious_people_pot.loc[contagious_people_pot["age"].isin(self.children_not_toddlers)]["person_id"])
            # Calculate who all came to the party
            # kids_at_risk_set = set(unique_kids_df["person_id"])
            intersected_set = set.intersection(kids_at_risk_set, set(unique_kids_df["person_id"]))
            if len(intersected_set) > 0:
                for kid in kids_at_risk_set:
                    if kid in self.friends_set_index:
                        kids_at_risk_set = set.union(kids_at_risk_set, self.children_friends_list[self.friends_set_index[kid]])
            # Randomly select a good population to be added to the bday_infections_pot - select only those who is not in the infected set
            contagious_kids_pot = children_df.loc[(~children_df["person_id"].isin(self.infected_set)) & (children_df["person_id"].isin(kids_at_risk_set)) & (children_df["date"] == str(day))]
            # sample_size = int(contagious_kids_pot.shape[0] * random_selection_infected)
            sample_size = int(contagious_kids_pot.shape[0])
            contagious_kids_pot = contagious_kids_pot.sample(n=sample_size)
            # Add both the contagious people and the contagious kids to the queue
            if not contagious_people_pot.empty:
                contagious_queue.append(contagious_people_pot)
            if not contagious_kids_pot.empty:
                family_ids = set(contagious_kids_pot["fam_id"])
                other_person_ids = set(people_df.loc[(people_df["fam_id"].isin(family_ids)) & (~people_df["person_id"].isin(set(contagious_kids_pot["person_id"])))]["person_id"])
                inf_family_size = int(math.ceil(len(other_person_ids) * random.choice(self.family_people_picker)))
                inf_family = random.sample(list(other_person_ids), inf_family_size)
                self.infected_set = set.union(self.infected_set, inf_family, set(contagious_kids_pot["person_id"]))
                family_contact_df = altered_merged_df.loc[(~altered_merged_df["person_id"].isin(self.infected_set)) & (altered_merged_df["person_id"].isin(inf_family)) & (altered_merged_df["date"] == str(day))]
                contagious_queue.append(family_contact_df)
                contagious_queue.append(contagious_kids_pot)
                altered_merged_df, counter = self.calculate_infection_metrics(day, counter, contagious_kids_pot, altered_merged_df)

            while contagious_queue:
                # If here, it is to spread the virus by checking the contact between the infected and the healthy.
                cont_person = contagious_queue.popleft()
                # Get all the people who are contagious on this day
                cont_person_df = altered_merged_df.loc[(altered_merged_df["person_id"].isin(set(cont_person["person_id"]))) & (altered_merged_df["date"] == str(day)) & (altered_merged_df["contagious"].isin([1]))]
                # Get all people who are not infected and are potential victims on the current day
                merged_without_infected = altered_merged_df.loc[~altered_merged_df["person_id"].isin(self.infected_set) & (altered_merged_df["date"] == str(day)) & (~altered_merged_df["contagious"].isin([1]))]
                newly_exposed_set = self.virus_check(cont_person_df, merged_without_infected)
                # New trial starts
                # newly_exposed_set = newly_exposed_set.difference(self.infected_set)
                self.simulator_count += len(newly_exposed_set)
                # New trial ends
                self.infected_set = set.union(self.infected_set, newly_exposed_set)
                newly_exposed_df = altered_merged_df.loc[(altered_merged_df["person_id"].isin(newly_exposed_set)) & (altered_merged_df["date"] == str(day))]
                altered_merged_df, counter = self.calculate_infection_metrics(day, counter, newly_exposed_df, altered_merged_df)
                newly_contagious = altered_merged_df.loc[(~altered_merged_df["person_id"].isin(self.infected_set)) & (altered_merged_df["contagious"].isin([1])) & (altered_merged_df["date"].isin([day]))]

                if not newly_contagious.empty:
                    contagious_queue.append(newly_contagious)
            # print(counter)
            self.counter_date[str(day)] = len(self.infected_set)
            self.susceptible_dict[str(day)] = int(sys.argv[1]) - len(self.infected_set)
            print(len(self.infected_set))
            print("next day")
        return altered_merged_df

    def calculate_infection_metrics(self, day, counter, newly_exposed_df, altered_merged_df):
        for index, infected in newly_exposed_df.iterrows():
            counter += 1
            # incubation_period = 10
            incubation_period = random.randint(5, 15)
            exposed_date = day
            altered_merged_df.at[index, "new_infection"] = 1
            infection_date = exposed_date + timedelta(days=incubation_period)
            contagious_date = infection_date - timedelta(days=2)
            range_of_contagious_dates = set([contagious_date + timedelta(days=x) for x in range((infection_date - contagious_date).days)])
            self.new_infection_date_dict[str(day)] += 1
            self.contagious_dates_info[infected["person_id"]] = range_of_contagious_dates
            contagious_date_index = [d for d in range(index + incubation_period - 2, index + incubation_period)]
            # Assign the contagious property on the mentioned dates
            for c_date_idx in contagious_date_index:
                altered_merged_df.at[c_date_idx, "contagious"] = 1
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

    def dob_split(self, birthday_df):
        """
        To extract the day and month fields from the birthday field
        :param birthday_df: The merged dataframe
        :return: The dataframe with the month and day fields extracted
        """
        birthday_df["bir_day"] = pd.to_datetime(birthday_df["dob"]).dt.day
        birthday_df["bir_month"] = pd.to_datetime(birthday_df["dob"]).dt.month
        return birthday_df


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: python3 birthdays_v3.py [Argument_1]")
        print("     Argument_1: Number of people in the population")
        sys.exit()
    start = time.time()
    people_df = pd.read_csv("../Results/Data/people.csv")
    bir = Birthdays()
    bir.create_friends(people_df)
    merged_df = pd.read_csv("../Results/Data/merged.csv")
    altered_merged_df = bir.dob_split(merged_df)
    children_df = altered_merged_df.loc[altered_merged_df["age"].isin(bir.children_not_toddlers)]
    bir.generate_dates()
    altered_merged_df = bir.initialize_infections(altered_merged_df, children_df)
    final_df = bir.initiate_birthdays(altered_merged_df, children_df, people_df)
    print("The number of infected people are:", len(bir.infected_set))
    print("The simulator count is:", bir.simulator_count)
    print(bir.counter_date)
    print(sum(list(bir.counter_date.values())))
    with open('../Results/Data/Birthdays/infections.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.counter_date))
    with open('../Results/Data/Birthdays/new_infection_date_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.new_infection_date_dict))
    with open('../Results/Data/Birthdays/recovery_date_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.recovery_date_dict))
    with open('../Results/Data/Birthdays/susceptible_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.susceptible_dict))
    with open('../Results/Data/Birthdays/death_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.death_dict))
    final_df.to_csv("../Results/Data/Birthdays/birthday_final.csv", index=False)
    print("Total time taken:", (time.time() - start) / 60)