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

Author: Ravikiran Jois Yedur Prabhakar
Advisor: Dr. Thomas B. Kinsman
"""

class PopulationGen:

    def __init__(self):
        self.NO_OF_PEOPLE = 10000
        self.NO_OF_FAMILIES = 0
        self.family_size = (1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6)
        self.store_visitors = dict()
        self.gender = ["M", "F"]
        self.bool_values = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        self.bool_higher_probability = [0, 0, 1, 1, 0, 1, 1, 1, 1, 1]
        self.bool_lower_probability = [1, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        self.person_counter = 1
        self.dates = []
        self.weekends = {"Saturday", "Sunday"}
        self.weekdays = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
        self.grade_1_days = {"Monday", "Wednesday", "Friday"}
        self.not_grade_1_days = {"Tuesday", "Thursday"}
        self.grade_2_days = {"Tuesday", "Thursday", "Friday"}
        self.not_grade_2_days = {"Monday", "Wednesday"}
        self.grade_3_days = {"Monday", "Tuesday", "Friday"}
        self.not_grade_3_days = {"Wednesday", "Friday"}
        self.grade_4_days = {"Wednesday", "Thursday", "Friday"}
        self.not_grade_4_days = {"Monday", "Tuesday"}
        self.middle_1_days = {"Monday", "Tuesday", "Thursday"}
        self.not_middle_1_days = {"Wednesday", "Friday"}
        self.middle_2_days = {"Tuesday", "Wednesday", "Thursday"}
        self.not_middle_2_days = {"Monday", "Friday"}
        self.middle_3_days = {"Monday", "Thursday", "Friday"}
        self.not_middle_3_days = {"Tuesday", "Wednesday"}
        self.middle_4_days = {"Monday", "Wednesday", "Friday"}
        self.not_middle_4_days = {"Tuesday", "Thursday"}
        self.higher_1_days = {"Tuesday", "Wednesday", "Thursday"}
        self.not_higher_1_days = {"Monday", "Friday"}
        self.higher_2_days = {"Monday", "Thursday", "Friday"}
        self.not_higher_2_days = {"Tuesday", "Wednesday"}
        self.higher_3_days = {"Wednesday", "Thursday", "Friday"}
        self.not_higher_3_days = {"Monday", "Tuesday"}
        self.higher_4_days = {"Monday", "Tuesday", "Friday"}
        self.not_higher_4_days = {"Wednesday", "Thursday"}
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
        self.grade_school_types = ["Grade-school_"+str(i) for i in range(1, 5)]
        self.middle_school_types = ["Middle-school_" + str(i) for i in range(1, 5)]
        self.high_school_types = ["High-school_" + str(i) for i in range(1, 5)]
        self.work_types = ["attend_work_" + str(i) for i in range(1, 8)]
        self.volunteering_types = ["volunteer_type_" + str(i) for i in range(1, 5)]
        self.prayer_group_types = ["prayer_group_type_" + str(i) for i in range(1, 5)]
        self.sports_types = ["play_sports_" + str(i) for i in range(1, 5)]
        self.dog_walk_types = ["dog_walk_" + str(i) for i in range(1, 5)]
        self.grocery_store_type = ["grocery_store_" + str(i) for i in range(1, 5)]
        self.gas_store_type = ["gas_store_" + str(i) for i in range(1, 5)]

    def create_dates(self):
        """
        To create the date of birth and the current date fields
        :return: Dataframes with dates for the two roles
        """
        # Current date dataframe from 1/1/2020 to 1/1/2021
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 5)
        weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        delta = end_date - start_date
        current_date_list = []

        for i in range(delta.days + 1):
            # Monday is 0, Sunday is 6
            c_date = start_date + timedelta(days=i)
            self.dates.append(c_date)
            day_of_week = c_date.weekday()
            current_date_list.append({"date": str(c_date), "day_of_week": weekdays[day_of_week]})
        current_date_df = pd.DataFrame(current_date_list)

        """
        Date of birth fields
        For Adults - from Jan 1st 1930 to Jan 1st 2003
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
        end_date = date(2021, 1, 1)
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
            family_dict = dict()
            family_dict["fam_id"] = family_id_counter
            family_dict["family_size"] = random.choice(self.family_size)
            family_dict["mask"] = random.choice(self.bool_values)
            family_dict["has_dog"] = random.choice(self.bool_values)
            if family_dict["has_dog"] == 1:
                dog_walk_type = random.choice(self.dog_walk_types)
                int_dog_walk = random.choice(self.bool_higher_probability)
            else:
                int_dog_walk = 0
            if int_dog_walk:
                family_dict["dog_walk_type"] = dog_walk_type
                family_dict["int_dog_walk"] = int_dog_walk
            family_dict["grocery_store_type"] = random.choice(self.grocery_store_type)
            family_dict["gas_store_type"] = random.choice(self.gas_store_type)
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
                person = dict()
                person["person_id"] = self.person_counter
                person["fam_id"] = fam["fam_id"]
                person["gender"] = random.choice(self.gender)
                person["dob"] = random.choice(list(dob_child_set))
                person["age"] = abs(date.today().year - person["dob"].year)
                if 0 <= person["age"] <= 4:
                    person["school_type"] = "Toddlers"
                    person["in_school"] = 0
                elif 5 <= person["age"] <= 11:
                    person["school_type"] = random.choice(self.grade_school_types)
                elif 12 <= person["age"] <= 15:
                    person["school_type"] = random.choice(self.middle_school_types)
                elif 16 <= person["age"] <= 18:
                    person["school_type"] = random.choice(self.high_school_types)
                volunteering = 0
                prayer_group = 0
                play_sports = 0
                int_volunteering = 0
                int_play_sports = 0
                int_prayer = 0

                """
                Some decisions are made to pick data for individuals such as, interests in many activities.
                These values are based on the ages of the people.
                Here, children who belong to the ages between 8 and 18 are chosen and certain attributes are assigned to them.
                These attributes include their interests in doing/attending certain common activities. 
                """

                if 8 < person["age"] < 13:
                    volunteering = random.choice(self.bool_lower_probability)
                    play_sports = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_lower_probability)
                    int_play_sports = random.choice(self.bool_higher_probability)
                elif 13 < person["age"] < 18:
                    volunteering = random.choice(self.bool_values)
                    prayer_group = random.choice(self.bool_values)
                    play_sports = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_values)
                    int_play_sports = random.choice(self.bool_higher_probability)
                    int_prayer = random.choice(self.bool_values)

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

                self.person_counter += 1
                fam_size -= 1
                people.append(person)

            while fam_size != 0:
                person = dict()
                person["person_id"] = self.person_counter
                person["fam_id"] = fam["fam_id"]
                person["gender"] = random.choice(self.gender)
                person["dob"] = random.choice(list(dob_adult_set))
                person["age"] = abs(date.today().year - person["dob"].year)
                person["school_type"] = "No-school"
                person["in_school"] = 0
                if person["fam_id"] not in self.store_visitors:
                    self.store_visitors[person["fam_id"]] = person["person_id"]
                volunteering = 0
                prayer_group = 0
                play_sports = 0
                int_volunteering = 0
                int_play_sports = 0
                int_prayer = 0
                int_work = 0

                """
                In this simulation, ages govern the attributes of the people thus, attempting to emulate the real world.
                """
                if person["age"] in self.adults_to60:
                    int_work = random.choice(self.bool_higher_probability)
                    person["work_type"] = random.choice(self.work_types)
                    volunteering = random.choice(self.bool_lower_probability)
                    int_volunteering = random.choice(self.bool_lower_probability)
                    play_sports = random.choice(self.bool_lower_probability)
                    int_play_sports = random.choice(self.bool_lower_probability)
                    int_prayer = random.choice(self.bool_lower_probability)
                if person["age"] in self.adults_f60_t70:
                    int_work = random.choice(self.bool_lower_probability)
                    person["work_type"] = random.choice(self.work_types)
                    volunteering = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_higher_probability)
                    int_prayer = random.choice(self.bool_values)
                if person["age"] in self.adults_f70:
                    person["attend_work"] = 0
                    volunteering = random.choice(self.bool_higher_probability)
                    int_volunteering = random.choice(self.bool_higher_probability)
                    person["prayer_group_type"] = random.choice(self.prayer_group_types)
                    int_prayer = random.choice(self.bool_higher_probability)

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
                if int_work == 1:
                    person["work_type"] = random.choice(self.work_types)
                    person["int_work"] = int_work
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
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["Grade-school_1"]) & merged_df["day_of_week"].isin(self.grade_1_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["Grade-school_2"]) & merged_df["day_of_week"].isin(self.grade_2_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["Grade-school_3"]) & merged_df["day_of_week"].isin(self.grade_3_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.grade_school) & merged_df["school_type"].isin(["Grade-school_4"]) & merged_df["day_of_week"].isin(self.grade_4_days), "in_school"] = 1
        """
        Middle-School attendance
        """
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["Middle-school_1"]) & merged_df["day_of_week"].isin(self.middle_1_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["Middle-school_2"]) & merged_df["day_of_week"].isin(self.middle_2_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["Middle-school_3"]) & merged_df["day_of_week"].isin(self.middle_3_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.middle_school) & merged_df["school_type"].isin(["Middle-school_4"]) & merged_df["day_of_week"].isin(self.middle_4_days), "in_school"] = 1
        """
        High-School attendance
        """
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["High-school_1"]) & merged_df["day_of_week"].isin(self.higher_1_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["High-school_2"]) & merged_df["day_of_week"].isin(self.higher_2_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["High-school_3"]) & merged_df["day_of_week"].isin(self.higher_3_days), "in_school"] = 1
        merged_df.loc[merged_df["age"].isin(self.high_school) & merged_df["school_type"].isin(["High-school_4"]) & merged_df["day_of_week"].isin(self.higher_4_days), "in_school"] = 1

        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["day_of_week"].isin(self.weekends), "in_school"] = 0

        """
        Other activities
        """
        # 1. Volunteering
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["volunteer_type_1"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_1_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["volunteer_type_2"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_1_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["volunteer_type_3"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_1_days)), "volunteering"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_volunteering_age) & merged_df["volunteering_type"].isin(["volunteer_type_4"]) & merged_df["int_volunteering"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_1_days)), "volunteering"] = 1

        # 2. Sports
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["play_sports_1"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_2_days)), "play_sports"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["play_sports_2"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_2_days)), "play_sports"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["play_sports_3"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "play_sports"] = 1
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["sports_type"].isin(["play_sports_4"]) & merged_df["int_play_sports"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "play_sports"] = 1

        # 3. Prayer Group
        merged_df.loc[merged_df["age"].isin(self.children_not_toddlers) & merged_df["prayer_group_type"].isin(self.prayer_group_types) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(self.weekends), "prayer_group"] = 1

        """
        ADULTS - General conditions
        """
        merged_df.loc[merged_df["age"] > 18, "in_school"] = 0
        merged_df.loc[merged_df["person_id"].isin(self.store_visitors.values()) & merged_df["has_dog"].isin([1]) & merged_df["int_dog_walk"].isin([1]) & merged_df["dog_walk_type"].isin(self.dog_walk_types), "dog_walk"] = 1

        """
        General activities of adults
        """
        merged_df.loc[merged_df["age"] > 70, ["attend_work", "play_sports"]] = [0, 0]

        # Work
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["attend_work_1"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.grade_1_days, self.higher_2_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["attend_work_2"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.middle_1_days, self.middle_2_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["attend_work_3"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.higher_1_days, self.grade_1_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["attend_work_4"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.higher_3_days, self.grade_3_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["attend_work_5"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.middle_4_days, self.higher_4_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["attend_work_6"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.grade_3_days, self.middle_3_days)), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_to60) & merged_df["work_type"].isin(["attend_work_7"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.grade_4_days, self.higher_2_days)), "attend_work"] = 1

        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["attend_work_1"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.grade_3_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["attend_work_2"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.higher_3_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["attend_work_3"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.middle_1_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["attend_work_4"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.middle_4_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["attend_work_5"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.grade_4_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["attend_work_6"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.higher_2_days), "attend_work"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["work_type"].isin(["attend_work_7"]) & merged_df["int_work"].isin([1]) & merged_df["day_of_week"].isin(self.grade_2_days), "attend_work"] = 1


        # Prayer group
        # Above 70 years
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["prayer_group_type_1"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_1_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["prayer_group_type_2"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["prayer_group_type_3"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_3_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f70) & merged_df["prayer_group_type"].isin(["prayer_group_type_4"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_4_days)), "prayer_group"] = 1

        # Above 60 and below 70
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["prayer_group_type_1"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_grade_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["prayer_group_type_2"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_middle_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["prayer_group_type_3"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_2_days)), "prayer_group"] = 1
        merged_df.loc[merged_df["age"].isin(self.adults_f60_t70) & merged_df["prayer_group_type"].isin(["prayer_group_type_4"]) & merged_df["int_prayer"].isin([1]) & merged_df["day_of_week"].isin(set.union(self.weekends, self.not_higher_4_days)), "prayer_group"] = 1

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
    start = time.time()
    pop = PopulationGen()

    current_date_df, dob_adult_set, dob_children_set = pop.create_dates()

    families_df = pop.initialize_families()
    families_df = families_df.replace(np.nan, 0)

    people_df = pop.initialize_people(families_df, dob_adult_set, dob_children_set)
    people_df = people_df.replace(np.nan, 0)

    fully_merged_df = pop.combine_families_date(families_df, current_date_df, people_df)
    fully_merged_df = pop.generate_attributes(fully_merged_df)
    current_date_df.to_csv("../Results/dates.csv", index=False)
    families_df.to_csv("../Results/family.csv", index=False)
    people_df.to_csv("../Results/people.csv", index=False)
    fully_merged_df = fully_merged_df.replace(np.nan, 0)
    fully_merged_df["work_type"].replace(0, "No-work")
    fully_merged_df["volunteering_type"].replace(0, "No-volunteering")
    fully_merged_df["prayer_group_type"].replace(0, "No-prayer")
    fully_merged_df["sports_type"].replace(0, "No-sports")
    fully_merged_df["dog_walk_type"].replace(0, "No-dog")
    fully_merged_df.to_csv("../Results/merged.csv", index=False)
    print("Total time taken:", (time.time() - start)/60)