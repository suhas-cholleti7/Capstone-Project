import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import json
from datetime import timedelta, datetime
import pandas as pd
low_memory=False

def date_creator():
    """
    To create the list of dates
    :return: The date list, the number of days between dates and the start date
    """
    start_date = datetime(2020, 1, 1).date()
    end_date = datetime(2020, 3, 15).date()
    delta_dates = end_date - start_date
    day_list = []
    for i in range(delta_dates.days + 1):
        day_list.append(start_date + timedelta(days=i))
    return day_list, delta_dates, start_date


def cumulative_infections(newly_infected, type):
    day_list, delta_dates, start_date = date_creator()

    newly_infected_data = json.load(newly_infected)
    newly_infected_data_rearranged = dict()
    day_counter = 1
    # if type == "Birthdays":
    for _date in day_list:
        if str(_date) in newly_infected_data:
            newly_infected_data_rearranged[day_counter] = newly_infected_data[str(_date)]
        # else:
            # newly_infected_data_rearranged[day_counter] = 0
        day_counter += 1
    # else:
    #     for i in range(delta_dates.days + 1):
    #         if str(day_counter) in newly_infected_data:
    #             newly_infected_data_rearranged[day_counter] = newly_infected_data[str(day_counter)]
    #         else:
    #             newly_infected_data_rearranged[day_counter] = 0
    #         day_counter += 1

    infect_list = [(k, v) for k, v in newly_infected_data_rearranged.items()]
    infection_days = np.array([z[0] for z in infect_list])
    infection_count = np.array([z[1] for z in infect_list])

    X_Y_inf = make_interp_spline(infection_days, infection_count)
    X_inf = np.linspace(infection_days.min(), infection_days.max(), 500)
    Y_inf = X_Y_inf(X_inf)

    color_dict = {"Work and School": "r", "Birthday Parties": "b", "Groups of Family Friends": "g", "One Family Group Per Week": "m", "Lockdown": "c",
                  "After Vaccinating 70%": "darkorange"}

    # Plotting the graphs
    plt.plot(X_inf, Y_inf, color_dict[type], label=type, linewidth=5)
    plt.xticks(np.arange(min(X_inf), max(X_inf) + 1, 5.0))
    plt.tick_params(labelsize=12)
    return newly_infected_data_rearranged


def convert_process(dict_data):
    day_list, delta_dates, start_date = date_creator()

    infected_data = json.load(dict_data)
    infected_data_rearranged = dict()
    day_counter = 1
    # if type == "Birthdays":
    for _date in day_list:
        if str(_date) in infected_data:
            infected_data_rearranged[day_counter] = infected_data[str(_date)]
        else:
            infected_data_rearranged[day_counter] = 0
        day_counter += 1
    # else:
    #     for i in range(delta_dates.days + 1):
    #         if str(day_counter) in newly_infected_data:
    #             newly_infected_data_rearranged[day_counter] = newly_infected_data[str(day_counter)]
    #         else:
    #             newly_infected_data_rearranged[day_counter] = 0
    #         day_counter += 1

    # infect_list = [(k, v) for k, v in infected_data_rearranged.items()]
    # infection_days = np.array([z[0] for z in infect_list])
    # infection_count = np.array([z[1] for z in infect_list])
    return infected_data_rearranged


def per_capita_infections(type, newly_infected, death_dict, recovery):

    death_df = convert_process(death_dict)
    death_df_info = pd.DataFrame(death_df.items(), columns=["Day", "Dead"])
    recovery_df = convert_process(recovery)
    recovery_df_info = pd.DataFrame(recovery_df.items(), columns=["Day", "Recovered"])

    plt.figure(figsize=(16, 9), dpi=1080)

    per_capita_infections_days = newly_infected["Day"]
    per_capita_infections_count = newly_infected["Infected"]

    recovery_days = recovery_df_info["Day"]
    recovery_count = recovery_df_info["Recovered"]

    death_days = death_df_info["Day"]
    death_count = death_df_info["Dead"]

    # X_Y_inf = make_interp_spline(infection_days, infection_count)
    # X_inf = np.linspace(infection_days.min(), infection_days.max(), 500)
    # Y_inf = X_Y_inf(X_inf)
    # x_ticks = [x for x in per_capita_infections_days if x % 5 == 0]
    # print(x_ticks)
    plt.fill_between(per_capita_infections_days, per_capita_infections_count, color="b", alpha=0.6,
                     label='New Infections')
    plt.fill_between(recovery_days, recovery_count, color="r", alpha=0.6, label='Recovered')
    plt.fill_between(death_days, death_count, color="y", alpha=0.6, label='Death')
    # if type == "Vaccinations":
    #     plt.plot(vax_days, vax_count, color='g', alpha=0.5, label='Vaccination')
    plt.legend(loc="right")
    plt.title("Infections vs. Days: " + type)
    plt.xlabel("No. of days")
    plt.ylabel("No. of infections")
    plt.savefig("../Results/Graphs/Per_Capita_" + type + ".png")
    plt.show()



if __name__ == '__main__':
    date_creator()

    plt.figure(figsize=(21, 10), dpi=300)

    # Birthdays
    infected_birthdays = open("../Results/Data/Birthdays/infections.json")
    infected_data_rearranged_bir = cumulative_infections(infected_birthdays, "Birthday Parties")

    # Friends
    friends_many_infected = open('../Results/Data/Friends/infections_1.json')
    infected_data_rearranged_frnd = cumulative_infections(friends_many_infected, "Groups of Family Friends")

    # Friends Only One
    friends_one_infected = open('../Results/Data/Friends_Ltd/infections_1.json')
    infected_data_rearranged_frnd_lim = cumulative_infections(friends_one_infected, "One Family Group Per Week")

    # General
    infected_general = open("../Results/Data/General/infections.json")
    infected_data_rearranged_gen = cumulative_infections(infected_general, "Work and School")

    # Complete Lockdown
    complete_lockdown_infected = open('../Results/Data/Lockdown/infections.json')
    infected_data_rearranged_lockdown = cumulative_infections(complete_lockdown_infected, "Lockdown")

    # # Vaccinations - 1
    # vaccinated_infected = open('../Results/Data/Vax/bday_infections_all_1.json')
    # infected_data_rearranged_vax_1 = cumulative_infections(vaccinated_infected, "Vaccinated-1")

    # # Vaccinations - 2
    # vaccinated_infected = open('../Results/Data/Vax/bday_infections_all_2.json')
    # infected_data_rearranged_vax_2 = cumulative_infections(vaccinated_infected, "Vaccinated-2")

    # Vaccinations - 3
    vaccinated_infected = open('../Results/Data/Vax/bday_infections_all_3.json')
    infected_data_rearranged_vax_3 = cumulative_infections(vaccinated_infected, "After Vaccinating 70%")

    # # Non-Responsible Vaccinated-2
    # non_resp_vaccinated_infected = open('../Results/Data/Vax_Not_Resp/bday_infections_irresponsible_1.json')
    # infected_data_rearranged_non_resp_vax = cumulative_infections(non_resp_vaccinated_infected, "Non-Responsible People Vaccinated")

    plt.title("Cumulative Infections for All Scenarios: COVID-19", fontsize=20)
    plt.ylabel("No. of people infected", fontsize=15)
    plt.xlabel("No. of days", fontsize=15)
    plt.legend(loc="upper center", fontsize=14, bbox_to_anchor = (0.5, -0.075), fancybox=True, ncol=6)
    # plt.tight_layout()
    # plt.show()
    plt.savefig('../Results/Graphs/Infections_1.png')

    # For vaccinations
    plt.figure(figsize=(21, 9), dpi=300)

    # Birthdays
    infected_birthdays = open("../Results/Data/Birthdays/infections.json")
    infected_data_rearranged_bir_sep = cumulative_infections(infected_birthdays, "Birthday Parties")

    # Vaccinations - 3
    vaccinated_infected = open('../Results/Data/Vax/bday_infections_all_3.json')
    infected_data_rearranged_vax_3_sep = cumulative_infections(vaccinated_infected, "After Vaccinating 70%")

    # To draw the plots
    plt.title("Cumulative Infections for Vaccinations and Birthdays: COVID-19", fontsize=20)
    plt.ylabel("No. of people infected", fontsize=15)
    plt.xlabel("No. of days", fontsize=15)
    plt.legend(loc="center right", fontsize=14)
    plt.savefig('../Results/Graphs/Vaccinations_vs_Birthdays.png')



