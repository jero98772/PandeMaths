#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PandeMaths - 2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PandeMaths; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
VERSION = "v0.3_beta"
RELEASE = "29032020"
SOURCE1 = "https://code.03c8.net/epsylon/pandemaths"
SOURCE2 = "https://github.com/epsylon/pandemaths"
CONTACT = "epsylon@riseup.net - (https://03c8.net)"

pandemic_model_variables_path = "model/pandemia.txt" # pandemia variables file
extended_model_variables_path = "model/extended.txt" # extended model variables file
simulation_templates_path = "templates/" # templates files
reports_path = "reports/" # reports files

import json, datetime, os, random, sys
import matplotlib.pyplot as plt

def model_maths():
    print("[Info] Reviewing Model ...\n")
    try:
        print(" "+"-"*5+"\n")
        f = open(pandemic_model_variables_path, "r")
        model_variables = f.readlines()
        f.close()
        for v in model_variables:
            print("   - "+str(v.replace("\n", "")))
    except:
        pass
    try:
        print("\n "+"-"*5+"\n")
        f = open(extended_model_variables_path, "r")
        extended_variables = f.readlines()
        f.close()
        for v in extended_variables:
            print("   - "+str(v.replace("\n", "")))
    except:
        pass
    print("\n "+"-"*5+"\n")

def simulation():
    print("[Info] Defining ecosystem ...\n")
    total_population = input("   + Total population (default: 100000): ")
    try:
        total_population = int(total_population)
    except:
        total_population = 100000
    if not total_population:
        total_population = 100000
    starting_population = total_population
    infected_starting = input("   + Infected (at the beginning) population (default: 1): ")
    try:
        infected_starting = int(infected_starting)
    except:
        infected_starting = 1
    if not infected_starting or infected_starting < 1:
        infected_starting = 1
    infected = infected_starting
    print("\n "+"-"*5+"\n")
    print("[Info] Establishing time units ...\n")
    days = input("   + Number of days (default: 200): ")
    try:
        days = int(days)
    except:
        days = 200
    if not days:
        days = 200
    daily_rate_interaction = input("   + Daily rate of interaction between individuals (default: 2.50): ")
    try:
        daily_rate_interaction = int(daily_rate_interaction)
    except:
        daily_rate_interaction = 2.50
    if not daily_rate_interaction:
        daily_rate_interaction = 2.50
    print("\n "+"-"*5+"\n")
    template = input("+ CHOOSE: (O)pen Simulation or (L)oad template: ").upper()
    if template == "O": # New Simulation
        average_rate_duration = None
        probability_of_contagion = None
        recovery_rate = None
        simulation_name = "OPEN"
        new_simulation(total_population, infected_starting, days, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, simulation_name, starting_population)
    else: # Load template
        load_template(total_population, infected_starting, days, daily_rate_interaction, starting_population)

def load_template(total_population, infected_starting, days, daily_rate_interaction, starting_population):
    print("\n "+"-"*5+"\n")
    print("[Info] Generating templates ...\n")
    import glob
    templates = {}
    i = 0
    for file in glob.iglob(simulation_templates_path + '*', recursive=False):
        if(file.endswith(".txt")): 
            i = i +1
            f=open(file, 'r')  
            template =  f.read().replace('\n',' ')
            templates[i] = file.replace("templates/",""), template.upper() # add template to main dict
            f.close()
    for k,v in templates.items():
        print ("  ["+str(k)+"] - "+str(v[0].replace(".txt","")))
    print("\n "+"-"*5+"\n")
    template_set = input("+ CHOOSE: Number of template (ex: 1): ").upper()
    try:
        template_set = int(template_set)
    except:
        template_set = 1
    if not template_set or template_set > len(templates) or template_set < 1:
        template_set = 1
    for k,v in templates.items():
        if template_set == k:
            simulation_name = v[0].replace(".txt","")
            average_rate_duration = int(v[1].split("DURATION:")[1].split(" ")[0])
            probability_of_contagion = int(v[1].split("CONTAGION:")[1].split(" ")[0])
            recovery_rate = int(v[1].split("RECOV:")[1].split(" ")[0])
            new_simulation(total_population, infected_starting, days, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, simulation_name, starting_population)

def new_simulation(total_population, infected_starting, days, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, simulation_name, starting_population):
    print("\n "+"-"*5+"\n")
    print("[Info] Generating variables ...\n")
    if average_rate_duration == None:
        average_rate_duration = input("   + Average duration of illness (default: 12) (days): ")
        try:
            if average_rate_duration == 0:
                pass
            else:
                average_rate_duration = int(average_rate_duration)
        except:
            average_rate_duration = 12
        if average_rate_duration < 0 or average_rate_duration > 100:
            average_rate_duration = 12
    else:
        print("   + Average duration of illness: "+str(average_rate_duration)+" days")
    if probability_of_contagion == None:
        probability_of_contagion = input("   + Infection rate (default: 14%): ")
        try:
            if probability_of_contagion == 0:
                pass
            else:
                probability_of_contagion = int(probability_of_contagion)
        except:
            probability_of_contagion = 14
        if probability_of_contagion < 0 or probability_of_contagion > 100:
            probability_of_contagion = 14
    else:
        print("   + Infection rate: "+str(probability_of_contagion)+"%")
    if recovery_rate == None:
        recovery_rate = input("   + Recovery rate (default: 95%): ")
        try:
            if recovery_rate == 0:
                pass
            else:
                recovery_rate = int(recovery_rate)
        except:
            recovery_rate = 95
        if recovery_rate < 0 or recovery_rate > 100:
            recovery_rate = 95
    else:
        print("   + Recovery rate: "+str(recovery_rate)+"%")
    mortality = 100 - recovery_rate
    print("\n "+"-"*5+"\n")
    print("[Info] Building parameters ...\n")
    print("   + Mortality rate: "+str(mortality)+"%")
    mortality = mortality / 100
    recovery_rate = recovery_rate / 100
    probability_of_contagion = probability_of_contagion / 100
    infected = infected_starting
    susceptible_starting = int(total_population) - int(infected)
    susceptible = susceptible_starting # susceptitble at start
    recovered = 0 # recovered individuals at start
    deceased = 0 # deceases individuals at start
    print("   + Susceptible: "+str(susceptible))
    print("   + Recovered: "+str(recovered))
    print("   + Deceased: "+str(deceased))
    print("\n"+"-"*15+"\n")
    print("[Info] Launching Simulation: [ "+str(simulation_name)+" ] ...\n")
    total_contagion = 0
    recoveries = 0
    current_time = datetime.datetime.now() # current datetime
    if not os.path.exists(reports_path): # create folder for reports
        os.makedirs(reports_path)
    data = {
      'METADATA': [
        {
        'Simulation Name': str(simulation_name),
        'Datetime': str(current_time)
        }
      ],
      'ECOSYSTEM': [
        {
        'Total Population': str(total_population),
        'Infected (at the beginning)': str(infected_starting),
        'Number of days': str(days),
        'Daily rate of interaction between individuals': str(daily_rate_interaction),
        'Average duration of illness': str(average_rate_duration),
        'Infection rate': str(probability_of_contagion*100)+"%",
        'Recovery rate': str(recovery_rate*100)+"%",
        'Mortality': str(mortality*100)+"%",
        'Susceptible': str(susceptible),
        'Recovered': str(recovered),
        'Deceased': str(deceased)
        }
      ],
     'SIMULATION': [
        {}
      ]
    }
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    with open(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".txt"), 'a', encoding='utf-8') as f: # append into txt
        f.write("="*50+os.linesep)
        f.write("Simulation Name:"+str(simulation_name)+os.linesep)
        f.write("Infected (at the beginning):"+str(infected_starting)+os.linesep)
        f.write("Number of days:"+str(days)+os.linesep)
        f.write("Daily rate of interaction between individuals:"+str(daily_rate_interaction)+os.linesep)
        f.write("Average duration of illness:"+str(average_rate_duration)+os.linesep)
        f.write("Infection rate:"+str(probability_of_contagion*100)+"%"+os.linesep)
        f.write("Recovery rate:"+str(recovery_rate*100)+"%"+os.linesep)
        f.write("Mortality:"+str(mortality*100)+"%"+os.linesep)
        f.write("Susceptible:"+str(susceptible)+os.linesep)
        f.write("Recovered:"+str(recovered)+os.linesep)
        f.write("Deceased:"+str(deceased)+os.linesep)
        f.write("="*50+os.linesep)
    entire_population_infected = 0
    day_started = False
    plot_starting_population = []
    plot_days = []
    plot_contagion = []
    plot_recoveries = []
    plot_deaths = []
    plot_susceptible = []
    plot_infected = []
    plot_recovered = []
    plot_total_population = []
    plot_total_contagion = []
    plot_total_recovered = []
    plot_total_deceased = []
    plot_total_non_affected = []
    for i in range(0, days):
        if i > 0:
            try:
                status_rate = round(int(infected*100/total_population))
            except:
                status_rate = 100
            if status_rate < 11: # ENDEMIA (-11%)
                if susceptible > 0:
                    status = "IMPACT LEVEL: ENDEMIC!"
                else:
                    if int(total_population*100/starting_population) > 49:
                        status = "PRACTICALLY ERRADICATED BUT AT LEAST HALF OF THE POPULATION HAS DIED!"
                    else:
                        status = "PRACTICALLY ERRADICATED!"
            elif status_rate > 10 and status_rate < 25: # EPIDEMIA (>10%<25%)
                if susceptible > 0:
                    status = "IMPACT LEVEL: EPIDEMIC!"
                else:
                    status = "IMPORTANT FOCUS OF INCUBATION!"
            else: # PANDEMIA (>25%)
                if susceptible > 0:
                    status = "IMPACT LEVEL: PANDEMIC!"
                else:
                    status = "MOSTLY OF THE POPULATION IS INCUBATING!"
            sir = susceptible+infected+recovered # S-I-R model
            try:
                contagion = round(infected*daily_rate_interaction*susceptible/sir*probability_of_contagion) # contagion rounded rate
            except:
                contagion = 100
            recoveries = round(infected*recovery_rate/average_rate_duration) # recoveries rounded rate
            deaths = round(infected*mortality/average_rate_duration) # deaths rounded rate
            susceptible = susceptible - contagion + recoveries - deaths
            infected = infected+contagion-recoveries-deaths
            recovered =recovered + recoveries
            deceased = deceased + deaths
            total_contagion = total_contagion + contagion
            total_recovered = recovered
            total_deceased = total_deceased + deaths
            total_population = starting_population - deceased
            total_non_affected = susceptible_starting+infected_starting+0+0-total_contagion
            day_started = True
        else: # related to the first day
            status = "STARTED!"
            contagion = 0
            recoveries = 0
            deaths = 0
            total_recovered = 0
            total_deceased = 0
            deceased = 0
            susceptible = total_population - infected
            recovered = 0
            total_contagion = infected_starting
            total_non_affected = susceptible
        if total_population < 0:
            total_population = 0
        if total_contagion < total_contagion < 0:
            total_contagion = 0
        if contagion > susceptible: # more individuals than susceptible cannot be infected
            contagion = susceptible
        if contagion < 1:
            contagion = 0
        if total_non_affected < 1: # cannot be negative non affected individuals
            total_non_affected = 0
        if recoveries < 1:
            recoveries = 0
        if susceptible + infected + recovered + deceased > starting_population:
            susceptible = int(starting_population - infected - recovered - deceased)
            deaths = int(recovered + deceased - starting_population)
        if deaths < 1:
            deaths = 0
        if deaths > total_population:
            deaths = total_population
        if deaths > infected:
            deaths = infected
            infected = 0
        if susceptible < 1: # cannot be negative susceptible individuals
            susceptible = 0
        if susceptible == 0:
            total_non_affected = 0
        if day_started == True:
            if int(contagion + recoveries + deaths) == 0: # infected final resolution phase solved by random results
                if infected > 0:
                    deaths = random.randrange(infected)
                if deaths > infected:
                    infected = deaths
                if infected == 1: # random final against Existentialism!
                    res = random.randrange(2)
                    if res == 1: # survive!
                        recoveries = recoveries + 1
                    else: # die!
                        deaths = deaths + 1
                infected = infected+contagion-recoveries-deaths
                recovered = recovered + recoveries
                total_recovered = total_recovered + recoveries
                deceased = deceased+deaths
        if infected > starting_population:
            infected = starting_population
        if total_population > 0:
            if infected > 0:
                if total_non_affected > 0:
                    print("  -> [DAY: "+str(i)+"]\n      Status: "+str(status)+"\n      Contagion: ("+str(int(contagion))+")["+str(round(contagion/total_population*100))+"%] - Recoveries: ("+str(int(recoveries))+")["+str(round(recoveries/total_population*100))+"%] - Deaths: ("+str(int(deaths))+")["+str(round(deaths/total_population*100))+"%] | Susceptible: ("+str(int(susceptible))+")["+str(round(susceptible/total_population*100))+"%] - Infected: ("+str(int(infected))+")["+str(round(infected/total_population*100))+"%] - Recovered: ("+str(int(recovered))+")["+str(round(recovered/total_population*100))+"%]")
                    print("      Total Population: ("+str(int(total_population))+"/"+str(int(starting_population))+") - Total Contagion: ("+str(int(total_contagion))+")["+str(round(total_contagion/starting_population*100))+"%] - Total Recovered: (" +str(int(total_recovered))+")["+str(round(total_recovered/starting_population*100))+"%] - Total Deceased: ("+str(int(total_deceased))+")["+str(round(total_deceased/starting_population*100))+"%] - Total N/A: ("+str(int(total_non_affected))+")["+str(round(total_non_affected/starting_population*100))+"%]\n")
                else:
                    if entire_population_infected == 0:
                        total_contagion = starting_population
                        susceptible = 0
                        status = "ALL INFECTED !!!"
                        print("-"*75+"\n")
                        print("  -> [DAY: "+str(i)+"] -> [ THE ENTIRE POPULATION HAS BEEN INFECTED! ]\n      Status: "+str(status)+"\n      Contagion: ("+str(int(contagion))+")[100%] - Recoveries: ("+str(int(recoveries))+")["+str(round(recoveries/total_population*100))+"%] - Deaths: ("+str(int(deaths))+")["+str(round(deaths/total_population*100))+"%] | Susceptible: ("+str(int(susceptible))+")[0%] - Infected: ("+str(int(infected))+")[100%] - Recovered: ("+str(int(recovered))+")["+str(round(recovered/total_population*100))+"%]")
                        entire_population_infected = entire_population_infected + 1
                        print("      Total Population: ("+str(int(total_population))+"/"+str(int(starting_population))+") - Total Contagion: ("+str(int(total_contagion))+")["+str(round(total_contagion/starting_population*100))+"%] - Total Recovered: (" +str(int(total_recovered))+")["+str(round(total_recovered/starting_population*100))+"%] - Total Deceased: ("+str(int(total_deceased))+")["+str(round(total_deceased/starting_population*100))+"%] - Total N/A: ("+str(int(total_non_affected))+")["+str(round(total_non_affected/starting_population*100))+"%]\n")
                        print("-"*75+"\n")
                    else:
                        print("  -> [DAY: "+str(i)+"]\n      Status: "+str(status)+"\n      Contagion: ("+str(int(contagion))+")[100%] - Recoveries: ("+str(int(recoveries))+")["+str(round(recoveries/total_population*100))+"%] - Deaths: ("+str(int(deaths))+")["+str(round(deaths/total_population*100))+"%] | Susceptible: ("+str(int(susceptible))+")[0%] - Infected: ("+str(int(infected))+")[100%] - Recovered: ("+str(int(recovered))+")["+str(round(recovered/total_population*100))+"%]")
                        print("      Total Population: ("+str(int(total_population))+"/"+str(int(starting_population))+") - Total Contagion: ("+str(int(total_contagion))+")["+str(round(total_contagion/starting_population*100))+"%] - Total Recovered: (" +str(int(total_recovered))+")["+str(round(total_recovered/starting_population*100))+"%] - Total Deceased: ("+str(int(total_deceased))+")["+str(round(total_deceased/starting_population*100))+"%] - Total N/A: ("+str(int(total_non_affected))+")["+str(round(total_non_affected/starting_population*100))+"%]\n")
                export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate txt
                export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate json
                export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_recovered, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, plot_total_non_affected, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, recovered, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate plotting graph
            else: # population has passed the pandemia
                status = "VACCINED! [ NO MORE INFECTED! ]"
                if entire_population_infected == 0:
                    total_contagion = starting_population
                print("-"*75+"\n")
                print("  -> [DAY: "+str(i)+"] -> [ NO MORE INFECTED! ]\n      Status: "+str(status)+"\n      Contagion: ("+str(int(contagion))+")[0%] - Recoveries: ("+str(int(recoveries))+")["+str(round(recoveries/total_population*100))+"%] - Deaths: ("+str(int(deaths))+")["+str(round(deaths/total_population*100))+"%] | Susceptible: ("+str(int(susceptible))+")[0%] - Infected: ("+str(int(infected))+")[0%] - Recovered: ("+str(int(recovered))+")["+str(round(recovered/total_population*100))+"%]")
                print("      Total Population: ("+str(int(total_population))+"/"+str(int(starting_population))+") - Total Contagion: ("+str(int(total_contagion))+")["+str(round(total_contagion/starting_population*100))+"%] - Total Recovered: (" +str(int(total_recovered))+")["+str(round(total_recovered/starting_population*100))+"%] - Total Deceased: ("+str(int(total_deceased))+")["+str(round(total_deceased/starting_population*100))+"%] - Total N/A: ("+str(int(total_non_affected))+")["+str(round(total_non_affected/starting_population*100))+"%]\n")
                print("-"*75+"\n")
                export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate txt
                export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate json
                export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_recovered, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, plot_total_non_affected, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, recovered, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate plotting graph
                break
        else: 
            if total_deceased >= starting_population: # the entire population has died! [game over!]
                status = "FATAL! [ THE ENTIRE POPULATION HAS DIED! ]"
                contagion = 0
                recoveries = 0
                deaths = 0
                susceptible = 0
                total_population = 0
                total_non_affected = 0
                print("  -> [DAY: "+str(i)+"] -> FATAL! [ THE ENTIRE POPULATION HAS DIED! ]\n      Status: "+str(status)+"\n      Contagion: ("+str(int(contagion))+")[100%] - Recoveries: ("+str(int(recoveries))+")[0%] - Deaths: ("+str(int(deaths))+")[100%] - Susceptible: ("+str(int(susceptible))+")[0%] - Infected: ("+str(int(infected))+")[100%] - Recovered: ("+str(int(recovered))+")[0%]")
                print("      Total Population: ("+str(int(total_population))+"/"+str(int(starting_population))+") - Total Contagion: ("+str(int(total_contagion))+")["+str(round(total_contagion/starting_population*100))+"%] - Total Recovered: (" +str(int(total_recovered))+")["+str(round(total_recovered/starting_population*100))+"%] - Total Deceased: ("+str(int(total_deceased))+")["+str(round(total_deceased/starting_population*100))+"%] - Total N/A: ("+str(int(total_non_affected))+")["+str(round(total_non_affected/starting_population*100))+"%]\n")
                export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate txt
                export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate json
                export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_recovered, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, plot_total_non_affected, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, recovered, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate plotting graph
                break
    status = "FINISHED!"
    if infected == 0:
        deaths = 0
        recoveries = 0
        contagion = 0
    print("  -> [DAY: "+str(i)+"] -> [ SIMULATION END! ]\n      Status: "+str(status))
    print("      Total Population: ("+str(int(total_population))+"/"+str(int(starting_population))+") - Total Contagion: ("+str(int(total_contagion))+")["+str(round(total_contagion/starting_population*100))+"%] - Total Recovered: (" +str(int(total_recovered))+")["+str(round(total_recovered/starting_population*100))+"%] - Total Deceased: ("+str(int(total_deceased))+")["+str(round(total_deceased/starting_population*100))+"%] - Total N/A: ("+str(int(total_non_affected))+")["+str(round(total_non_affected/starting_population*100))+"%]\n")
    export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate txt
    export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate json
    export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_recovered, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, plot_total_non_affected, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, recovered, total_population, total_contagion, total_recovered, total_deceased, total_non_affected) # generate plotting graph
    print("="*50 + "\n")
    generate_graph(starting_population, simulation_name, infected_starting, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, mortality, total_population, plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_recovered, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, plot_total_non_affected, current_time) # generate final graph
    print ("[Info] [REPORTS] (txt|json|png) -> [SAVED!] at: '"+str(reports_path+"PandeMaths-report_"+str(current_time)+"/'")+"\n")

def export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected):
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    with open(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".txt"), 'a', encoding='utf-8') as f: # append into txt
        f.write(os.linesep)
        f.write("Day:"+str(i)+os.linesep)
        f.write("Status:"+str(status)+os.linesep)
        f.write("Contagion:"+str(contagion)+os.linesep)
        f.write("Recoveries:"+str(recoveries)+os.linesep)
        f.write("Deaths:"+str(deaths)+os.linesep)
        f.write("Susceptible:"+str(susceptible)+os.linesep)
        f.write("Infected:"+str(infected)+os.linesep)
        f.write("Recovered:"+str(recovered)+os.linesep)
        f.write("Deceased:"+str(deceased)+os.linesep)
        f.write("Total Population:"+str(total_population)+os.linesep)
        f.write("Total Contagion:"+str(total_contagion)+os.linesep)
        f.write("Total Deceased:"+str(total_deceased)+os.linesep)
        f.write("Total N/A:"+str(total_non_affected)+os.linesep)

def export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, recovered, deceased, total_population, total_contagion, total_recovered, total_deceased, total_non_affected):
    data['SIMULATION'][0]['DAY'] = str(i)
    data['SIMULATION'][0]['Status'] = str(status)
    data['SIMULATION'][0]['Contagion'] = str(int(contagion))
    data['SIMULATION'][0]['Recoveries'] = str(int(recoveries))
    data['SIMULATION'][0]['Deaths'] = str(int(deaths))
    data['SIMULATION'][0]['Susceptible'] = str(int(susceptible))
    data['SIMULATION'][0]['Infected'] = str(int(infected))
    data['SIMULATION'][0]['Recovered'] = str(int(recovered))
    data['SIMULATION'][0]['Deceased'] = str(int(deceased))
    data['SIMULATION'][0]['Total Population'] = str(int(total_population))
    data['SIMULATION'][0]['Total Contagion'] = str(int(total_contagion))
    data['SIMULATION'][0]['Total Recovered'] = str(int(recovered))
    data['SIMULATION'][0]['Total Deceased'] = str(int(total_deceased))
    data['SIMULATION'][0]['Total N/A'] = str(int(total_non_affected))
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    with open(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".json"), 'a', encoding='utf-8') as f: # append into json
        json.dump(data, f, ensure_ascii=False, sort_keys=False, indent=4)

def export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_recovered, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, plot_total_non_affected, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, recovered, total_population, total_contagion, total_recovered, total_deceased, total_non_affected):
    plot_starting_population = starting_population
    plot_days.append(i)
    plot_contagion.append(contagion)
    plot_recoveries.append(recoveries)
    plot_deaths.append(deaths)
    plot_susceptible.append(susceptible)
    plot_infected.append(infected)
    plot_recovered.append(recovered)
    plot_total_population.append(total_population)
    plot_total_contagion.append(total_contagion)
    plot_total_recovered.append(total_recovered)
    plot_total_deceased.append(total_deceased)
    plot_total_non_affected.append(total_non_affected)

def generate_graph(starting_population, simulation_name, infected_starting, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, mortality, total_population, plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_recovered, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, plot_total_non_affected, current_time):
    plt.plot(plot_days, plot_contagion, "blue", label="Contagion")
    plt.plot(plot_days, plot_recoveries, "grey", label="Recoveries")
    plt.plot(plot_days, plot_deaths, "orange", label="Deaths")
    plt.plot(plot_days, plot_susceptible, "cyan", label="Susceptible")
    plt.plot(plot_days, plot_infected, "purple", label="Infected")
    plt.plot(plot_days, plot_recovered, "brown", label="Recovered")
    plt.plot(plot_days, plot_total_population, "pink", label="Total Population")
    plt.plot(plot_days, plot_total_contagion, "red", label="Total Contagion")
    plt.plot(plot_days, plot_total_recovered, "yellow", label="Total Recovered")
    plt.plot(plot_days, plot_total_deceased, "black", label="Total Deceased")
    plt.plot(plot_days, plot_total_non_affected, "green", label="Total N/A")
    plt.plot(plot_starting_population)
    plt.title("SIMULATION: '"+str(simulation_name)+"' = Av_Ill: ["+str(average_rate_duration)+" days] - Inf_R: ["+str(probability_of_contagion*100)+"%] - Rec_R: ["+str(recovery_rate*100)+"%] - Mort: ["+str(mortality*100)+"%]\n\nTotal Population: ["+str(total_population)+"/"+str(starting_population)+"] - Infected (at the beginning): ["+str(infected_starting)+"] - Interaction (rate): ["+str(daily_rate_interaction)+"]\n")
    plt.xlabel('Day(s)')
    plt.ylabel('Individual(s)')
    plt.legend(loc='center left', fancybox=True, bbox_to_anchor=(1, 0.5))
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    plt.savefig(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".png"), bbox_inches='tight')

def print_banner():
    print("\n"+"="*50)
    print(" ____                 _      __  __       _   _         ")
    print("-  _ \ __ _ _ __   __- - ___-  \/  - __ _- -_- -__  ___ ")
    print("- -_) / _` - '_ \ / _` -/ _ \ -\/- -/ _` - __- '_ \/ __--2020")
    print("-  __/ (_- - - - - (_- -  __/ -  - - (_- - -_- - - \__ /")
    print("-_-   \__,_-_- -_-\__,_-\___-_-  -_-\__,_-\__-_- -_-___/-by psy")
    print('\n"Pandemics Extensible Mathematical Model"')
    print("\n"+"-"*15+"\n")
    print(" * VERSION: ")
    print("   + "+VERSION+" - (rev:"+RELEASE+")")
    print("\n * SOURCES:")
    print("   + "+SOURCE1)
    print("   + "+SOURCE2)
    print("\n * CONTACT: ")
    print("   + "+CONTACT+"\n")
    print("-"*15+"\n")
    print("="*50)

# sub_init #
print_banner() # show banner
try:
    option = input("\n+ CHOOSE: (M)odel or (S)imulation: ").upper()
except:
    print("\n"+"="*50 + "\n")
    print ("[Info] Try to run the tool with Python3.x.y... (ex: python3 pandemaths) -> [EXITING!]\n")
    sys.exit()
print("")
print("="*50+"\n")
if option == "S": # simulation
    simulation()
else: # model
    model_maths()
print ("="*50+"\n")
