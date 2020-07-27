from flask import Flask, render_template ,request
from PandeMaths.pandemaths import new_simulation ,load_template
import os
app = Flask(__name__)
def deletefiles():
	if os.path.isfile("PandeMaths-report.json"):
		os.remove("static/reports/PandeMaths-report/PandeMaths-report.json")
	if os.path.isfile("PandeMaths-report.txt"):
		os.remove("static/reports/PandeMaths-report/PandeMaths-report.txt")
	if os.path.isfile("PandeMaths-report.png"):
		os.remove("static/reports/PandeMaths-report/PandeMaths-report.png")
@app.route("/",methods=['GET','POST'])
def index():
	deletefiles()
	if request.method == 'POST':
		total_population = int(request.form['total_population'])#1
		infected_starting = int(request.form['infected_starting'])#2
		days = int(request.form['days'])#3
		daily_rate_interaction = float(request.form['daily_rate_interaction'])#4
		average_rate_duration = int(request.form['average_rate_duration'])#6
		probability_of_contagion = int(request.form['probability_of_contagion'])#7
		recovery_rate = int(request.form['recovery_rate'])#8
		starting_population = total_population#9
		template = request.form['template']
		template_set = request.form['template_set']
		if template == "load template":
			average_rate_duration = None
			probability_of_contagion = None
			recovery_rate = None
			simulation_name = "OPEN"
			new_simulation(total_population, infected_starting, days, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, simulation_name, starting_population)
		elif template == "new simulation":
			load_template(total_population, infected_starting, days, daily_rate_interaction, starting_population,template_set)
	return render_template("index.html")
@app.route("/out",methods=['GET','POST'])
def out():
	text = ""
	with open("static/reports/PandeMaths-report/PandeMaths-report.txt", "r") as f:
		data = f.readlines()
	for i in data:
		text += i
	return render_template("out.html",text=text )
if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0")