import time
import numpy as np
from faker import Faker
import pandas as pd
from datetime import date, timedelta, datetime
import random
import collections


class Populator:
    def __init__(self):
        self.NO_OF_PEOPLE = 36000
        self.counter = 1
        self.bool_values = [0, 1]
        self.bool_higher_probability = [0, 0, 1, 1, 0, 1, 1, 1, 1, 1]
        self.bool_lower_probability = [1, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        self.family_size_list = (1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6)
        self.gender = ["M", "F"]
        self.family_data = collections.defaultdict(set)
        self.weekends = {"Saturday", "Sunday"}
        self.weekdays = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
        self.grade_days = {"Monday", "Wednesday", "Friday"}
        self.not_grade_days = {"Tuesday", "Thursday"}
        self.middle_days = {"Tuesday", "Thursday", "Monday"}
        self.not_middle_days = {"Wednesday", "Friday"}
        self.higher_days = {"Tuesday", "Friday", "Monday"}
        self.not_higher_days = {"Wednesday", "Thursday"}
        self.toddlers = set([age for age in range(0, 5)])
        self.grade_school = set([age for age in range(5, 12)])
        self.middle_school = set([age for age in range(12, 15)])
        self.high_school = set([age for age in range(16, 19)])
        self.children = set([age for age in range(0, 19)])
        self.children_not_toddlers = set([age for age in range(5, 19)])
        self.adults = set([age for age in range(19, 100)])
        self.adults_to60 = set([age for age in range(19, 61)])
        self.adults_f60_t70 = set([age for age in range(61, 71)])
        self.adults_f70 = set([age for age in range(71, 100)])
        random.seed(10)

    def create_dates(self):
        """
        To create the date of birth and the current date fields
        :return: Dataframes with dates for the two roles
        """
        # Current date dataframe from 1/1/2020 to 1/1/2021
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        delta = end_date - start_date
        current_date_list = []

        for i in range(delta.days + 1):
            # Monday is 0, Sunday is 6
            c_date = start_date + timedelta(days=i)
            day_of_week = c_date.weekday()
            current_date_list.append({"date": c_date, "day_of_week": weekdays[day_of_week]})
        current_date_df = pd.DataFrame(current_date_list)
        # current_date_df.insert(0, 'date_ID', range(1, 1 + len(current_date_df)))

        # Date of birth fields
        # For Adults - from Jan 1st 1930 to Jan 1st 2003
        start_date = date(1940, 1, 1)
        end_date = date(2003, 1, 1)
        dob_adult_set = set()
        vaccination_list = []
        no_of_adults = int(0.65 * self.NO_OF_PEOPLE)
        for d in range(no_of_adults):
            dob_adult_set.add(faker.date_between_dates(start_date, end_date))

        # For Children
        start_date = date(2003, 1, 1)
        end_date = date(2021, 1, 1)
        dob_children_set = set()
        no_of_children = int(0.35 * self.NO_OF_PEOPLE)
        for d in range(no_of_children):
            dob_children_set.add(faker.date_between_dates(start_date, end_date))

        # Date of vaccination
        start_date = date(2020, 1, 1)
        end_date = date(2021, 1, 1)
        pd.date_range(start_date, end_date - timedelta(days=1), freq='d')
        # for d in range(NO_OF_PEOPLE):
        #   vaccination_list.append(faker.date_between_dates(start_date, end_date))

        return dob_adult_set, dob_children_set, current_date_df

    def people_filler(self, dob_adult_set, dob_children_set, family_size, person_list, fam_id):
        """
        Function to fill in the data for the attributes for individual members of the society
        :param dob_adult_set: Set of adults' date of birth
        :param dob_children_set: Set of children's date of birth
        :param family_size: Set of size of the families
        :param person_list: List to contain the data for each individual
        :param fam_id: Initial family ID value
        :return: None
        """
        rem_size = 0
        if family_size > 2:
            rem_size = family_size - 2
            family_size = 2
        mask_choice = random.choice(self.bool_values)
        """
        To generate the family and the adults in the family
        """
        for size in range(family_size):
            if self.counter == self.NO_OF_PEOPLE + 1:
                return
            single_doc = dict()
            single_doc["person_id"] = self.counter
            single_doc["fam_id"] = fam_id
            single_doc["gender"] = random.choice(self.gender)
            dob_adult_val = random.choice(list(dob_adult_set))
            single_doc["dob"] = dob_adult_val.strftime("%x")
            single_doc["age"] = abs(date.today().year - dob_adult_val.year)
            single_doc["has_dog"] = random.choice(self.bool_values)
            if single_doc["has_dog"] == 1:
                single_doc["dog_walk"] = random.choice(self.bool_higher_probability)
            else:
                single_doc["dog_walk"] = 0
            single_doc["mask"] = mask_choice
            person_list.append(single_doc)
            self.counter += 1
            # TODO: Enter in the vaccination_date
            # single_doc["vaccinated"] = random.choice(self.bool_values)
            # if single_doc["vaccinated"] == 1:
            #   pass

        """
        To generate the children in the family
        """
        for size in range(rem_size):
            if self.counter == self.NO_OF_PEOPLE + 1:
                break
            single_doc = dict()
            single_doc["person_id"] = self.counter
            single_doc["fam_id"] = fam_id
            single_doc["gender"] = random.choice(self.gender)
            dob_children_val = random.choice(list(dob_children_set))
            single_doc["dob"] = dob_children_val.strftime("%x")
            single_doc["age"] = abs(date.today().year - dob_children_val.year)
            single_doc["has_dog"] = 0
            single_doc["dog_walk"] = 0
            single_doc["mask"] = mask_choice
            if 0 <= single_doc["age"] <= 4:
                single_doc["school_type"] = "Toddlers"
            elif 5 <= single_doc["age"] <= 11:
                single_doc["school_type"] = "Grade-school"
            elif 12 <= single_doc["age"] <= 15:
                single_doc["school_type"] = "Middle-school"
            elif 16 <= single_doc["age"] <= 18:
                single_doc["school_type"] = "High-school"
            person_list.append(single_doc)
            self.counter += 1
            # TODO: Enter in the vaccination_date
            # single_doc["vaccinated"] = random.choice(self.bool_values)
            # if single_doc["vaccinated"] == 1:
            #   pass
        fam_id += 1

    def person_data(self, dob_adult_set, dob_children_set):
        """
        To initiate the generation of data of individuals in the city
        :param dob_adult_set: Set of adults' date of birth
        :param dob_children_set: Set of children's date of birth
        :return: People data frame
        """
        person_list = []
        fam_id = 1
        for no in range(self.NO_OF_PEOPLE):
            family_size = random.choice(self.family_size_list)
            self.people_filler(dob_adult_set, dob_children_set, family_size, person_list, fam_id)
            fam_id += 1
            if self.counter == self.NO_OF_PEOPLE:
                break
        people_df = pd.DataFrame(person_list)
        return people_df

    def process_fields_with_date(self, all_fields_df):
        """
        Imputing data to many attributes pertaining to the age of individuals
        :param all_fields_df: The merged dataframe that contains the date and individuals' data
        :return: None
        """
        """
        ADULTS:
        """
        all_fields_df.loc[all_fields_df["age"] > 18, ["school_type", "in_school"]] = ["No-School", 0]
        print("Im here - 178")

        """
        Weekday activities of adults
        """
        all_fields_df.loc[all_fields_df["age"] > 70, ["attend_work", "prayer_group", "play_sports", "volunteering"]] = [0, random.choice(self.bool_values), 0, random.choice(self.bool_values)]
        all_fields_df.loc[all_fields_df["age"].isin(self.adults_to60) & all_fields_df["day_of_week"].isin(self.weekdays), ["attend_work", "prayer_group", "play_sports", "volunteering"]] = [random.choice(self.bool_higher_probability), random.choice(self.bool_lower_probability), random.choice(self.bool_lower_probability), 0]
        # all_fields_df.loc[((all_fields_df["age"] > 18) & (all_fields_df["age"] < 60) & (all_fields_df["day_of_week"].isin(self.weekdays))), ["attend_work", "prayer_group","play_sports", "volunteering"]] = [random.choice(self.bool_higher_probability), random.choice(self.bool_lower_probability), random.choice(self.bool_lower_probability), 0]
        all_fields_df.loc[all_fields_df["age"].isin(self.adults_f60_t70) & all_fields_df["day_of_week"].isin(self.weekdays), ["attend_work", "prayer_group", "play_sports", "volunteering"]] = [random.choice(self.bool_values), random.choice(self.bool_higher_probability), 0, 0]
        print("Im here - 183")

        """
        Weekend activities of adults
        """
        all_fields_df.loc[all_fields_df["age"].isin(self.adults_to60) & all_fields_df["day_of_week"].isin(self.weekends), ["attend_work", "prayer_group", "play_sports", "volunteering"]] = [0, random.choice(self.bool_values), random.choice(self.bool_values), random.choice(self.bool_higher_probability)]
        all_fields_df.loc[all_fields_df["age"].isin(self.adults_f60_t70) & all_fields_df["day_of_week"].isin(self.weekends), ["attend_work", "prayer_group", "play_sports", "volunteering"]] = [0, random.choice(self.bool_higher_probability), random.choice(self.bool_lower_probability), random.choice(self.bool_lower_probability)]
        print("Im here - 187")

        """
        CHILDREN
        """
        all_fields_df.loc[all_fields_df["age"] < 19, "in_school"] = 0
        all_fields_df.loc[all_fields_df["age"] <= 4, ["school_type", "attend_work", "prayer_group", "play_sports", "volunteering", "in_school"]] = ["Toddlers", 0, 0, 0, 0, 0]
        print("Im here - 198")

        """
        Grade-School attendance
        """
        all_fields_df.loc[all_fields_df["age"].isin(self.grade_school) & all_fields_df["day_of_week"].isin(self.grade_days), ["school_type", "in_school"]] = ["Grade-school", 1]
        # all_fields_df.loc[all_fields_df["age"].isin(self.grade_school) & all_fields_df["day_of_week"].isin(self.not_grade_days), ["school_type", "in_school"]] = ["Grade-school", 0]

        """
        Middle-School attendance
        """
        all_fields_df.loc[all_fields_df["age"].isin(self.middle_school) & all_fields_df["day_of_week"].isin(self.middle_days), ["school_type", "in_school"]] = ["Middle-school", 1]
        print("Im here - 204")
        # all_fields_df.loc[all_fields_df["age"].isin(self.middle_school) & all_fields_df["day_of_week"].isin(self.not_middle_days), ["school_type", "in_school"]] = ["Middle-school", 0]

        """
        High-School attendance
        """
        all_fields_df.loc[all_fields_df["age"].isin(self.high_school) & all_fields_df["day_of_week"].isin(self.higher_days), ["school_type", "in_school"]] = ["High-school", 1]
        print("Im here - 208")
        # all_fields_df.loc[all_fields_df["age"].isin(self.high_school) & all_fields_df["day_of_week"].isin(self.not_higher_days), ["school_type", "in_school"]] = ["High-school", 0]
        # all_fields_df.loc[all_fields_df["age"].isin(self.grade_school), "school_type"] = "Grade-school"
        # all_fields_df.loc[all_fields_df["age"].isin(self.middle_school), "school_type"] = "Middle-school"
        # all_fields_df.loc[all_fields_df["age"].isin(self.high_school), "school_type"] = "High-school"
        all_fields_df.loc[all_fields_df["age"].isin(self.children_not_toddlers) & all_fields_df["day_of_week"].isin(self.weekdays), ["attend_work", "prayer_group", "play_sports", "volunteering"]] = [0, random.choice(self.bool_values), random.choice(self.bool_higher_probability), 0]
        print("Im here - 214")
        all_fields_df.loc[all_fields_df["age"].isin(self.children_not_toddlers) & all_fields_df["day_of_week"].isin(self.weekends), ["attend_work", "prayer_group", "play_sports", "volunteering", "in_school"]] = [0, random.choice(self.bool_higher_probability), 1, random.choice(self.bool_values), 0]
        print("Im here - 216")
        # all_fields_df.loc[(all_fields_df["school_type"] == "Grade-school") & (all_fields_df["day_of_week"] in ("Monday", "Wednesday", "Friday")), "in_school"] = 1
        # all_fields_df.loc[(all_fields_df["school_type"] == "Grade-school") & (all_fields_df["day_of_week"] in ("Monday", "Wednesday", "Friday")), "in_school"] = 1
        # all_fields_df.loc[(all_fields_df["school_type"] == "Grade-school") & (all_fields_df["day_of_week"] not in ("Monday", "Wednesday", "Friday")), "in_school"] = 0
        # all_fields_df.loc[(all_fields_df["school_type"] == "Middle-school") & (all_fields_df["day_of_week"] in ("Tuesday", "Thursday", "Monday")), "in_school"] = 1
        # all_fields_df.loc[(all_fields_df["school_type"] == "Middle-school") & (all_fields_df["day_of_week"] not in ("Tuesday", "Thursday", "Monday")), "in_school"] = 0
        # all_fields_df.loc[(all_fields_df["school_type"] == "High-school") & (all_fields_df["day_of_week"] in ("Tuesday", "Friday", "Monday")), "in_school"] = 1
        # all_fields_df.loc[(all_fields_df["school_type"] == "High-school") & (all_fields_df["day_of_week"] not in ("Tuesday", "Friday", "Monday")), "in_school"] = 0









        # for person in to_process:
        #     if person["age"] > 18:
        #         person["school_type"] = "No-School"#DONE
        #         person["in_school"] = 0#DONE
        #         if person["age"] > 70:#DONE
        #             person["attend_work"] = 0#DONE
        #             person["prayer_group"] = random.choice(self.bool_values)#DONE
        #             person["play_sports"] = 0#DONE
        #             person["volunteering"] = random.choice(self.bool_values)#DONE
        #         else:
        #             if person["day_of_week"] not in ("Saturday", "Sunday"):
        #                 if 60 < person["age"] < 70:
        #                     person["attend_work"] = random.choice(self.bool_values)#DONE
        #                 else:
        #                     person["attend_work"] = random.choice(self.bool_higher_probability)#DONE
        #                 person["prayer_group"] = random.choice(self.bool_values)#DONE
        #                 person["play_sports"] = random.choice(self.bool_values)#DONE
        #                 person["volunteering"] = 0#DONE
        #             else:
        #                 person["attend_work"] = 0#DONE
        #                 person["prayer_group"] = random.choice(self.bool_higher_probability)#DONE
        #                 person["play_sports"] = random.choice(self.bool_higher_probability)#DONE
        #                 person["volunteering"] = random.choice(self.bool_values)#DONE
        #     else:
        #         if 0 <= person["age"] <= 4:
        #             person["school_type"] = "Toddlers"#DONE
        #         elif 5 <= person["age"] <= 11:
        #             person["school_type"] = "Grade-school"#DONE
        #         elif 12 <= person["age"] <= 15:
        #             person["school_type"] = "Middle-school"#DONE
        #         elif 16 <= person["age"] <= 18:
        #             person["school_type"] = "High-school"#DONE
        #         if person["age"] < 5:
        #             person["attend_work"] = 0#DONE
        #             person["prayer_group"] = 0#DONE
        #             person["play_sports"] = 0#DONE
        #             person["volunteering"] = 0#DONE
        #             person["in_school"] = 0#DONE
        #         elif person["age"] >= 5:
        #             if person["day_of_week"] not in ("Saturday", "Sunday"):
        #                 person["attend_work"] = 0#DONE
        #                 person["prayer_group"] = random.choice(self.bool_values)#DONE
        #                 person["play_sports"] = random.choice(self.bool_higher_probability)#DONE
        #                 person["volunteering"] = 0#DONE
        #                 if person["school_type"] == "Grade-school" and person["day_of_week"] in (
        #                         "Monday", "Wednesday", "Friday"):
        #                     person["in_school"] = 1#DONE
        #                 else:
        #                     person["in_school"] = 0#DONE
        #                 if person["school_type"] == "Middle-school" and person["day_of_week"] in (
        #                         "Tuesday", "Thursday", "Monday"):
        #                     person["in_school"] = 1#DONE
        #                 else:
        #                     person["in_school"] = 0#DONE
        #                 if person["school_type"] == "High-school" and person["day_of_week"] in (
        #                         "Tuesday", "Friday", "Monday"):
        #                     person["in_school"] = 1#DONE
        #                 else:
        #                     person["in_school"] = 0#DONE
        #             else:
        #                 person["attend_work"] = 0
        #                 person["prayer_group"] = random.choice(self.bool_higher_probability)
        #                 person["play_sports"] = 1
        #                 person["volunteering"] = random.choice(self.bool_values)
        #                 person["in_school"] = 0




        to_process = all_fields_df.to_dict('index').values()
        print("Im here - 301")

        """
        To impute the values for grocery and gasoline quantities
        """
        family_id_set = set()
        for family in to_process:
            if family["fam_id"] not in self.family_data:
                self.family_data[family["fam_id"]] = {(family["person_id"], family["age"])}
            else:
                if family["person_id"] not in self.family_data[family["fam_id"]]:
                    self.family_data[family["fam_id"]].add((family["person_id"], family["age"]))

            if family["fam_id"] not in family_id_set and family["date"].month == 1:
                family["grocery_qty"] = random.randrange(1, 10)
                family["gasoline_qty"] = random.randrange(1, 8)
                family_id_set.add(family["fam_id"])
        print("Im here - 313")
        #
        # family_grocery_dict = dict()
        # family_gas_dict = dict()
        # person_id_set = set()
        # final_merged_df = all_fields_df

        # family_grocery_dict[final_merged_df["fam_id"]] = final_merged_df.loc[np.where(~final_merged_df["fam_id"]).isin(family_grocery_dict) & (final_merged_df["date"] == datetime(2020, 1, 1).date()) & (~final_merged_df["grocery_qty"].isin(None)) & (~final_merged_df["person_id"]).isin(person_id_set), final_merged_df["grocery_qty"], ]

        final_merged_df = pd.DataFrame(to_process)
        print("Im here - 322")
        family_grocery_dict = dict()
        family_gas_dict = dict()
        person_id_set = set()
        for index, family in final_merged_df.iterrows():
            if family["fam_id"] not in family_grocery_dict and family["date"] == datetime(2020, 1, 1).date() \
                    and family["grocery_qty"] is not None and family["person_id"] not in person_id_set:
                family_grocery_dict[family["fam_id"]] = family["grocery_qty"]
                person_id_set.add(family["person_id"])
            elif family["fam_id"] in family_grocery_dict and family["date"] == datetime(2020, 1, 1).date() \
                    and family["person_id"] not in person_id_set:
                person_id_set.add(family["person_id"])
                final_merged_df.loc[(final_merged_df["fam_id"] == family["fam_id"])
                            & (final_merged_df["person_id"] == family["person_id"])
                            & (final_merged_df["date"] == datetime(2020, 1, 1).date()), "grocery_qty"] = family_grocery_dict[family["fam_id"]]
        print("Im here - 337")
        person_id_set.clear()
        block_start_time = time.time()
        for index, family in final_merged_df.iterrows():
            if family["fam_id"] not in family_gas_dict and family["date"] == datetime(2020, 1, 1).date() \
                    and family["gasoline_qty"] is not None and family["person_id"] not in person_id_set:
                family_gas_dict[family["fam_id"]] = family["gasoline_qty"]
                person_id_set.add(family["person_id"])
            elif family["fam_id"] in family_gas_dict and family["date"] == datetime(2020, 1, 1).date() \
                    and family["person_id"] not in person_id_set:
                person_id_set.add(family["person_id"])
                final_merged_df.loc[(final_merged_df["fam_id"] == family["fam_id"])
                            & (final_merged_df["person_id"] == family["person_id"])
                            & (final_merged_df["date"] == datetime(2020, 1, 1).date()), "gasoline_qty"] = family_gas_dict[family["fam_id"]]
        print("Time for this block:", (time.time()-block_start_time)/60)
        print("Im here - 350")

        """
        To impute the grocery and the gasoline quantities
        """
        for i in range(0, len(final_merged_df)):
            if final_merged_df.loc[i, "date"] != datetime(2020, 1, 1).date():
                final_merged_df.loc[i, "grocery_qty"] = final_merged_df.loc[i - 1, "grocery_qty"] - 1
                if final_merged_df.loc[i, "grocery_qty"] == 0:
                    final_merged_df.loc[i, "grocery_qty"] = 9
        print("Im here - 358")
        for i in range(0, len(final_merged_df)):
            if final_merged_df.loc[i, "date"] != datetime(2020, 1, 1).date():
                final_merged_df.loc[i, "gasoline_qty"] = final_merged_df.loc[i-1, "gasoline_qty"] - 1
                if final_merged_df.loc[i, "gasoline_qty"] == 0:
                    final_merged_df.loc[i, "gasoline_qty"] = 7
        print("Im here - 366")

        """
        To update the grocery store and gas station visits
        """
        final_merged_df.loc[(final_merged_df["grocery_qty"] == 9) & (18 < final_merged_df["age"]), "grocery_visit"] = 1
        final_merged_df.loc[final_merged_df["grocery_visit"] != 1, "grocery_visit"] = 0

        final_merged_df.loc[(final_merged_df["gasoline_qty"] == 7) & (18 < final_merged_df["age"]), "gasoline_visit"] = 1
        final_merged_df.loc[final_merged_df["gasoline_visit"] != 1, "gasoline_visit"] = 0
        final_merged_df["exposed"] = 0
        final_merged_df["quarantined"] = 0
        print("Im here - 371")
        final_merged_df.to_csv("merged.csv", sep=",", index_label='data_key')


if __name__ == '__main__':
    start = time.time()
    faker = Faker()
    pop = Populator()
    dob_adult_set, dob_children_set, current_date_df = pop.create_dates()
    people_df = pop.person_data(dob_adult_set, dob_children_set)
    current_date_df["key"] = 1
    people_df["key"] = 1
    merged_df = pd.merge(people_df, current_date_df, on="key").drop("key", 1)
    pop.process_fields_with_date(merged_df)
    print("Time taken to run this code:", (time.time()-start)/60)