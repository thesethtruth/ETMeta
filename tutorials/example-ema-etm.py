# ema_etm.py
from functools import cache
from ema_workbench import (
    Model,
    RealParameter,
    ScalarOutcome,
    Constant,
    perform_experiments,
)
from ema_workbench.em_framework.parameters import Scenario
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# import ETM connection
from ETMeta import ETMapi

metrics = [
    "dashboard_reduction_of_co2_emissions_versus_1990",
    "dashboard_renewability",
    "dashboard_share_of_renewable_electricity",
    "dashboard_energy_import_netto",
    "dashboard_total_costs",
    "dashboard_energy_demand_primary_of_final_plus_export_losses",
    "dashboard_blackout_hours",
    "dashboard_total_number_of_excess_events",
    "dashboard_security_of_supply",
    "lv_net_capacity_delta_present_future",
    "mv_net_capacity_delta_present_future",
    "hv_net_capacity_delta_present_future",
]


def init_ETM(ref_scenario, metrics):
    ETMa = ETMapi(scenario_id=ref_scenario)
    ETMa.verbose = False
    ETMa.create_new_scenario("EMA scenario", use_custom_values=False)
    ETMa.gqueries = metrics
    return ETMa


@cache
def ETMwrapper(
    ETM_instance=None,
    solarVSwind=None,
    flh_of_energy_power_wind_turbine_inland=None,
    flh_of_solar_pv_solar_radiation=None,
    costs_co2=None,
    total_supply=None,
):
    
    if ETM_instance is None:
        ETMi = ETMapi()
    else:
        ETMi = ETM_instance
    
    constants = {
        "flh_of_energy_power_wind_turbine_inland": flh_of_energy_power_wind_turbine_inland,
        "flh_of_solar_pv_solar_radiation": flh_of_solar_pv_solar_radiation,
        "costs_co2": costs_co2,
    }

    capacity_of_energy_power_wind_turbine_inland = (
        solarVSwind * total_supply / flh_of_energy_power_wind_turbine_inland
    )
    capacity_of_energy_power_solar_pv_solar_radiation = (
        (1 - solarVSwind) * total_supply / flh_of_solar_pv_solar_radiation
    )

    ETMi.user_values = {
        "capacity_of_energy_power_wind_turbine_inland": capacity_of_energy_power_wind_turbine_inland,
        "capacity_of_energy_power_solar_pv_solar_radiation": capacity_of_energy_power_solar_pv_solar_radiation,
    }
    ETMi.user_values.update(constants)

    p = ETMi.update_inputs()
    if not p.status_code == 200:
        raise ValueError(f"Response not succesful: {p.json()['errors']}")
    ETMi._update_metrics(output_format="dict")

    getter = lambda m: ETMi.metrics.get(m, 0)["future"]

    return {metric: getter(metric) for metric in metrics}


model = Model("ETMwrapper", function=ETMwrapper)

# set levers
model.levers = [RealParameter("solarVSwind", 0, 1)]

# specify outcomes
model.outcomes = [ScalarOutcome(metric) for metric in metrics]
# model.outcomes = [ScalarOutcome("hv_net_capacity_delta_present_future")]

# initiate ETM connection
ref_scenario = 769771
ETM = init_ETM(ref_scenario, metrics)

# override some of the defaults of the model
model.constants = [
    # standard = 1920 hours / year
    Constant("ETM_instance", ETM),
    Constant("flh_of_energy_power_wind_turbine_inland", 3000),
    Constant("flh_of_solar_pv_solar_radiation", 1000),  # standard = 867 / year
    Constant("costs_co2", 100),  # standard = 8 €/tonne
    Constant("total_supply", 55e6),  # MWh 35e6 minimum, RES 1.0 55e6
]

results = perform_experiments(model, policies=25)

experiments, outcomes = results

policies = experiments["policy"]
for i, policy in enumerate(np.unique(policies)):
    experiments.loc[policies == policy, "policy"] = str(i)

data = pd.DataFrame(outcomes)
data["solarVSwind"] = experiments["solarVSwind"]

#%% plotting section
colors = sns.color_palette("Set2", len(data.columns))
sns.set_style("whitegrid")


to_plot1 = [
    "dashboard_reduction_of_co2_emissions_versus_1990",
    "dashboard_share_of_renewable_electricity",
    "dashboard_total_costs",
]

to_plot2 = [
    "dashboard_total_number_of_excess_events",
    "dashboard_security_of_supply",
]


def multi_scatter_stack(data, to_plot, title=None, save_fig=False):
    fig, ax = plt.subplots(len(to_plot), 1, sharex=True, figsize=(10, 10))
    for i, col in enumerate(to_plot):

        sns.scatterplot(
            data=data,
            x="solarVSwind",
            y=col,
            palette=[colors[i]],
            ax=ax[i],
        )
        ax[i].set_ylabel("")
        ax[i].set_title(col)
    
    sns.despine(left=True, bottom=True)
    
    if title is not None:
        plt.suptitle(title)

    if save_fig:
        plt.savefig(title + ".png")
    

multi_scatter_stack(data, to_plot1, title='Cost and renewability', save_fig=True)
multi_scatter_stack(data, to_plot2, title='Curtailment and underload', save_fig=True)

# %%
from ema_workbench.analysis import feature_scoring

x = experiments
y = outcomes

fs = feature_scoring.get_feature_scores_all(x, y)
sns.heatmap(fs, cmap='viridis', annot=True)
plt.show()
# %%
