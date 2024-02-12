import collections
import json
import pandas as pd
import numpy as np
from networkx.generators.random_graphs import erdos_renyi_graph
low_memory=False
import networkx as nx
import matplotlib.pyplot as plt
from numpy import random
from datetime import timedelta, datetime
pd.options.mode.chained_assignment = None
import random


class Birthdays:
    def __init__(self):
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
        self.probability_list = [0.1 * x for x in range(1, 10)]
        self.recovery_time_probability = [random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 14), random.randint(2, 14), random.randint(2, 14),
                                          random.randint(2, 28), random.randint(2, 28), random.randint(2, 28),
                                          random.randint(2, 28), random.randint(2, 35), random.randint(2, 42)]
        # self.school_prob = 0.7
        # self.work_prob = 0.7
        # self.dog_walk_prob = 0.7
        # self.prayer_group_prob = 0.6
        # self.volunteer_prob = 0.6
        # self.play_sports_prob = 0.6
        # self.grocery_prob = 0.6
        # self.gas_prob = 0.6
        # self.mall_prob = 0.6
        # self.mask_00 = 0.2
        # self.mask_01 = 0.6
        # self.mask_10 = 0.3
        # self.mask_11 = 0.9
        # self.prob_death_4_weeks = 0.6
        # self.prob_death_gt4_weeks = 0.2
        self.school_prob = 0.5
        self.work_prob = 0.5
        self.dog_walk_prob = 0.5
        self.prayer_group_prob = 0.5
        self.volunteer_prob = 0.5
        self.play_sports_prob = 0.5
        self.grocery_prob = 0.5
        self.gas_prob = 0.5
        self.mall_prob = 0.5
        self.mask_00 = 0.1
        self.mask_01 = 0.6
        self.mask_10 = 0.3
        self.mask_11 = 0.8
        self.prob_death_4_weeks = 0.4
        self.prob_death_gt4_weeks = 0.1
        self.day_counter = 0

    def generate_dates(self):
        """
        The method generates the dates for the simulation and adds it to a list
        :return: None
        """
        start_date = datetime(2020, 1, 1).date()
        end_date = datetime(2020, 12, 31).date()
        delta_dates = end_date - start_date
        for i in range(delta_dates.days + 1):
            self.day_list.append(start_date + timedelta(days=i))

    def create_friends(self, people_df):
        children = people_df.loc[people_df["age"].isin(self.children_not_toddlers)]
        list_of_children = list(children["person_id"])
        _friends = set()
        counter = 0
        for child in list_of_children:
            if counter < 20:
                _friends.add(child)
                counter += 1
            else:
                _friends.add(child)
                self.children_friends_list.append(_friends)
                _friends = set()
                counter = 0

        for index, friend_set in enumerate(self.children_friends_list):
            for each_person in friend_set:
                self.friends_set_index[each_person] = index

    def initialize_infections(self, people_df):
        """
        This function initializes the infection for 5 random people. This function also defines the incubation period,
        infection date, contagious period, recovery date for these 5 people.
        :param people_df: The dataset with date, person and family data joined together
        :return: The updated people_df dataframe
        """
        for day in self.day_list:
            birth_day_kids_df = children_df.loc[(children_df["bir_day"] == day.day) & (children_df["bir_month"] == day.month)]
            birth_day_kids_df = birth_day_kids_df.loc[children_df["date"] == str(day)]
            if birth_day_kids_df.shape[0] > 0:
                break
        self.day_counter = 1
        if birth_day_kids_df.iloc[0]["date"] not in self.death_dict:
            self.death_dict[birth_day_kids_df.iloc[0]["date"]] = 0
        for index, bd_kid in birth_day_kids_df.iterrows():
            self.new_infection_date_dict[self.day_counter] += 1
            """An incubation period is randomly chosen between 2 and 15 days"""
            incubation_period = random.randint(5, 15)
            self.infected_set.add(bd_kid["person_id"])
            exposed_date = datetime.strptime(bd_kid["date"], '%Y-%m-%d').date()
            infection_date = exposed_date + timedelta(days=incubation_period)
            """The dates when the person who is infected spreads the virus are calculated using the exposed and the incubation periods"""
            contagious_date = infection_date - timedelta(days=2)
            range_of_contagious_dates = [str(contagious_date + timedelta(days=x)) for x in range((infection_date - contagious_date).days)]
            people_df.loc[(people_df["person_id"] == bd_kid["person_id"]) & (people_df["date"] == str(exposed_date)), ["exposed", "quarantined", "new_infection"]] = [1, 0, 1]
            people_df.loc[(people_df["person_id"] == bd_kid["person_id"]) & (people_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [1, 0, 0, 1]
            people_df.loc[(people_df["person_id"] == bd_kid["person_id"]) & (people_df["date"] == str(infection_date)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
            """The recovery date is calculated based on the recovery time that has been generated using random valurs."""
            recovery_time = int(random.choice(self.recovery_time_probability))
            date_of_recovery = infection_date + timedelta(days=recovery_time)
            self.recovery_date_dict[str(date_of_recovery)] += 1
            range_of_contagious_dates = set([infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
            people_df.loc[(people_df["person_id"] == bd_kid["person_id"]) & (people_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
        people_df = people_df.replace(np.nan, 0)
        self.susceptible_dict[self.day_counter] = 10000 - len(self.infected_set)
        return people_df



        # random_infected_df = people_df.loc[people_df["age"].isin(self.children_not_toddlers)].sample(n=5)
        # self.day_counter = 1
        # if str(datetime(2020, 1, 1).date()) not in self.death_dict:
        #     self.death_dict[str(datetime(2020, 1, 1).date())] = 0
        # for index, infected in random_infected_df.iterrows():
        #     self.new_infection_date_dict[self.day_counter] += 1
        #     """An incubation period is randomly chosen between 2 and 15 days"""
        #     incubation_period = random.randint(5, 15)
        #     self.infected_set.add(infected["person_id"])
        #     exposed_date = datetime.strptime(infected["date"], '%Y-%m-%d').date()
        #     infection_date = exposed_date + timedelta(days=incubation_period)
        #     """The dates when the person who is infected spreads the virus are calculated using the exposed and the incubation periods"""
        #     contagious_date = infection_date - timedelta(days=2)
        #     range_of_contagious_dates = [str(contagious_date + timedelta(days=x)) for x in range((infection_date - contagious_date).days)]
        #     people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(exposed_date)), ["exposed", "quarantined", "new_infection"]] = [1, 0, 1]
        #     people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [1, 0, 0, 1]
        #     people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"] == str(infection_date)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
        #     """The recovery date is calculated based on the recovery time that has been generated using random valurs."""
        #     recovery_time = int(random.choice(self.recovery_time_probability))
        #     date_of_recovery = infection_date + timedelta(days=recovery_time)
        #     self.recovery_date_dict[str(date_of_recovery)] += 1
        #     prob_death = random.choice(self.probability_list)
        #     if (14 < recovery_time <= 28 and prob_death >= self.prob_death_4_weeks) or \
        #             (recovery_time > 28 and prob_death >= self.prob_death_gt4_weeks):
        #         if str(date_of_recovery) not in self.death_dict:
        #             self.death_dict[str(date_of_recovery)] = 1
        #         else:
        #             self.death_dict[str(date_of_recovery)] += 1
        #         death_day_idx = index + incubation_period + recovery_time
        #         people_df.at[death_day_idx, "death"] = 1
        #     range_of_contagious_dates = set([infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
        #     people_df.loc[(people_df["person_id"] == infected["person_id"]) & (people_df["date"].isin(range_of_contagious_dates)), ["exposed", "quarantined", "new_infection", "contagious"]] = [0, 1, 0, 0]
        # people_df = people_df.replace(np.nan, 0)
        # self.susceptible_dict[self.day_counter] = 10000 - len(self.infected_set)
        # return people_df

    # def initiate_birthdays(self, altered_merged_df, children_df):
    #     first_flag = False
        # for day in self.day_list:
            # Get all children who have birthdays on this day
            # Then, get each child's friends on that day
            # Have a probability that each child catches the virus (Say 0.4 - More than this number, they catch the virus)
            # These children will be put to the contagious queue.
            # After the kids, add the newly infected people from popping the queue (See simulator code for this)
            # Do the rest of the simulation like before
            # self.children_friends_list[self.friends_set_index[5613]] -> to get the group of children
            # birth_day_kids_df = children_df.loc[(children_df["bir_day"] == day.day) & (children_df["bir_month"] == day.month)]
            # unique_kids_df = birth_day_kids_df.drop_duplicates("person_id")
            # # Add unique_kids_df to the infected set
            # # Now get all friends of these kids
            # bday_kids = set(unique_kids_df["person_id"])
            # kids_at_risk = set(unique_kids_df["person_id"])
            # for kid in kids_at_risk:
            #     kids_at_risk = set.union(kids_at_risk, self.children_friends_list[self.friends_set_index[kid]])
            # if len(kids_at_risk) > 0 and not first_flag:
            #     altered_merged_df.loc[altered_merged_df["person_id"].isin(bday_kids) & altered_merged_df["date"] == str(day), ""]
            #     first_flag = True
            # if it is the first day when the kids at risk > 0: then randomly make 10 people infected from the kids_at_risk set
                # Make them contagious and calculate the infection scenario - initial infectors
            # Get all the friends in the birthdays. Make about 70% of them to the infected set
            # Calculate the infection scenario for the friends
            # Get all people with contagious = 1
            # Add them all to queue
            # Pop from queue
            # While queue:
            #   Call the virus_check algorithm
            #   Calculate the contagiousness


    def initiate_birthdays(self, altered_merged_df, children_df):
        first_flag = False
        contagious_queue = collections.deque()
        for day in self.day_list:
            print(day)
            counter = 0
            self.day_counter += 1
            contagious_people_pot = altered_merged_df.loc[(altered_merged_df["date"] == str(day)) & (altered_merged_df["contagious"].isin([1]))]
            # Calculate who all had birthdays that day and if they are not in infected set
            bday_kids = altered_merged_df.loc[(altered_merged_df["bir_day"] == day.day) & (altered_merged_df["bir_month"] == day.month)]
            unique_kids_df = bday_kids.loc[bday_kids["date"] == str(day)]
            # Calculate who all came to the party
            kids_at_risk_set = set(unique_kids_df["person_id"])
            for kid in kids_at_risk_set:
                if kid in self.friends_set_index and kid not in self.infected_set:
                    kids_at_risk_set = set.union(kids_at_risk_set, self.children_friends_list[self.friends_set_index[kid]])
            # Randomly select a good population to be added to the bday_infections_pot - select only those who is not in the infected set
            contagious_kids_pot = children_df.loc[(children_df["person_id"].isin(kids_at_risk_set)) & (~children_df["person_id"].isin(self.infected_set)) & (children_df["date"] == str(day))]
            random_selection_infected = random.choice(self.probability_list)
            sample_size = int(contagious_kids_pot.shape[0] * random_selection_infected)
            # sample_size = int(contagious_kids_pot.shape[0])
            contagious_kids_pot = contagious_kids_pot.sample(n=sample_size)
            # self.infected_set = set.union(self.infected_set, set(contagious_kids_pot["person_id"]))
            # Add both the contagious people and the contagious kids to the queue
            if not contagious_people_pot.empty:
                contagious_queue.append(contagious_people_pot)
            if not contagious_kids_pot.empty:
                # Make them contagious
                # for index, infected in contagious_kids_pot:
                #     counter += 1
                #     incubation_period = random.randint(5, 15)
                #     exposed_date = day
                #     altered_merged_df.at[index, "new_infection"] = 1
                #     infection_date = exposed_date + timedelta(days=incubation_period)
                #     contagious_date = infection_date - timedelta(days=2)
                #     range_of_contagious_dates = set([contagious_date + timedelta(days=x) for x in range((infection_date - contagious_date).days)])
                #     self.new_infection_date_dict[self.day_counter] += 1
                #     self.contagious_dates_info[infected["person_id"]] = range_of_contagious_dates
                #     contagious_date_index = [d for d in range(index + incubation_period - 2, index + incubation_period)]
                self.infected_set = set.union(self.infected_set, set(contagious_kids_pot["person_id"]))
                altered_merged_df, counter = self.calculate_infection_metrics(day, counter, contagious_kids_pot)

            while contagious_queue:
                cont_person = contagious_queue.popleft()
                merged_without_infected = altered_merged_df.loc[~altered_merged_df["person_id"].isin(self.infected_set) & (altered_merged_df["date"] == str(day))]
                newly_exposed_set = self.virus_check(cont_person, merged_without_infected)
                self.infected_set = set.union(self.infected_set, newly_exposed_set)
                newly_exposed_df = altered_merged_df.loc[(altered_merged_df["person_id"].isin(newly_exposed_set)) & (altered_merged_df["date"] == str(day))]
                altered_merged_df, counter = self.calculate_infection_metrics(day, counter, newly_exposed_df)
                # for index, infected in newly_exposed_df.iterrows():
                #     """Similar to the initial dataset of contagious people, the incubation, recovery and contagious dates
                #                         are defined and simulated here."""
                #     counter += 1
                #     incubation_period = random.randint(5, 15)
                #     exposed_date = day
                #     altered_merged_df.at[index, "new_infection"] = 1
                #     infection_date = exposed_date + timedelta(days=incubation_period)
                #     contagious_date = infection_date - timedelta(days=2)
                #     range_of_contagious_dates = set([contagious_date + timedelta(days=x) for x in range((infection_date - contagious_date).days)])
                #     self.new_infection_date_dict[self.day_counter] += 1
                #     self.contagious_dates_info[infected["person_id"]] = range_of_contagious_dates
                #     contagious_date_index = [d for d in range(index + incubation_period - 2, index + incubation_period)]
                #     # Assign the contagious property on the mentioned dates
                #     for c_date_idx in contagious_date_index:
                #         altered_merged_df.at[c_date_idx, "contagious"] = 1
                #     recovery_time = int(random.choice(self.recovery_time_probability))
                #     date_of_recovery = infection_date + timedelta(days=recovery_time)
                #     self.recovery_date_dict[str(date_of_recovery)] += 1
                #     range_of_recovery_dates = set([infection_date + timedelta(days=x) for x in range((date_of_recovery - infection_date).days)])
                #     prob_death = random.choice(self.probability_list)
                #     if (14 < recovery_time < 28 and prob_death > self.prob_death_4_weeks) or (recovery_time > 28 and prob_death > self.prob_death_gt4_weeks):
                #         if str(date_of_recovery) not in self.death_dict:
                #             self.death_dict[str(date_of_recovery)] = 1
                #         else:
                #             self.death_dict[str(date_of_recovery)] += 1
                #         death_day_idx = index + incubation_period + recovery_time
                #         altered_merged_df.at[death_day_idx, "death"] = 1
                #     if recovery_time < 14:
                #         recovery_day_idx = index + incubation_period + recovery_time
                #         altered_merged_df.at[recovery_day_idx, "recovery"] = 1
                #     self.quarantined_dates_info[infected["person_id"]] = range_of_recovery_dates

                newly_contagious = altered_merged_df.loc[(~altered_merged_df["person_id"].isin(self.infected_set)) & (altered_merged_df["contagious"].isin([1])) & (altered_merged_df["date"].isin([day]))]
                if not newly_contagious.empty:
                    contagious_queue.append(newly_contagious)
            print(counter)
            self.susceptible_dict[self.day_counter] = 10000 - len(self.infected_set)
            print("next day")

        return altered_merged_df

    def calculate_infection_metrics(self, day, counter, newly_exposed_df):
        for index, infected in newly_exposed_df.iterrows():
            counter += 1
            incubation_period = random.randint(5, 15)
            exposed_date = day
            altered_merged_df.at[index, "new_infection"] = 1
            infection_date = exposed_date + timedelta(days=incubation_period)
            contagious_date = infection_date - timedelta(days=2)
            range_of_contagious_dates = set([contagious_date + timedelta(days=x) for x in range((infection_date - contagious_date).days)])
            self.new_infection_date_dict[self.day_counter] += 1
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
                if str(date_of_recovery) not in self.death_dict:
                    self.death_dict[str(date_of_recovery)] = 1
                else:
                    self.death_dict[str(date_of_recovery)] += 1
                death_day_idx = index + incubation_period + recovery_time
                altered_merged_df.at[death_day_idx, "death"] = 1
            if recovery_time < 14:
                recovery_day_idx = index + incubation_period + recovery_time
                altered_merged_df.at[recovery_day_idx, "recovery"] = 1
            self.quarantined_dates_info[infected["person_id"]] = range_of_recovery_dates
            # self.infected_set.add(infected["person_id"])
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
        curr_day_person_df = curr_day_person_df.loc[~curr_day_person_df["person_id"].isin(self.infected_set)]
        df = curr_day_person_df.merge(cont_person, on=["date"], how="inner", suffixes=['_1', '_2'])
        del curr_day_person_df

        """
        To filter out people who are already infected
        """
        df = df.loc[~df["person_id_1"].isin(self.infected_set)]
        df = df.loc[df["person_id_1"] != df["person_id_2"]]

        df["mask_condition_1"] = df["mask_exposure_1"] * df["mask_exposure_2"]
        """
        To generate the probabilities of people wearing masks
        """
        # df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([0])), "mask_condition_1"] = random.choice(self.probability_list)
        # df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([1])), "mask_condition_1"] = random.choice(self.probability_list)
        # df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([0])), "mask_condition_1"] = random.choice(self.probability_list)

        """
        To check the probabilities of people for different activities
        """
        # df.loc[(df["in_school_1"].isin([1]) & df["in_school_2"].isin([1])) & (df["school_type_1"] == df["school_type_2"]), "school_meetup_1"] = random.choice(self.probability_list)
        # df.loc[(df["attend_work_1"].isin([1]) & df["attend_work_2"].isin([1])) & (df["work_type_1"] == df["work_type_2"]), "work_meetup_1"] = random.choice(self.probability_list)
        # df.loc[(df["dog_walk_1"].isin([1]) & df["dog_walk_2"].isin([1])) & (df["dog_walk_type_1"] == df["dog_walk_type_2"]), "dog_walk_meetup_1"] = random.choice(self.probability_list)
        # df.loc[(df["prayer_group_1"].isin([1]) & df["prayer_group_2"].isin([1])) & (df["prayer_group_type_1"] == df["prayer_group_type_2"]), "prayer_meetup_1"] = random.choice(self.probability_list)
        # df.loc[(df["play_sports_1"].isin([1]) & df["play_sports_2"].isin([1])) & (df["sports_type_1"] == df["sports_type_2"]), "sports_meetup_1"] = random.choice(self.probability_list)
        # df.loc[(df["volunteering_1"].isin([1]) & df["volunteering_2"].isin([1])) & (df["volunteering_type_1"] == df["volunteering_type_2"]), "volunteer_meetup_1"] = random.choice(self.probability_list)
        # df.loc[(df["grocery_visitor_1"].isin([1]) & df["grocery_visitor_2"].isin([1])) & (df["grocery_store_type_1"] == df["grocery_store_type_2"]), "grocery_meetup_1"] = random.choice(self.probability_list)
        # df.loc[(df["gas_visitor_1"].isin([1]) & df["gas_visitor_2"].isin([1])) & (df["gas_store_type_1"] == df["gas_store_type_2"]), "gas_meetup_1"] = random.choice(self.probability_list)

        df["school_meetup_1"] = df["school_exposure_1"] * df["school_exposure_2"]
        df["work_meetup_1"] = df["work_exposure_1"] * df["work_exposure_2"]
        df["dog_walk_meetup_1"] = df["dog_walk_exposure_1"] * df["dog_walk_exposure_2"]
        df["prayer_meetup_1"] = df["prayer_group_exposure_1"] * df["prayer_group_exposure_2"]
        df["sports_meetup_1"] = df["sports_exposure_1"] * df["sports_exposure_2"]
        df["volunteer_meetup_1"] = df["volunteering_exposure_1"] * df["volunteering_exposure_2"]
        df["grocery_meetup_1"] = df["grocery_exposure_1"] * df["grocery_exposure_2"]
        df["gas_meetup_1"] = df["gas_exposure_1"] * df["gas_exposure_2"]
        df["mall_meetup_1"] = df["mall_exposure_1"] * df["mall_exposure_2"]

        # """
        # To calculate average contact rate
        # """
        # school_meetup = df.loc[df["school_meetup_1"] > 0]
        # work_meetup = df.loc[df["work_meetup_1"] > 0]
        # dog_walk_meetup = df.loc[df["dog_walk_meetup_1"] > 0]
        # prayer_meetup = df.loc[df["prayer_meetup_1"] > 0]
        # sports_meetup = df.loc[df["sports_meetup_1"] > 0]
        # volunteer_meetup = df.loc[df["volunteer_meetup_1"] > 0]
        # grocery_meetup = df.loc[df["grocery_meetup_1"] > 0]
        # gas_meetup = df.loc[df["gas_meetup_1"] > 0]
        # mall_meetup = df.loc[df["mall_meetup_1"] > 0]
        # self.contact.append(len(set(school_meetup["person_id_1"]).union(set(work_meetup["person_id_1"]), set(dog_walk_meetup["person_id_1"]), set(prayer_meetup["person_id_1"]),
        #                     set(sports_meetup["person_id_1"]), set(volunteer_meetup["person_id_1"]), set(grocery_meetup["person_id_1"]), set(gas_meetup["person_id_1"]), set(mall_meetup["person_id_1"]))))

        # TODO: Implement this part

        """
        To filter data from the dataframe for mask conditions based on the probabilities given.
        """
        # df_mask_90 = df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([1])) & (df["mask_condition_1"] >= self.mask_11)]
        # df_mask_70 = df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([0])) & (df["mask_condition_1"] >= self.mask_10)]
        # df_mask_50 = df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([1])) & (df["mask_condition_1"] >= self.mask_01)]
        # df_mask_30 = df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([0])) & (df["mask_condition_1"] >= self.mask_00)]
        # df = None

        df_res = pd.concat([df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([1])) & (df["mask_condition_1"] >= self.mask_11)],
                            df.loc[(df["mask_1"].isin([1])) & (df["mask_2"].isin([0])) & (df["mask_condition_1"] >= self.mask_10)],
                            df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([1])) & (df["mask_condition_1"] >= self.mask_01)],
                            df.loc[(df["mask_1"].isin([0])) & (df["mask_2"].isin([0])) & (df["mask_condition_1"] >= self.mask_00)]], axis=0)
        # df_mask_30, df_mask_90, df_mask_70, df_mask_50 = None, None, None, None
        del df
        """
        To filter the dataframe based on the people who match the activities' criteria.
        """
        # df_school = df_res.loc[df_res["school_meetup_1"] >= self.school_prob]
        # df_work = df_res.loc[df_res["work_meetup_1"] >= self.work_prob]
        # df_dog_walk = df_res.loc[df_res["dog_walk_meetup_1"] >= self.dog_walk_prob]
        # df_prayer_group = df_res.loc[df_res["prayer_meetup_1"] > self.prayer_group_prob]
        # df_sports = df_res.loc[df_res["sports_meetup_1"] >= self.play_sports_prob]
        # df_volunteer = df_res.loc[df_res["volunteer_meetup_1"] >= self.volunteer_prob]
        # df_grocery = df_res.loc[df_res["grocery_meetup_1"] >= self.grocery_prob]
        # df_gas_store = df_res.loc[df_res["gas_meetup_1"] >= self.gas_prob]
        # df_res = pd.concat([df_res.loc[df_res["school_meetup_1"] >= self.school_prob],
        #                     df_res.loc[df_res["work_meetup_1"] >= self.work_prob],
        #                     df_res.loc[df_res["dog_walk_meetup_1"] >= self.dog_walk_prob],
        #                     df_res.loc[df_res["prayer_meetup_1"] > self.prayer_group_prob],
        #                     df_res.loc[df_res["sports_meetup_1"] >= self.play_sports_prob],
        #                     df_res.loc[df_res["volunteer_meetup_1"] >= self.volunteer_prob],
        #                     df_res.loc[df_res["grocery_meetup_1"] >= self.grocery_prob],
        #                     df_res.loc[df_res["gas_meetup_1"] >= self.gas_prob]])
        # df_res = pd.concat([df_school, df_work, df_dog_walk, df_prayer_group, df_sports, df_volunteer, df_grocery, df_gas_store], axis=0)
        # df_school, df_work, df_dog_walk, df_prayer_group, df_sports, df_volunteer, df_grocery, df_gas_store = None, None, None, None, None, None, None, None

        # df_res = df_res.loc[((df_res["in_school_1"].isin([1]) & df_res["in_school_2"].isin([1])) & (df_res["school_type_1"] == df_res["school_type_2"])) |
        #                     ((df_res["attend_work_1"].isin([1]) & df_res["attend_work_2"].isin([1])) & (df_res["work_type_1"] == df_res["work_type_2"])) |
        #                     ((df_res["dog_walk_1"].isin([1]) & df_res["dog_walk_2"].isin([1])) & (df_res["dog_walk_type_1"] == df_res["dog_walk_type_2"])) |
        #                     ((df_res["prayer_group_1"].isin([1]) & df_res["prayer_group_2"].isin([1])) & (df_res["prayer_group_type_1"] == df_res["prayer_group_type_2"])) |
        #                     ((df_res["play_sports_1"].isin([1]) & df_res["play_sports_2"].isin([1])) & (df_res["sports_type_1"] == df_res["sports_type_2"])) |
        #                     ((df_res["volunteering_1"].isin([1]) & df_res["volunteering_2"].isin([1])) & (df_res["volunteering_type_1"] == df_res["volunteering_type_2"])) |
        #                     ((df_res["grocery_visitor_1"].isin([1]) & df_res["grocery_visitor_2"].isin([1])) & (df_res["grocery_store_type_1"] == df_res["grocery_store_type_2"])) |
        #                     ((df_res["gas_visitor_1"].isin([1]) & df_res["gas_visitor_2"].isin([1])) & (df_res["gas_store_type_1"] == df_res["gas_store_type_2"]))]

        df_res = df_res.loc[((df_res["in_school_1"].isin([1]) & df_res["in_school_2"].isin([1])) & (df_res["school_type_1"] == df_res["school_type_2"]) & (df_res["school_meetup_1"] >= self.school_prob)) |
                            ((df_res["attend_work_1"].isin([1]) & df_res["attend_work_2"].isin([1])) & (df_res["work_type_1"] == df_res["work_type_2"]) & df_res["work_meetup_1"] >= self.work_prob) |
                            ((df_res["dog_walk_1"].isin([1]) & df_res["dog_walk_2"].isin([1])) & (df_res["dog_walk_type_1"] == df_res["dog_walk_type_2"]) & (df_res["dog_walk_meetup_1"] >= self.dog_walk_prob)) |
                            ((df_res["prayer_group_1"].isin([1]) & df_res["prayer_group_2"].isin([1])) & (df_res["prayer_group_type_1"] == df_res["prayer_group_type_2"]) & (df_res["prayer_meetup_1"] > self.prayer_group_prob)) |
                            ((df_res["play_sports_1"].isin([1]) & df_res["play_sports_2"].isin([1])) & (df_res["sports_type_1"] == df_res["sports_type_2"]) & (df_res["sports_meetup_1"] >= self.play_sports_prob)) |
                            ((df_res["volunteering_1"].isin([1]) & df_res["volunteering_2"].isin([1])) & (df_res["volunteering_type_1"] == df_res["volunteering_type_2"]) & (df_res["volunteer_meetup_1"] >= self.volunteer_prob)) |
                            ((df_res["grocery_visitor_1"].isin([1]) & df_res["grocery_visitor_2"].isin([1])) & (df_res["grocery_store_type_1"] == df_res["grocery_store_type_2"]) & (df_res["grocery_meetup_1"] >= self.grocery_prob)) |
                            ((df_res["gas_visitor_1"].isin([1]) & df_res["gas_visitor_2"].isin([1])) & (df_res["gas_store_type_1"] == df_res["gas_store_type_2"]) & (df_res["gas_meetup_1"] >= self.gas_prob))]


        # df_res = df_res.loc[((df_res["in_school_1"].isin([1]) & df_res["in_school_2"].isin([1])) & (
        #             df_res["school_type_1"] == df_res["school_type_2"]) & (
        #                                  df_res["school_meetup_1"] >= self.school_prob)) |
        #                     ((df_res["attend_work_1"].isin([1]) & df_res["attend_work_2"].isin([1])) & (
        #                                 df_res["work_type_1"] == df_res["work_type_2"]) & (
        #                                  df_res["work_meetup_1"] >= self.work_prob)) |
        #                     ((df_res["dog_walk_1"].isin([1]) & df_res["dog_walk_2"].isin([1])) & (
        #                                 df_res["dog_walk_type_1"] == df_res["dog_walk_type_2"]) & (
        #                                  df_res["dog_walk_meetup_1"] >= self.dog_walk_prob)) |
        #                     ((df_res["prayer_group_1"].isin([1]) & df_res["prayer_group_2"].isin([1])) & (
        #                                 df_res["prayer_group_type_1"] == df_res["prayer_group_type_2"]) & (
        #                                  df_res["prayer_meetup_1"] >= self.prayer_group_prob)) |
        #                     ((df_res["play_sports_1"].isin([1]) & df_res["play_sports_2"].isin([1])) & (
        #                                 df_res["sports_type_1"] == df_res["sports_type_2"]) & (
        #                                  df_res["sports_meetup_1"] >= self.play_sports_prob)) |
        #                     ((df_res["volunteering_1"].isin([1]) & df_res["volunteering_2"].isin([1])) & (
        #                                 df_res["volunteering_type_1"] == df_res["volunteering_type_2"]) & (
        #                                  df_res["volunteer_meetup_1"] >= self.volunteer_prob)) |
        #                     ((df_res["grocery_visitor_1"].isin([1]) & df_res["grocery_visitor_2"].isin([1])) & (
        #                                 df_res["grocery_store_type_1"] == df_res["grocery_store_type_2"]) & (
        #                                  df_res["grocery_meetup_1"] >= self.grocery_prob)) |
        #                     ((df_res["gas_visitor_1"].isin([1]) & df_res["gas_visitor_2"].isin([1])) & (
        #                                 df_res["gas_store_type_1"] == df_res["gas_store_type_2"]) & (
        #                                  df_res["gas_meetup_1"] >= self.gas_prob))]

        df_res = df_res.loc[~df_res["person_id_1"].isin(self.infected_set)]
        set_of_exposed_people = set(df_res["person_id_1"])
        del df_res
        return set_of_exposed_people

    def dob_split(self, birthday_df):
        birthday_df["bir_day"] = pd.to_datetime(birthday_df["dob"]).dt.day
        birthday_df["bir_month"] = pd.to_datetime(birthday_df["dob"]).dt.month
        return birthday_df


if __name__ == '__main__':
    people_df = pd.read_csv("../Results/Data/people.csv")
    bir = Birthdays()
    bir.create_friends(people_df)
    merged_df = pd.read_csv("../Results/Data/merged.csv")
    altered_merged_df = bir.dob_split(merged_df)
    children_df = altered_merged_df.loc[altered_merged_df["age"].isin(bir.children_not_toddlers)]
    bir.generate_dates()
    altered_merged_df = bir.initialize_infections(children_df)
    final_df = bir.initiate_birthdays(altered_merged_df, children_df)
    with open('../Results/Data/Birthdays/new_infection_date_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.new_infection_date_dict))
    with open('../Results/Data/Birthdays/recovery_date_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.recovery_date_dict))
    with open('../Results/Data/Birthdays/susceptible_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.susceptible_dict))
    with open('../Results/Data/Birthdays/death_bir_dict.json', 'w') as convert_file:
        convert_file.write(json.dumps(bir.death_dict))
    final_df.to_csv("../Results/Data/Birthdays/birthday_final.csv", index=False)