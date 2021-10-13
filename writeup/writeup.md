# iGEM modelling

## Table of contents

[TOC]

## Custom modelling

The most significant component of the modelling we performed as part of the project was the design, implementation, and interpretation of a custom stochastic model we designed to show that our proposed product would be "useful" in the real world.

We understand that computer models can become quite dry, particularly when explaining the details of their implementation, as if this is not done precisely, a small misunderstanding can be quickly amplified to an unexpected result, as the model's high complexity causes it to have a fairly so-called chaotic output.

As a result of this, we created an in-browser interactive implementation of the model, which plots the output graph of the model based on the user inputting initial parameter states. We intend that this can quickly, intuitively, and interactively show the function and results of the model, which can help inform the goal throughout the implementation explanation, and provide a top-level understanding even if the rest of this page were omitted.

### Introduction

To show that our proposed product would positively benefit the environment where it is proposed to be used, we wrote a computer model of the environment, with and without the product in use, and showed that when it is in use, the model scenario result improved.

#### Abstract

We propose a validated computational model of the spread of an antibiotic resistant pathogens in a hospital, with and without our diagnostic tool for quickly identifying it, and show that in a relevant scenario it reduces the presence of antibiotic resistant pathogens in our selected scenario, showing our product is beneficial in the real-world.

#### Motivation

The purpose of the model is two-fold:

- Demonstrating that our product is beneficial

- Understanding the use cases where it is most and least applicable

#### Assets

The whole project repository is available on GitHub at: [https://github.com/Warwick-iGEM-2021/modelling](https://github.com/Warwick-iGEM-2021/modelling)

The newest model version is also available: [Model V3](https://github.com/Warwick-iGEM-2021/modelling/blob/main/model_v4.py)

#### Model development

#### Model type

Our model is discrete time, stochastic, and compartmental:

- Compartmental means that the model is expressed in terms of the transitions between a set of states. The logic for these transitions forms a fundamental part of the model

- Stochastic means that the model is based on random probabilities, as opposed to a deterministic system of equations

  - A set of constant probabilities define the properties of the model
  - Transitions between states are chosen randomly with these constant probabilities

  These probabilities, and other variable aspects of the model, such as population size or how many drugs are used, are set as constant values at the top of the model.

  Initially, the model just had a parameter for how many different antibiotics are used, and all the associated probabilities (e.g. likelihood of recovery, likelihood of death, etc.) with these antibiotics were the same, but in the final version, the different antibiotics are named to more closely map to the real world, and they are allowed to have their own separate values for these probabilities. However, for convenience's sake, we introduce meta-parameters which can be used to set all the antibiotics to have the same probability in a given category.
  Below shows code for a default setting of these probabilities, the meaning of which will be explained further on:

  ```python
  # General model parameters
  NUM_TIMESTEPS = 100
  POPULATION_SIZE = 500
  INITIALLY_INFECTED = 10
  
  # Ordered list of drugs used, their properties, and the properties of their
  # resistant pathogens
  DRUG_NAMES = ["Penicillin", "Carbapenemase", "Colistin"]
  
  PROBABILITY_MOVE_UP_TREATMENT = 0.2
  TIMESTEPS_MOVE_UP_LAG_TIME = 5
  ISOLATION_THRESHOLD = DRUG_NAMES.index("Colistin")
  
  PRODUCT_IN_USE = True
  PROBABILIY_PRODUCT_DETECT = 1
  PRODUCT_DETECTION_LEVEL = DRUG_NAMES.index("Carbapenemase")
  
  ############################################################
  # Use these if you want to set all drugs to the same thing #
  ############################################################
  
  PROBABILITY_GENERAL_RECOVERY = 0
  PROBABILITY_TREATMENT_RECOVERY = 0.3
  PROBABILITY_MUTATION = 0.25
  PROBABILITY_DEATH = 0.015
  # Add time infected into consideration for death chance
  DEATH_FUNCTION = lambda p, t: round(min(0.001*t + p, 1), 4)
  # TODO: Make this more robust
  PROBABILITY_SPREAD = 0.25
  NUM_SPREAD_TO = 1
  
  ###########################################################################
  # Set these explicitly for more granular control, or use the above to set #
  # them all as a group                                                     #
  ###########################################################################
  
  # Lookup table of drug properties by their names
  DRUG_PROPERTIES = {}
  DRUG_PROPERTIES["Penicillin"] = (
      PROBABILITY_TREATMENT_RECOVERY,
  )
  DRUG_PROPERTIES["Carbapenemase"] = (PROBABILITY_TREATMENT_RECOVERY,)
  DRUG_PROPERTIES["Colistin"] = (PROBABILITY_TREATMENT_RECOVERY,)
  
  # Lookup table of resistance properties by their names
  NUM_RESISTANCES = len(DRUG_NAMES)
  RESISTANCE_PROPERTIES = {}
  RESISTANCE_PROPERTIES["None"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
  RESISTANCE_PROPERTIES["Penicillin"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
  RESISTANCE_PROPERTIES["Carbapenemase"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
  RESISTANCE_PROPERTIES["Colistin"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
  
  ```

  Additionally, there are internal settings, for example how the model outputs it results.

- Discrete time means that changes in the model occur at granular timesteps - like turns in a boards game

  Below shows the code for how operations are performed on every person in the population each timestep, and data about them recorded

  ```python
  # Make a new data handler for each simulation
  self.data_handler.__init__()
  
  # Repeat the simulation for a set number of timesteps
  for _ in range(NUM_TIMESTEPS):
  
      # For each person in the population
      for person in self.population:
  
          # Record the data throughout the model
          self.data_handler.record_person(person)
  
  ```

  

The model essentially is a modification of the standard SIR model for epidemic disease, adding more "compartments" for additional states people can take, when they are infected with increasingly antibiotic resistant pathogens.

![SIR Graph](C:\Users\egood\Desktop\modelling\writeup\diagrams\SIR_graph.png)

A diagram of the SIR model. Image source: [1]

### Implementation

The key features of the model can be split up into five semi-distinct sections:

#### 1. Pathogen and people

A pathogen with a probability of death and a probability of recovery spreads through the population.

- Patients have a small chance of recovering by themselves, or can be treated with antibiotics, which have a larger chance of curing them

- Different strains of the pathogen exist, which are resistant to different antibiotics
- Pathogens can mutate to more resistant strains in specific circumstances explained in the mutation section

- When they have recovered, they become immune to the all strains of the pathogen irrespective to their resistances

- Patients also have a small chance of dying due to the pathogen

Hence, patients can be in any of the disjoint states: uninfected, infected (possibly with resistance), immune, or dead.

In the limit of time to infinity, all individuals will be either uninfected, immune or dead, as they will all either not be infected in the first place, or recover or die from the pathogen.

Below shows the state transition diagram of every state a person within the population can take (for reasons discussed later in the treatment section, pathogenic resistances to antibiotics will occur in a set order):

![General state transition diagram](C:\Users\egood\Desktop\modelling\writeup\diagrams\general.PNG)



Below shows a state transition diagram of a person centred around the state of being infected with a pathogen resistant to antibiotic $$n$$ in the precedence of antibiotics:

![Specific state transition diagram](C:\Users\egood\Desktop\modelling\writeup\diagrams\specific_none.png)

#### 2. Treatment and mutation

Antibiotics are used in a specific order, which are numbered accordingly for clarity (with $$1$$ being the first administered, and $$n$$ being the last for antibiotics $$1..n$$ ). This is to simulate the real-world, where different antibiotics are used in a tiered system, reserving the last for highly dangerous, multi-drug resistant pathogens - and is an important aspect of our model, as our product attempts to identify CRE, which are a type of these resistant pathogens.

Pathogens have a small chance of mutating to develop resistance to antibiotics being used to treat them, as such strains will only become dominant when there is a pressure giving them a survival advantage.

```python
# Handle Mutation to higher resistance due to treatment
if decision(person.infection.mutation_probability):
    person.mutate_infection()
```

Below shows the same specified diagram used above, with additional information about the mutation step to elucidate it:

![Specific state transition diagram with mutation explanation](C:\Users\egood\Desktop\modelling\writeup\diagrams\specific_mutation.png)

The pathogen is modelled as being immediately symptomatic, meaning doctors can immediately identify a patient is infected with it, but they cannot quickly identify whether or not they have a resistant strain if our product is not in use.

Once a person becomes infected, treatment with the lowest tier of antibiotics becomes immediately, as they are immediately symptomatic.

If the pathogen is resistant to the antibiotic, the patient still has the opportunity to make a recovery on their own, but the antibiotic will have no effect, whereas if the pathogen is not, the patient has the opportunity  to recover both on their own, and via the antibiotic - increasing their likelihood of recovery each timestep.

Since multiple antibiotics are used in a tiered system, there must be a mechanism to move to a higher antibiotic.

There are a number of days which can be set as a parameter for the model, before which the same antibiotic will be used, then after this is exceeded a probability parameter is used each day to decide whether they will me moved up to a higher treatment tier.

```python
# Handle increasing treatment
if person.treatment is None:
    # If the person is infected but are not being treated
    # with **anything**, start them on the lowest tier
    # treatment (we can know that the person is infected,
    # but not which tier they are on, without diagnostic
    # tools, as we can see they are sick)
    person.treatment = Treatment()
else:
    # If the person has been treated for a number of
    # consecutive days with the, a certain probability is
    # exceeded, move them up a treatment tier
    time_cond = person.treatment.time_treated > TIMESTEPS_MOVE_UP_LAG_TIME
    rand_cond = decision(PROBABILITY_MOVE_UP_TREATMENT)
    if time_cond and rand_cond:
        person.increase_treatment()
```

#### 3. Spread

Disease can spread from infected patients to uninfected patients, and patients with a less resistant strain. The likelihood of this occurring, and the number of people spread to each time can be controlled as parameters

```python
# Spread the infection strains throughout the population
# We need a deepcopy operation, to prevent someone who has just
# been spread to in this timestep spreading the thing they've
# just received, so technically don't have yet
updated_population = deepcopy(self.population)
for person in self.population:
    if person.infection is not None and decision(PROBABILITY_SPREAD):
        for receiver in sample(updated_population, NUM_SPREAD_TO):
            person.spread_infection(receiver)
self.population = updated_population[:]
```

#### 4. Isolation

Patients can be put into isolation, preventing the spreading the disease. This is the main place where the our product differentiates itself.

Without our product, a person is put in isolation when they exceed a threshold of **treatment**

With our product, since it provides a fast testing mechanism for highly resistant strains, patients can be detected as having the resistant strain, they are put into isolation when they exceed a threshold of **having the resistant strain**

```python
# Isolate if in high enough treatment class (which
# is not the same as infection class - this will
# likely lag behind)
treatment_tier = Infection.get_tier_from_resistance(person.treatment.drug)
if treatment_tier >= ISOLATION_THRESHOLD:
    person.isolate()

# Handle use of the product
if PRODUCT_IN_USE and decision(PROBABILIY_PRODUCT_DETECT):
    if person.infection.get_tier() >= PRODUCT_DETECTION_LEVEL:
        # Put people into isolation if our product detects
        # them as being infected
        person.isolate()
```

Below shows the same specified diagram used above, with additional information about the isolation step to elucidate it:

![Specific state transition diagram with isolation explanation](C:\Users\egood\Desktop\modelling\writeup\diagrams\specific_isolation.png)

#### 5. Recovery and death

As discussed in section (1), each timestep, patients can recover (either naturally or via treatment), and patients can die.

Recovery makes the patients immune, meaning they cannot be infected again, essentially removing them from the system. Death also essentially removes patients from the system, as there cannot be any more state changes after death.

```python
# Handle Recovery generally or by treatment if currently infected
general_recovery = decision(person.infection.general_recovery_probability)
treatment_recovery = (person.correct_treatment() and
                    decision(person.treatment.treatment_recovery_probability))
if general_recovery or treatment_recovery:
    person.recover_from_infection()
    # Don't do anything else, as infection/treatment will
    # now be set to None
    continue

# Handle deaths due to infection
death_probability = person.infection.death_function(
    person.infection.death_probability,
    person.time_infected
)
if decision(death_probability):
    person.die()
    # Don't do anything else, as infection/treatment will
    # now be set to None
    continue
```

The goal is to create a situation where in the limit of time, the number of uninfected and immune people is maximised, and the number of dead people is minimised.

### Testing and validation

It is important to remember that computer models are not infallible. It is impossible for a computer model of a system to "perfectly" emulate the real system, as that would require total simulation of the entire universe, which is evidently unfeasible. However, closely approximate models provide a wealth of information when correctly implemented, and can provide a level of abstraction to make the applicable in a wide variety of cases.

To ensure that models are sufficiently accurate to the real-world scenario they are trying to emulate, it is important to test and validate them.

#### Types of testing

*Reference books on how to test and validate model*

#### Manual testing

#### Automated testing



### Contextualisation

*Due to the flexibility of the model, its parameters can be adjusted to simulate the spread of many real-world diseases. Adding such context to the model helps us better understand better how our product could improve the situation in such scenarios.*

#### Selected scenario

*Here we have chosen to use Neo-natal Bacterial Meningitis as an example. The disease can easily be spread within hospitals by medical staff and often has a deadly outcome [2], all of which can be simulated in the model. Furthermore, since the last line of treatment of meropenem, a carbapenem, it is relevant to the use of our product.*

*The parameters of the model have hence been adjusted because:*

1. *NBM has two lines of treatment (amoxicillin + cefotaxime/ceftriaxone, then meropenem) [3], the model has two levels of treatment and corresponding resistance levels.*
2. *There is a 100% mortality rate of untreated NBM [4], there is no chance of recovery if the pathogen is resistant against the current antibiotic in use.*
3. *There is 40% overall mortality [4] , parameters have been adjusted to end up with a 40% mortality rate*



The input parameters for the model of this scenario are:

```python
# General model parameters
NUM_TIMESTEPS = 100
POPULATION_SIZE = 500
INITIALLY_INFECTED = 10

# Ordered list of drugs used, their properties, and the properties of their
# resistant pathogens
DRUG_NAMES = ["Penicillin", "Carbapenemase", "Colistin"]

PROBABILITY_MOVE_UP_TREATMENT = 0.2
TIMESTEPS_MOVE_UP_LAG_TIME = 5
ISOLATION_THRESHOLD = DRUG_NAMES.index("Colistin")

PRODUCT_IN_USE = True
PROBABILIY_PRODUCT_DETECT = 1
PRODUCT_DETECTION_LEVEL = DRUG_NAMES.index("Carbapenemase")

############################################################
# Use these if you want to set all drugs to the same thing #
############################################################

PROBABILITY_GENERAL_RECOVERY = 0
PROBABILITY_TREATMENT_RECOVERY = 0.3
PROBABILITY_MUTATION = 0.25
PROBABILITY_DEATH = 0.015
# Add time infected into consideration for death chance
DEATH_FUNCTION = lambda p, t: round(min(0.001*t + p, 1), 4)
# TODO: Make this more robust
PROBABILITY_SPREAD = 0.25
NUM_SPREAD_TO = 1

###########################################################################
# Set these explicitly for more granular control, or use the above to set #
# them all as a group                                                     #
###########################################################################

# Lookup table of drug properties by their names
DRUG_PROPERTIES = {}
DRUG_PROPERTIES["Penicillin"] = (
    PROBABILITY_TREATMENT_RECOVERY,
)
DRUG_PROPERTIES["Carbapenemase"] = (PROBABILITY_TREATMENT_RECOVERY,)
DRUG_PROPERTIES["Colistin"] = (PROBABILITY_TREATMENT_RECOVERY,)

# Lookup table of resistance properties by their names
NUM_RESISTANCES = len(DRUG_NAMES)
RESISTANCE_PROPERTIES = {}
RESISTANCE_PROPERTIES["None"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
RESISTANCE_PROPERTIES["Penicillin"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
RESISTANCE_PROPERTIES["Carbapenemase"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
RESISTANCE_PROPERTIES["Colistin"] = (PROBABILITY_GENERAL_RECOVERY, PROBABILITY_MUTATION, PROBABILITY_SPREAD, NUM_SPREAD_TO, PROBABILITY_DEATH, DEATH_FUNCTION,)
```

#### Results

Raw data output graphs for with and without

short explanation of what each line means 

#### Analysis

Whatever analysis you think is relevant

Final headline chart which simply shows our product making things better (two lines, one labelled without, one labelled with)

​	- I might add something additional here (box plot of how much better our stuff is with different random seeds?)

### Conclusion

Given the fact that we have tested and validated our model to be sufficiently representative of the real world, and the model output indicates that the use of the product reduces the presence of antibiotic resistant pathogenic strains in our selected scenario, we conclude that our product is beneficial.

### Discussion

Some common questions about the model are answered below:

- Q. Is the model realistic

  A. No, very little about it is realistic. It is an abstraction of the real world which discards many unnecessary complexities, in order to simply and efficiently model how resistance spreads and is combatted. It is not viable to make a wholly realistic model, as this inevitable turns into a "hospital simulator", and would be too complex to design, and take too long to run on current computers.

- Q. Is the model useful

  A. Yes, because it provides several helpful insights:

  - The impact our product will have on the spread of resistance just by quickly detecting who to put into isolation
  - Whether higher or lower mortality or transmissibility of a disease increase or decrease the effectiveness

- Q. What potential improvements are there

  A. It would be possible to add additional features to the model to make it more realistic, for example:

  - Spatial considerations – e.g. modelling multiple wards with movement between them
  - Asymptomatic transmission periods of infection

  however, these are beyond the scope of our project

- How does the model compare to other existent ones

- Q. Can the model be applied to current issues, i.e. the COVID pandemic

  A. Since the model is a very generic abstraction of the real world, by adjusting it's parameters, a vast amount of different scenarios can be modelled. The key issue in adapting it to different scenarios is if they fit the inherent logic and states hard-coded into it. Since COVID is a viral infection, as opposed to a bacterial infection, antibiotics cannot be used to treat it, so the tiered system of antibiotic uses fits less cleanly to it, however, they could instead be considered as increasingly aggressive treatment options, to which it also grows resistant. However, the logic around our product would not apply, as viral infections are not affected by carbapenem, which is the antibiotic we focus on.

### References

[1] Simon, Cory M., 2020. *_The SIR dynamic model of infectious disease transmission and its analogy with chemical kinetics_*. Available at [https://peerj.com/articles/pchem-14/](https://peerj.com/articles/pchem-14/) [Accessed 27 September 2021]. DOI: 10.7717/peerj-pchem.14

[2] Şah İpek, M., 2019. *_Neonatal Bacterial Meningitis_*. [online] IntechOpen. Available at: [https://www.intechopen.com/chapters/68042](https://www.intechopen.com/chapters/68042). DOI: 10.5772/intechopen.87118

[3] Meningitis Research Foundation, 2017. *_Management of Bacterial Meningitis in infants <3 months_*. Available at: [https://www.meningitis.org/getmedia/75ce0638-a815-4154-b504-b18c462320c8/Neo-Natal-Algorithm-Nov-2017](https://www.meningitis.org/getmedia/75ce0638-a815-4154-b504-b18c462320c8/Neo-Natal-Algorithm-Nov-2017) [pdf]

[4] Tesini, B., 2020. *_Neonatal Bacterial Meningitis_*. [online] MSD Manual Professional Edition. Available at: [https://www.msdmanuals.com/en-gb/professional/pediatrics/infections-in-neonates/neonatal-bacterial-meningitis](https://www.msdmanuals.com/en-gb/professional/pediatrics/infections-in-neonates/neonatal-bacterial-meningitis) [Accessed 23 September 2021].



## NUPAC modelling

## COPASI modelling
