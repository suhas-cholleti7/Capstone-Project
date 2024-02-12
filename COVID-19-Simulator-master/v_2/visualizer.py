import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import json
from datetime import timedelta, datetime
import pandas as pd
low_memory=False


def calculate_moving_averages(infection_count):
    window_size = 3
    numbers_series = pd.Series(infection_count)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:]
    return without_nans


def sir_emulation(susceptible, newly_infected, death_dict, recovery, type):
    susceptible_data = json.load(susceptible)
    susceptible_data_rearranged = {int(k): int(v) for k, v in susceptible_data.items()}
    sus_list = [(k, v) for k, v in susceptible_data_rearranged.items()]

    recovery_data = json.load(recovery)
    start_date = datetime(2020, 1, 1).date()
    end_date = datetime(2020, 12, 31).date()
    delta_dates = end_date - start_date
    day_list = []

    for i in range(delta_dates.days + 1):
        day_list.append(start_date + timedelta(days=i))
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
    for i in range(delta_dates.days + 1):
        if str(day_counter) in newly_infected_data:
            newly_infected_data_rearranged[day_counter] = newly_infected_data[str(day_counter)]
        else:
            newly_infected_data_rearranged[day_counter] = 0
        day_counter += 1

    new_infect_list = [(k, v) for k, v in newly_infected_data_rearranged.items()]

    death_data = json.load(death_dict)
    start_date = datetime(2020, 1, 1).date()
    end_date = datetime(2020, 12, 31).date()
    delta_dates = end_date - start_date
    day_list = []

    for i in range(delta_dates.days + 1):
        day_list.append(start_date + timedelta(days=i))
    death_data_rearranged = dict()
    day_counter = 1
    for _date in day_list:
        if str(_date) in death_data:
            death_data_rearranged[day_counter] = death_data[str(_date)]
        else:
            death_data_rearranged[day_counter] = 0
        day_counter += 1

    death_list = [(k, v) for k, v in death_data_rearranged.items()]

    susceptible_days = np.array([x[0] for x in sus_list])
    susceptible_count = np.array([x[1] for x in sus_list])

    recovered_days = np.array([y[0] for y in rec_list])
    recovered_count = np.array([y[1] for y in rec_list])
    recovered_count = np.cumsum(recovered_count)

    infection_days = np.array([z[0] for z in new_infect_list])
    infection_count = np.array([z[1] for z in new_infect_list])
    infection_count_mov = calculate_moving_averages(infection_count)
    infection_count_mov.insert(0, 0)
    infection_count_mov.insert(0, 0)

    death_days = np.array([d[0] for d in death_list])
    death_count = np.array([d[1] for d in death_list])
    death_count = np.cumsum(death_count)

    # X_Y_Spline_sus = make_interp_spline(susceptible_days, susceptible_count)
    # X_sus = np.linspace(susceptible_days.min(), susceptible_days.max(), 500)
    # Y_sus = X_Y_Spline_sus(X_sus)
    #
    # X_Y_Spline_rec = make_interp_spline(recovered_days, recovered_count)
    # X_rec = np.linspace(recovered_days.min(), recovered_days.max(), 500)
    # Y_rec = X_Y_Spline_rec(X_rec)
    #
    # X_Y_Spline_inf = make_interp_spline(infection_days, infection_count)
    # X_inf = np.linspace(infection_days.min(), infection_days.max(), 500)
    # Y_inf = X_Y_Spline_inf(X_inf)
    #
    # X_Y_Spline_inf_mov = make_interp_spline(infection_days, infection_count_mov)
    # X_inf_mov = np.linspace(infection_days.min(), infection_days.max(), 500)
    # Y_inf_mov = X_Y_Spline_inf_mov(X_inf_mov)
    #
    # X_Y_Spline_deaths = make_interp_spline(death_days, death_count)
    # X_death = np.linspace(death_days.min(), death_days.max(), 500)
    # Y_death = X_Y_Spline_deaths(X_death)

    plt.figure()
    plt.plot(susceptible_days, susceptible_count, "b", label="Susceptible")
    plt.plot(infection_days, infection_count, "r", label="Infected")
    plt.plot(recovered_days, recovered_count, "g", label="Removed")
    # plt.plot(infection_days, infection_count_mov, "k", label="MA for Infected")
    plt.plot(death_days, death_count, "y", label="Cumulative Deaths")
    plt.title("SIR graph: " + type)
    plt.ylabel("SIR populations")
    plt.xlabel("No. of days")
    plt.legend(loc="upper right")
    plt.savefig('../Results/Graphs/SIR_simulation_' + type +'.png')
    plt.show()


def per_capita_numbers(simulated_df, type):
    df_new_inf = simulated_df.groupby('date', as_index=False)['new_infection'].sum()
    # df_death = simulated_df.groupby('date', as_index=False)['death'].sum()
    df_recovery = simulated_df.groupby('date', as_index=False)['recovery'].sum()
    # df_vaccinations = simulated_df.groupby('date', as_index=False)['vaccinated'].sum()

    df_new_inf["date"] = pd.to_datetime(df_new_inf['date'])
    # df_death['date'] = pd.to_datetime(df_death['date'])
    df_recovery['date'] = pd.to_datetime(df_recovery['date'])
    # df_vaccinations['date'] = pd.to_datetime(df_vaccinations["date"])

    per_capita_new_infections_days = np.array([d for d in list(df_new_inf["date"])])
    per_capita_new_infections_days = np.array([i for i in range(len(per_capita_new_infections_days))])
    per_capita_new_infections_count = np.array([d for d in list(df_new_inf["new_infection"])])

    # X_Y_Spline_new_infections = make_interp_spline(per_capita_new_infections_days, per_capita_new_infections_count)
    # X_new_inf = np.linspace(per_capita_new_infections_days.min(), per_capita_new_infections_days.max(), 500)
    # Y_new_inf = X_Y_Spline_new_infections(X_new_inf)

    # per_capita_death_days = np.array([d for d in list(df_death["date"])])
    # per_capita_death_days = np.array([i for i in range(len(per_capita_death_days))])
    # per_capita_death_count = np.array([d for d in list(df_death["death"])])
    #
    # X_Y_Spline_deaths = make_interp_spline(per_capita_death_days, per_capita_death_count)
    # X_death = np.linspace(per_capita_death_days.min(), per_capita_death_days.max(), 500)
    # Y_death = X_Y_Spline_deaths(X_death)

    per_capita_recovery_days = np.array([d for d in list(df_recovery["date"])])
    per_capita_recovery_days = np.array([i for i in range(len(per_capita_recovery_days))])
    per_capita_recovery_count = np.array([d for d in list(df_recovery["recovery"])])

    # X_Y_Spline_recovery = make_interp_spline(per_capita_recovery_days, per_capita_recovery_count)
    # X_recovery = np.linspace(per_capita_recovery_days.min(), per_capita_recovery_days.max(), 500)
    # Y_recovery = X_Y_Spline_recovery(X_recovery)

    # vaccination_days = np.array([d for d in list(df_vaccinations["date"])])
    # vaccination_days = np.array([i for i in range(len(vaccination_days))])
    # vaccination_count = np.array([d for d in list(df_vaccinations["vaccinated"])])
    #
    # X_Y_Spline_vaccinations = make_interp_spline(vaccination_days, vaccination_count)
    # X_vaccinations = np.linspace(vaccination_days.min(), vaccination_days.max(), 500)
    # Y_vaccinations = X_Y_Spline_vaccinations(X_vaccinations)

    plt.figure()
    # plt.plot(X_death, Y_death, "r", label="Deaths")
    plt.plot(per_capita_new_infections_days, per_capita_new_infections_count, 'b', label='New Infections')
    plt.plot(per_capita_recovery_days, per_capita_recovery_count, 'g', label='Recovered')
    # plt.plot(X_vaccinations, Y_vaccinations, 'y', label='Vaccinations')
    plt.legend(loc="upper right")
    plt.title("Infections vs. Days: " + type)
    plt.xlabel("No. of days")
    plt.ylabel("No. of infections")
    plt.savefig("../Results/Graphs/Per_Capita_" + type + ".png")
    plt.show()


if __name__ == '__main__':
    susceptible = open('../Results/Data/General/susceptible_dict.json')
    newly_infected = open('../Results/Data/General/new_infection_date_dict.json')
    death_dict = open('../Results/Data/General/death_dict.json')
    recovery = open('../Results/Data/General/recovery_date_dict.json')
    sir_emulation(susceptible, newly_infected, death_dict, recovery, "General")
    simulated_results = pd.read_csv("../Results/Data/General/simulated_df.csv")
    per_capita_numbers(simulated_results, "General")
    # susceptible = open('../Results/susceptible_dict_vaccinations.json')
    # newly_infected = open('../Results/new_infection_date_dict_vaccinations.json')
    # death_dict = open('../Results/death_dict_vaccinations.json')
    # recovery = open('../Results/recovery_date_dict_vaccinations.json')
    # simulated_results = pd.read_csv("../Results/simulated_df_vaccinations.csv")
    birth_susceptible = open('../Results/Data/Birthdays/susceptible_bir_dict.json')
    birth_newly_infected = open('../Results/Data/Birthdays/new_infection_date_bir_dict.json')
    birth_death_dict = open('../Results/Data/Birthdays/death_bir_dict.json')
    birth_recovery = open('../Results/Data/Birthdays/recovery_date_bir_dict.json')
    sir_emulation(birth_susceptible, birth_newly_infected, birth_death_dict, birth_recovery, "Birthdays")
    bday_df = pd.read_csv("../Results/Data/Birthdays/birthday_final.csv")
    per_capita_numbers(bday_df, "Birthdays")