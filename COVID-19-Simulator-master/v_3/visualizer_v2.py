import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import json
from datetime import timedelta, datetime
import pandas as pd
low_memory=False


def calculate_moving_averages(infection_count):
    """
    To calculate the moving averages for the infection count
    :param infection_count: The infection_count list
    :return: The infection_count moving averages list
    """
    window_size = 3
    numbers_series = pd.Series(infection_count)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:]
    return without_nans

def date_creator():
    """
    To create the list of dates
    :return: The date list, the number of days between dates and the start date
    """
    start_date = datetime(2020, 1, 1).date()
    end_date = datetime(2020, 5, 31).date()
    delta_dates = end_date - start_date
    day_list = []
    for i in range(delta_dates.days + 1):
        day_list.append(start_date + timedelta(days=i))
    return day_list, delta_dates, start_date


def sir_emulation(susceptible, newly_infected, death_dict, recovery, vaccinations, type):
    """
    The method to plot the data for the SIR simulations. This method processes the data from the various dictionaries
    and based on type of the graph to be drawn.
    :param susceptible: The dictionary with data about the susceptible population
    :param newly_infected: The dictionary with data about the newly infected population
    :param death_dict: The dictionary with data about the population who have been removed
    :param recovery: The dictionary with data about the population who have recovered from the virus
    :param vaccinations: The dictionary with data about the population who have been vaccinated
    :param type: The type of plot to be plotted
    :return: None
    """
    day_list, delta_dates, start_date = date_creator()
    susceptible_data = json.load(susceptible)
    if type == "Birthdays":
        susceptible_data_rearranged = dict()
        day_counter = 1
        for _date in day_list:
            if str(_date) in susceptible_data:
                susceptible_data_rearranged[day_counter] = susceptible_data[str(_date)]
            else:
                susceptible_data_rearranged[day_counter] = 0
            day_counter += 1
        susceptible_data_rearranged = {int(k): int(v) for k, v in susceptible_data_rearranged.items()}
    else:
        susceptible_data_rearranged = {int(k): int(v) for k, v in susceptible_data.items()}
    sus_list = [(k, v) for k, v in susceptible_data_rearranged.items()]


    recovery_data = json.load(recovery)
    recovery_data_rearranged = dict()
    day_counter = 1
    for _date in day_list:
        if str(_date) in recovery_data:
            recovery_data_rearranged[day_counter] = recovery_data[str(_date)]
        else:
            recovery_data_rearranged[day_counter] = 0
        day_counter += 1

    rec_list = [(k, v) for k, v in recovery_data_rearranged.items()]

    newly_infected_data = json.load(newly_infected)
    newly_infected_data_rearranged = dict()
    day_counter = 1
    if type == "Birthdays":
        for _date in day_list:
            if str(_date) in newly_infected_data:
                newly_infected_data_rearranged[day_counter] = newly_infected_data[str(_date)]
            else:
                newly_infected_data_rearranged[day_counter] = 0
            day_counter += 1
    else:
        for i in range(delta_dates.days + 1):
            if str(day_counter) in newly_infected_data:
                newly_infected_data_rearranged[day_counter] = newly_infected_data[str(day_counter)]
            else:
                newly_infected_data_rearranged[day_counter] = 0
            day_counter += 1


    new_infect_list = [(k, v) for k, v in newly_infected_data_rearranged.items()]

    death_data = json.load(death_dict)
    death_data_rearranged = dict()
    day_counter = 1
    for _date in day_list:
        if str(_date) in death_data:
            death_data_rearranged[day_counter] = death_data[str(_date)]
        else:
            death_data_rearranged[day_counter] = 0
        day_counter += 1

    death_list = [(k, v) for k, v in death_data_rearranged.items()]

    # Arranging the susceptible dictionary
    susceptible_days = np.array([x[0] for x in sus_list])
    susceptible_count = np.array([x[1] for x in sus_list])

    # Arranging the recovered dictionary
    recovered_days = np.array([y[0] for y in rec_list])
    recovered_count = np.array([y[1] for y in rec_list])
    recovered_count = np.cumsum(recovered_count)

    # Arranging the infected population dictionary
    infection_days = np.array([z[0] for z in new_infect_list])
    infection_count = np.array([z[1] for z in new_infect_list])
    infection_count_mov = calculate_moving_averages(infection_count)
    infection_count_mov.insert(0, 0)
    infection_count_mov.insert(0, 0)

    # Arranging the removed population dictionary
    death_days = np.array([d[0] for d in death_list])
    death_count = np.array([d[1] for d in death_list])
    death_count = np.cumsum(death_count)

    X_Y_sus = make_interp_spline(susceptible_days, susceptible_count)
    X_sus = np.linspace(susceptible_days.min(), susceptible_days.max(), 500)
    Y_sus = X_Y_sus(X_sus)

    X_Y_rec = make_interp_spline(recovered_days, recovered_count)
    X_rec = np.linspace(recovered_days.min(), recovered_days.max(), 500)
    Y_rec = X_Y_rec(X_rec)

    X_Y_inf = make_interp_spline(infection_days, infection_count)
    X_inf = np.linspace(infection_days.min(), infection_days.max(), 500)
    Y_inf = X_Y_inf(X_inf)

    X_Y_deaths = make_interp_spline(death_days, death_count)
    X_death = np.linspace(death_days.min(), death_days.max(), 500)
    Y_death = X_Y_deaths(X_death)

    # Plotting the graphs
    plt.figure(figsize=(16, 9), dpi=80)
    plt.plot(X_sus, Y_sus, "b", label="Susceptible")
    plt.plot(X_inf, Y_inf, "r", label="Infected")
    plt.plot(X_rec, Y_rec, "g", label="Removed")
    # plt.plot(infection_days, infection_count_mov, "k", label="MA for Infected")
    plt.plot(X_death, Y_death, "y", label="Cumulative Deaths")
    plt.title("SIR graph: " + type)
    plt.ylabel("SIR populations")
    plt.xlabel("No. of days")
    plt.legend(loc="upper right")
    plt.savefig('../Results/Graphs/SIR_simulation_' + type +'.png')
    plt.show()


def per_capita_numbers(simulated_df, vaccination_dict, type):
    """
    To calculate the per capita numbers for the newly infected, removed and the recovered population
    :param simulated_df: The simulated dataframe
    :param vaccination_dict: The vaccinated dictionary
    :param type: The type of the graph to be plotted
    :return:
    """
    df_new_inf = simulated_df.groupby('date', as_index=False)['new_infection'].sum()
    df_death = simulated_df.groupby('date', as_index=False)['death'].sum()
    df_recovery = simulated_df.groupby('date', as_index=False)['recovery'].sum()

    df_new_inf["date"] = pd.to_datetime(df_new_inf['date'])
    df_death['date'] = pd.to_datetime(df_death['date'])
    df_recovery['date'] = pd.to_datetime(df_recovery['date'])

    # Arranging the newly infected data
    per_capita_new_infections_days = np.array([d for d in list(df_new_inf["date"])])
    per_capita_new_infections_days = np.array([i for i in range(len(per_capita_new_infections_days))])
    per_capita_new_infections_count = np.array([d for d in list(df_new_inf["new_infection"])])

    # Arranging the removed population data
    per_capita_death_days = np.array([d for d in list(df_death["date"])])
    per_capita_death_days = np.array([i for i in range(len(per_capita_death_days))])
    per_capita_death_count = np.array([d for d in list(df_death["death"])])

    # Arranging the recovered population data
    per_capita_recovery_days = np.array([d for d in list(df_recovery["date"])])
    per_capita_recovery_days = np.array([i for i in range(len(per_capita_recovery_days))])
    per_capita_recovery_count = np.array([d for d in list(df_recovery["recovery"])])

    # if type == "Vaccinations":
    #     day_list, delta_dates, start_date = date_creator()
    #     vax_data = json.load(vaccination_dict)
    #     vax_data_rearranged = dict()
    #     day_counter = 1
    #     for _date in day_list:
    #         if str(_date) in vax_data:
    #             vax_data_rearranged[day_counter] = vax_data[str(_date)]
    #         else:
    #             vax_data_rearranged[day_counter] = 0
    #         day_counter += 1
    #
    #     vax_list = [(k, v) for k, v in vax_data_rearranged.items()]
    #
    #     vax_days = np.array([x[0] for x in vax_list])
    #     vax_count = np.array([x[1] for x in vax_list])

    # Plotting the graphs for the per-capita data
    plt.figure(figsize=(16, 9), dpi=80)
    plt.fill_between(per_capita_new_infections_days, per_capita_new_infections_count, color="b", alpha=0.6, label='New Infections')
    plt.fill_between(per_capita_recovery_days, per_capita_recovery_count, color="r", alpha=0.6, label='Recovered')
    plt.fill_between(per_capita_death_days, per_capita_death_count, color="y", alpha=0.6, label='Death')
    # if type == "Vaccinations":
    #     plt.plot(vax_days, vax_count, color='g', alpha=0.5, label='Vaccination')
    plt.legend(loc="upper right")
    plt.title("Infections vs. Days: " + type)
    plt.xlabel("No. of days")
    plt.ylabel("No. of infections")
    plt.savefig("../Results/Graphs/Per_Capita_" + type + ".png")
    plt.show()


if __name__ == '__main__':
    # General
    susceptible = open('../Results/Data/General/susceptible_dict.json')
    newly_infected = open('../Results/Data/General/new_infection_date_dict.json')
    death_dict = open('../Results/Data/General/death_dict.json')
    recovery = open('../Results/Data/General/recovery_date_dict.json')
    sir_emulation(susceptible, newly_infected, death_dict, recovery, None, "General")
    simulated_results = pd.read_csv("../Results/Data/General/simulated_df.csv")
    per_capita_numbers(simulated_results, None, "General")

    # Friends
    birth_susceptible = open('../Results/Data/Birthdays/susceptible_bir_dict.json')
    birth_newly_infected = open('../Results/Data/Birthdays/new_infection_date_bir_dict.json')
    birth_death_dict = open('../Results/Data/Birthdays/death_bir_dict.json')
    birth_recovery = open('../Results/Data/Birthdays/recovery_date_bir_dict.json')
    sir_emulation(birth_susceptible, birth_newly_infected, birth_death_dict, birth_recovery, None, "Birthdays")
    bday_df = pd.read_csv("../Results/Data/Birthdays/birthday_final.csv")
    per_capita_numbers(bday_df, None, "Birthdays")

    # # Vaccinations
    # vax_susceptible = open('../Results/Data/Vax/susceptible_vax_dict.json')
    # vax_newly_infected = open('../Results/Data/Vax/new_infection_date_vax_dict.json')
    # vax_death_dict = open('../Results/Data/Vax/death_vax_dict.json')
    # vax_recovery = open('../Results/Data/Vax/recovery_date_vax_dict.json')
    # vax_vaccinations = open('../Results/Data/Vax/vaccinations_vax_dict.json')
    # sir_emulation(vax_susceptible, vax_newly_infected, vax_death_dict, vax_recovery, vax_vaccinations, "Vaccinations")
    # vax_df = pd.read_csv("../Results/Data/Vax/simulated_vax_df.csv")
    # per_capita_numbers(vax_df, vax_vaccinations, "Vaccinations")