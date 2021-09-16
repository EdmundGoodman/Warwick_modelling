What is the model?
-	Shows the spread of a disease and the spread of levels of antimicrobial resistance among a population.
-	Two version exist: one with our product and one without.
-	The product is in the model used on patients, not sinks, for the sake of simplicity.

Purpose of the model
-	Demonstrate that our product works
-	Understand and demonstrate when it is more or less useful

Key features of the model
1.	There are turns during which everything happens.
2.	The model is stochastic, meaning it is based on probabilities.
3.	The population is fixed.
4.	A disease with a probability of death and a probability of recovery spreads
5.	A number of antibiotics, generally two or three, can be used to cure a patient faster
6.	These are used in a specific order, with antibiotic 1 used before 2 etc, to simulate the treatment/harm trade-off.
7.	All of these have their own respective antibiotic resistance 
8.	Each level of resistance gives protection against the counterpart antibiotic and all lower levels of antibiotics. E.g. resistance 2 makes antibiotics 2 and 1 useless.

Individuals/patients:
-	An individual can be uninfected, infected without resistance, infected with any level of resistance, immune or dead.
-	A person turns immune if they recover from the disease.
-	Since the population is fixed, as time goes to infinity, all individuals will at the end be either uninfected, immune or dead.

Treatment (without the product):
-	Once a person becomes infected, treatment starts immediately
-	Staff do not know if there is any resistance, hence they will start with the lowest level of antibiotics
-	If the infection is not resistant, there will be a greater chance of recovering from the disease every turn
-	If the infection is resistant, there will be no greater chance of recovery than for an untreated patient
-	Every turn the person has not recovered or died, there is a probability the staff will move up one antibiotic level.

Treatment (with the product):
-	Same as before, but now they know if the infection has the highest level of resistance or not. If they don’t, they will follow procedure as usual. If they do, they will immediately stop all antibiotic treatment.


Spread of the disease (without the product):
-	A number of people are infected at the start, perhaps with levels of resistance.
-	Every infected person has a probability to spread the disease
-	If a person is in isolation, that probability becomes zero.
-	A person enters isolation when they reach the highest level of treatment (note: without our product it is not related to whether the infection has the highest level of resistance).

Spread of the disease (with the product):
-	Same as before, but isolation is not dependent on treatment level, but whether the highest level of resistance has been detected. If it hasn’t, no isolation. If it has, isolation.

How does resistance increase?
-	Two ways, through spread and through mutation.
-	Spread: when a person infects another, the resistance (or lack thereof) will carry over.
-	Mutation: Every turn there is a slight chance the disease will increase the level of resistance by one.
-	Hence as patients with no or low resistance are treated more successfully, the share of infected patients with resistance will increase over time.
o	Without our product, the highest level of resistance cannot be detected and will therefore be very slow to treat, as the patient has to go through all stages of treatment. Although it is generally slow to mutate to the highest level, once it does it will spread rapidly throughout the population, killing swathes of people.

Is the model realistic?
-	No, very little about it is realistic. It is a model meant to portray how resistance spreads and is combatted.

Is it useful?
-	Yes, because it answers several questions.

Potential insights from the model:
-	The impact our product will have on the spread of resistance just by quickly detecting who to put into isolation.
-	Whether higher or lower mortality or transmissibility of a disease increase or decrease the effectiveness. 

Potential improvements:
-	Add special features  more realistic scenario and results.
-	Add asymptomatic transmission  more realistic scenario and results. Perhaps insights into whether asymptomatic transmission makes the product more or less useful.