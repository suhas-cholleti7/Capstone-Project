import sys
import time
import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
import random

"""
This program is used to generate the population of a community.
The data generated includes:
1. Date table
2. Family table
3. People table
These three are combined to generate the activities performed by the family or the people individually.

Rules to follow before execution of this file:
- In the parent directory, create folders with the following hierarchy:
- Results
    - Data
        - Birthdays
        - General
        - Vax
    - Graphs

Author: Ravikiran Jois Yedur Prabhakar
Advisor: Dr. Thomas B. Kinsman
"""

class PopulationGen:

    def __init__(self):
        """
        To set the parameters of the model
        """
        self.NO_OF_PEOPLE = int(sys.argv[1])
        self.NO_OF_FAMILIES = 0
        self.family_size = (1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6)
        self.store_visitors = dict()
        self.gender = ["M", "F"]
        self.bool_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        self.bool_higher_probability = [0, 0, 1, 1, 0, 1, 1, 1, 1, 1]
        self.bool_lower_probability = [1, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        self.mask_values = [0, 1]
        self.person_counter = 1
        self.dates = []
        # The different sets of days for determining the actions of people
        self.weekends = {"Sat", "Sun"}
        self.weekdays = {"Mon", "Tue", "Wed", "thu", "fri"}
        self.grade_1_days = {"mon", "wed", "fri"}
        self.not_grade_1_days = {"tue", "thu"}
        self.grade_2_days = {"tue", "thu", "fri"}
        self.not_grade_2_days = {"mon", "wed"}
        self.grade_3_days = {"mon", "tue", "fri"}
        self.not_grade_3_days = {"wed", "fri"}
        self.grade_4_days = {"wed", "thu", "fri"}
        self.not_grade_4_days = {"mon", "tue"}
        self.middle_1_days = {"mon", "tue", "thu"}
        self.not_middle_1_days = {"wed", "fri"}
        self.middle_2_days = {"tue", "wed", "thu"}
        self.not_middle_2_days = {"mon", "fri"}
        self.middle_3_days = {"mon", "thu", "fri"}
        self.not_middle_3_days = {"tue", "wed"}
        self.middle_4_days = {"mon", "wed", "fri"}
        self.not_middle_4_days = {"tue", "thu"}
        self.higher_1_days = {"tue", "wed", "thu"}
        self.not_higher_1_days = {"mon", "fri"}
        self.higher_2_days = {"mon", "thu", "fri"}
        self.not_higher_2_days = {"tue", "wed"}
        self.higher_3_days = {"wed", "thu", "fri"}
        self.not_higher_3_days = {"mon", "tue"}
        self.higher_4_days = {"mon", "tue", "fri"}
        self.not_higher_4_days = {"wed", "thu"}
        # Ages of different sets of people
        self.toddlers = set([age for age in range(0, 5)])
        self.grade_school = set([age for age in range(5, 12)])
        self.middle_school = set([age for age in range(12, 15)])
        self.high_school = set([age for age in range(16, 19)])
        self.children = set([age for age in range(0, 19)])
        self.children_not_toddlers = set([age for age in range(5, 19)])
        self.children_volunteering_age = set([age for age in range(8, 19)])
        self.adults = set([age for age in range(19, 100)])
        self.adults_to60 = set([age for age in range(19, 61)])
        self.adults_f60_t70 = set([age for age in range(61, 71)])
        self.adults_f70 = set([age for age in range(71, 100)])
        # The several groups/activities that people belong to or take part in
        self.grade_school_types = ["gs_"+str(i) for i in range(1, 5)]
        self.middle_school_types = ["ms_" + str(i) for i in range(1, 5)]
        self.high_school_types = ["hs_" + str(i) for i in range(1, 5)]
        self.work_types = ["aw_" + str(i) for i in range(1, 7)]
        self.volunteering_types = ["vt_" + str(i) for i in range(1, 5)]
        self.prayer_group_types = ["pgt_" + str(i) for i in range(1, 5)]
        self.sports_types = ["ps_" + str(i) for i in range(1, 5)]
        self.dog_walking_types = ["dw_" + str(i) for i in range(1, 5)]
        self.grocery_store_type = ["gr_st_" + str(i) for i in range(1, 5)]
        self.gas_store_type = ["gs_st_" + str(i) for i in range(1, 5)]
        self.mall_types = ["m_" + str(i) for i in range(1, 3)]
        # The list of probabilities from where the probabilities of actions of people are got from
        self.probability_list = [0.1 * x for x in range(1, 10)]

    def create_dates(self):
        """
        To create the date of birth and the current date fields
        :return: Dataframes with dates for the two roles
        """
        # Current date dataframe from 1/1/2020 to 5/31/2021
        start_date = date(2020, 1, 1)
        end_date = date(2020, 5, 31)
        weekdays = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
        delta = end_date - start_date
        current_date_list = []
        week_no = 1

        for i in range(delta.days + 1):
            # mon is 0, sun is 6
            c_date = start_date + timedelta(days=i)
            self.dates.append(c_date)
            day_of_week = c_date.weekday()
            if day_of_week == 6:
                week_no += 1
            current_date_list.append({"date": str(c_date), "day_of_week": weekdays[day_of_week], "week_no": week_no})
        current_date_df = pd.DataFrame(current_date_list)

        """
        Date of birth fields
        For Adults - from Jan 1st 1930 to Jan 1st 2003
        
        The DOB is randomly assigned from the year generated below.
        This is added to a set and the people are assigned a DOB randomly from this set.
        """
        start_date = date(1940, 1, 1)
        end_date = date(2003, 1, 1)
        dob_adult_set = set()
        no_of_adults = int(0.65 * self.NO_OF_PEOPLE)
        for d in range(no_of_adults):
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_number_of_days)
            dob_adult_set.add(random_date)

        # For Children
        start_date = date(2003, 1, 1)
        end_date = date(2020, 1, 1)
        dob_children_set = set()
        no_of_children = int(0.35 * self.NO_OF_PEOPLE)
        for d in range(no_of_children):
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_number_of_days)
            dob_children_set.add(random_date)

        return current_date_df, dob_adult_set, dob_children_set

    def initialize_families(self):
        """
        To initialize the family information and some attributes that the family part takes in.
        :return: The family dataframe
        """
        family_id_counter = 1
        size_checker = 0
        family = []
        while size_checker < self.NO_OF_PEOPLE:
            # To check if the population is completely generated
            family_dict = dict()
            family_dict["fam_id"] = family_id_counter
            family_dict["family_size"] = random.choice(self.family_size)
            family_dict["mask"] = random.choice(self.mask_values)
            family_dict["has_dog"] = random.choice(self.bool_values)
            if family_dict["has_dog"] == 1:
                dw_type = random.choice(self.dog_walking_types)
                int_dog_walk = random.choice(self.bool_higher_probability)
            else:
                int_dog_walk = 0
            if int_dog_walk:
                family_dict["dog_walk_type"] = dw_type
                family_dict["int_dog_walk"] = int_dog_walk
                family_dict["dog_walk_exposure"] = random.choice(self.probability_list)
            family_dict["grocery_store_type"] = random.choice(self.grocery_store_type)
            family_dict["gas_store_type"] = random.choice(self.gas_store_type)
            family_dict["grocery_exposure"] = random.choice(self.probability_list)
            family_dict["gas_exposure"] = random.choice(self.probability_list)
            family_id_counter += 1
            self.NO_OF_FAMILIES += 1
            size_checker += family_dict["family_size"]
            family.append(family_dict)
        return pd.DataFrame(family)

    def initialize_people(self, families_df, dob_adult_set, dob_child_set):
        """
        To initialize the people data in the families
        :param families_df: The family dataframe
        :param dob_adult_set: The date of births for adults
        :param dob_child_set: The date of births for children
        :return: The people dataframe
        """
        people = []
        for idx, fam in families_df.iterrows():
            fam_size = fam["family_size"]
            while fam_size > 2:
                # If here, then there are children.
                person = dict()
                person["person_id"] = self.person_counter
                person["fam_id"] = fam["fam_id"]
                person["gender"] = random.choice(self.gender)
                person["dob"] = random.choice(list(dob_child_set))
                person["age"] = abs(date.today().year - person["dob"].year)
                person["mask_exposure"] = random.choice(self.probability_list)
                if 0 <= person["age"] <= 4:
                    person["school_type"] = "Toddlers"
                    person["in_school"] = 0
                    person["school_exposure"] = 0
                elif 5 <= person["age"] <= 11:
                    person["school_type"] = random.choice(self.grade_school_types)
                    person["school_exposure"] = random.choice(self.probability_list)
                elif 12 <= person["age"] <= 15:
                    person["school_type"] = random.choice(self.middle_school_types)
                    person["school_exposure"] = random.choice(self.probability_list)
                elif 16 <= person["age"] <= 18:
                    person["school_type"] = random.choice(self.high_school_types)
                    person["school_exposure"] = random.choice(self.probability_list)
                volunteering = 0
                prayer_group = 0
                play_sports = 0
                int_volunteering = 0
                int_play_sports = 0
                int_prayer = 0
                int_mall = 0
                # Setting interests for the activities of children.
                # int -> Interest, not Integer.
                if 6 < person["age"] < 13:
                    volunteering = random.choice(self.bool_lower_probability)
                    play_sports = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_lower_probability)
                    int_play_sports = random.choice(self.bool_higher_probability)
                    int_mall = random.choice(self.bool_lower_probability)
                elif 13 < person["age"] < 18:
                    volunteering = random.choice(self.bool_values)
                    prayer_group = random.choice(self.bool_values)
                    play_sports = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_values)
                    int_play_sports = random.choice(self.bool_higher_probability)
                    int_prayer = random.choice(self.bool_values)
                    int_mall = random.choice(self.bool_values)

                """
                Initializing the values for the following conditions
                If the person is interested in volunteering, then a random volunteering group is chosen
                Similarly, if the person is interested in going to a prayer group, a random prayer group is chosen
                Same goes for playing sports
                """
                if volunteering == 1:
                    person["volunteering_type"] = random.choice(self.volunteering_types)
                    person["int_volunteering"] = int_volunteering
                if prayer_group == 1:
                    person["prayer_group_type"] = random.choice(self.prayer_group_types)
                    person["int_prayer"] = int_prayer
                if play_sports == 1:
                    person["sports_type"] = random.choice(self.sports_types)
                    person["int_play_sports"] = int_play_sports
                if int_mall == 1:
                    person["int_mall"] = int_mall
                    person["mall_type"] = random.choice(self.mall_types)
                person["volunteering_exposure"] = random.choice(self.probability_list)
                person["prayer_group_exposure"] = random.choice(self.probability_list)
                person["sports_exposure"] = random.choice(self.probability_list)
                person["work_exposure"] = 0
                person["mall_exposure"] = random.choice(self.probability_list)
                self.person_counter += 1
                fam_size -= 1
                people.append(person)

            while fam_size != 0:
                # If here, then there are adults. Children in this family are already generated.
                person = dict()
                person["person_id"] = self.person_counter
                person["fam_id"] = fam["fam_id"]
                person["gender"] = random.choice(self.gender)
                person["dob"] = random.choice(list(dob_adult_set))
                person["age"] = abs(date.today().year - person["dob"].year)
                person["mask_exposure"] = random.choice(self.probability_list)
                person["school_type"] = "No-school"
                person["in_school"] = 0
                if person["fam_id"] not in self.store_visitors:
                    self.store_visitors[person["fam_id"]] = person["person_id"]
                person["school_exposure"] = 0
                volunteering = 0
                prayer_group = 0
                play_sports = 0
                # Represents the interest of the person to do these activities. Here, "int" represents interest.
                int_volunteering = 0
                int_play_sports = 0
                int_prayer = 0
                int_work = 0
                int_mall = 0

                """
                In this simulation, ages govern the attributes of the people thus, attempting to emulate the real world.
                Assigning interests to the adults in the below segment. (int -> Interest. Not Integer)
                """
                if person["age"] in self.adults_to60:
                    # To assign interest and activities to people between the ages 19 and 60.
                    int_work = random.choice(self.bool_higher_probability)
                    person["work_type"] = random.choice(self.work_types)
                    volunteering = random.choice(self.bool_lower_probability)
                    int_volunteering = random.choice(self.bool_lower_probability)
                    play_sports = random.choice(self.bool_lower_probability)
                    int_play_sports = random.choice(self.bool_lower_probability)
                    int_prayer = random.choice(self.bool_lower_probability)
                    int_mall = random.choice(self.bool_values)
                if person["age"] in self.adults_f60_t70:
                    # To assign interest and activities to people between the ages 60 and 70.
                    int_work = random.choice(self.bool_lower_probability)
                    person["work_type"] = random.choice(self.work_types)
                    volunteering = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_higher_probability)
                    int_prayer = random.choice(self.bool_values)
                    int_mall = random.choice(self.bool_higher_probability)
                if person["age"] in self.adults_f70:
                    # To assign interest and activities to people from the ages 70 and above.
                    person["attend_work"] = 0
                    volunteering = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_higher_probability)
                    person["prayer_group_type"] = random.choice(self.prayer_group_types)
                    int_prayer = random.choice(self.bool_higher_probability)
                    int_mall = random.choice(self.bool_lower_probability)

                """
                Initializing the values for the following conditions
                If the person is interested in volunteering, then a random volunteering group is chosen
                Similarly, if the person is interested in going to a prayer group, a random prayer group is chosen
                Same goes for playing sports.
                """
                # In the following code block, the types of groups the people do various activities are selected.
                if volunteering == 1:
                    person["volunteering_type"] = random.choice(self.volunteering_types)
                    person["int_volunteering"] = int_volunteering
                if prayer_group == 1:
                    person["prayer_group_type"] = random.choice(self.prayer_group_types)
                    person["int_prayer"] = int_prayer
                if play_sports == 1:
                    person["sports_type"] = random.choice(self.sports_types)
                    person["int_play_sports"] = int_play_sports
                if int_work == 1:
                    person["work_type"] = random.choice(self.work_types)
                    person["int_work"] = int_work
                if int_mall == 1:
                    person["mall_type"] = random.choice(self.mall_types)
                    person["int_mall"] = int_mall
                person["volunteering_exposure"] = random.choice(self.probability_list)
                person["prayer_group_exposure"] = random.choice(self.probability_list)
                person["sports_exposure"] = random.choice(self.probability_list)
                person["work_exposure"] = random.choice(self.probability_list)
                person["mall_exposure"] = random.choice(self.probability_list)
                self.person_counter += 1
                fam_size -= 1
                people.append(person)
        return pd.DataFrame(people)

    def combine_families_date(self, families_df, current_date_df, people_df):
        """
        To combine the family and the date dataframes
        :param families_df: The family dataframe
        :param current_date_df: The current date dataframe
        :param people_df: The people dataframe
        :return: The dataframe with people, family and date dataframes merged
        """
        families_df["tmp"] = 1
        current_date_df["tmp"] = 1
        merged_df = pd.merge(families_df, current_date_df, on='tmp')
        del merged_df["tmp"]
        del families_df["tmp"]
        del current_date_df["tmp"]

        merged_df = self.store_visit_filler(merged_df)
        fully_merged_df = pd.merge(people_df, merged_df, on="fam_id", how="left")
        fully_merged_df.loc[(fully_merged_df["visit_grocery"] == 1) & (fully_merged_df["person_id"].isin(self.store_visitors.values())), "grocery_visitor"] = 1
        fully_merged_df.loc[(fully_merged_df["visit_gasstore"] == 1) & (fully_merged_df["person_id"].isin(self.store_visitors.values())), "gas_visitor"] = 1
        return fully_merged_df

    def store_visit_filler(self, merged_df):
        """
        To fill up the store and gas station quantities for the families
        :param merged_df: The date and family dataframes merged together
        :return: The edited merged dataframe
        """
        groceries = np.random.randint(3, 7, (self.NO_OF_FAMILIES, 1), dtype='int64')
        gas = np.random.randint(2, 10, (self.NO_OF_FAMILIES, 1), dtype='int64')
        groceries = np.where(groceries < 3, 7, groceries)
        gas = np.where(gas < 2, 10, gas)
        fam_resources = np.stack((groceries, gas))

        for day in self.dates:
            fam_resources = fam_resources - 1
            out_of_groceries = np.array(np.where(fam_resources[0] < 3)) + 1
            merged_df.loc[(merged_df["fam_id"].isin(out_of_groceries[0])) & (merged_df["date"] == str(day)), "visit_grocery"] = 1
            out_of_groceries = out_of_groceries - 1
            out_of_gas = np.array(np.where(fam_resources[1] < 2)) + 1
            merged_df.loc[(merged_df["fam_id"].isin(out_of_gas[0])) & (merged_df["date"] == str(day)), "visit_gasstore"] = 1
            out_of_gas = out_of_gas - 1
            fam_resources[0][fam_resources[0] < 3] = 7
            fam_resources[1][fam_resources[1] < 2] = 10
        return merged_df

    def generate_attributes(self, merged_df):
        """
        To assign attributes to people
        :param merged_df: The complete dataframe
        :return: The updated dataframe
        """

        """
        CHILDREN - General conditions
        """
        merged_df.loc[merged_df["age"] < 19, ["in_school", "dog_walk", "attend_work"]] = [0, 0, 0]
        merged_df.loc[merged_df["age"] <= 4, ["school_type", "attend_work", "prayer_group", "play_sports", "volunteering", "in_school"]] = ["Toddlers", 0, 0, 0, 0, 0]
        """
        Grade-School attendance
        """
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["gs_1"]) & merged_df["day_of_week"].isin(self.grade_1_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["gs_2"]) & merged_df["day_of_week"].isin(self.grade_2_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["gs_3"]) & merged_df["day_of_week"].isin(self.grade_3_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["gs_4"]) & merged_df["day_of_week"].isin(self.grade_4_days), "in_school"] = 1
        """
        Middle-School attendance
        """
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["ms_1"]) & merged_df["day_of_week"].isin(self.middle_1_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["ms_2"]) & merged_df["day_of_week"].isin(self.middle_2_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["ms_3"]) & merged_df["day_of_week"].isin(self.middle_3_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["ms_4"]) & merged_df["day_of_week"].isin(self.middle_4_days), "in_school"] = 1
        """
        High-School attendance
        """
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["hs_1"]) & merged_df["day_of_week"].isin(self.higher_1_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["hs_2"]) & merged_df["day_of_week"].isin(self.higher_2_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["hs_3"]) & merged_df["day_of_week"].isin(self.higher_3_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["hs_4"]) & merged_df["day_of_week"].isin(self.higher_4_days), "in_school"] = 1

        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["day_of_week"].isin(self.weekends), "in_school"] = 0

        """
        Other activities
        """
        # 1. Volunteering
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["vt_1"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_1_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["vt_2"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_1_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["vt_3"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_1_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["vt_4"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_1_days)), "volunteering"] = 1

        # 2. Sports
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["ps_1"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_2_days)), "play_sports"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["ps_2"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_2_days)), "play_sports"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["ps_3"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "play_sports"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["ps_4"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "play_sports"] = 1

        # 3. Prayer Group
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["prayer_group_type"].isin(self.prayer_group_types) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(self.weekends), "prayer_group"] = 1

        """
        ADULTS - General conditions
        """
        merged_df.loc[merged_df["age"] > 18, "in_school"] = 0
        merged_df.loc[merged_df["person_id"].isin(self.store_visitors.values()) & merged_df["has_dog"].isin([1]) & merged_df["int_dog_walk"].isin([1]) & merged_df["dog_walk_type"].isin(self.dog_walking_types), "dog_walk"] = 1

        """
        General activities of adults
        """
        merged_df.loc[merged_df["age"] > 70, ["attend_work", "play_sports"]] = [0, 0]

        # Work
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["aw_1"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.grade_1_days, self.higher_2_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["aw_2"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.middle_1_days, self.middle_2_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["aw_3"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.higher_1_days, self.grade_1_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["aw_4"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.higher_3_days, self.grade_3_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["aw_5"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.middle_4_days, self.higher_4_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["aw_6"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.grade_3_days, self.middle_3_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["aw_7"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.grade_4_days, self.higher_2_days)), "attend_work"] = 1

        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["aw_1"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.grade_3_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["aw_2"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.higher_3_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["aw_3"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.middle_1_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["aw_4"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.middle_4_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["aw_5"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.grade_4_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["aw_6"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.higher_2_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["aw_7"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.grade_2_days), "attend_work"] = 1

        # Mall Visit
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["day_of_week"].isin(set.union(self.weekends, self.higher_2_days)) & merged_df["int_mall"].isin([1]) & merged_df["mall_type"].isin(["mall_type_1"]), "in_mall"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["day_of_week"].isin(set.union(self.weekends, self.middle_1_days)) & merged_df["int_mall"].isin([1]) & merged_df["mall_type"].isin(["mall_type_2"]), "in_mall"] = 1

        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_2_days)) & merged_df["int_mall"].isin([1]) & merged_df["mall_type"].isin(["mall_type_1"]), "in_mall"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)) & merged_df["int_mall"].isin([1]) & merged_df["mall_type"].isin(["mall_type_2"]), "in_mall"] = 1

        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["day_of_week"].isin(set.union(self.weekends)) & merged_df["int_mall"].isin([1]) & merged_df["mall_type"].isin(self.mall_types), "in_mall"] = 1

        # Prayer group
        # Above 70 years
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["pgt_1"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_1_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["pgt_2"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["pgt_3"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_3_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["pgt_4"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_4_days)), "prayer_group"] = 1

        # Above 60 and below 70
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["pgt_1"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["pgt_2"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["pgt_3"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["pgt_4"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_4_days)), "prayer_group"] = 1

        # Above below 60
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["prayer_group_type"].isin(self.prayer_group_types) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(self.weekends), "prayer_group"] = 1

        # Volunteering
        # Above 70 years
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["volunteering_type"].isin(["volunteering_type_1"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_3_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["volunteering_type"].isin(["volunteering_type_2"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_3_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["volunteering_type"].isin(["volunteering_type_3"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_3_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["volunteering_type"].isin(["volunteering_type_4"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "volunteering"] = 1

        # Above 60 and below 70
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["volunteering_type"].isin(["volunteering_type_1"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_1_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["volunteering_type"].isin(["volunteering_type_2"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["volunteering_type"].isin(["volunteering_type_3"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_3_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["volunteering_type"].isin(["volunteering_type_4"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_3_days)), "volunteering"] = 1

        # Above below 60
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["volunteering_type"].isin(self.volunteering_types) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(self.weekends), "volunteering"] = 1

        # Play Sports
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["sports_type"].isin(self.sports_types) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(self.weekends), "play_sports"] = 1

        return merged_df


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: python3 population_generator_v3.py [Argument_1]")
        print("     Argument_1: Number of people in the population")
        sys.exit()
    start = time.time()
    pop = PopulationGen()

    current_date_df, dob_adult_set, dob_children_set = pop.create_dates()

    families_df = pop.initialize_families()
    families_df = families_df.replace(np.nan, 0)

    people_df = pop.initialize_people(families_df, dob_adult_set, dob_children_set)
    people_df = people_df.replace(np.nan, 0)

    fully_merged_df = pop.combine_families_date(families_df, current_date_df, people_df)
    fully_merged_df = pop.generate_attributes(fully_merged_df)
    current_date_df.to_csv("../Results/Data/dates.csv", index=False)
    families_df.to_csv("../Results/Data/family.csv", index=False)
    people_df.to_csv("../Results/Data/people.csv", index=False)
    fully_merged_df = fully_merged_df.replace(np.nan, 0)
    fully_merged_df.drop(["int_play_sports", "int_mall", "int_volunteering", "int_work", "int_prayer", "has_dog"], axis=1, inplace=True)
    fully_merged_df.to_csv("../Results/Data/merged.csv", index=False)
    print("Total time taken:", (time.time() - start)/60)