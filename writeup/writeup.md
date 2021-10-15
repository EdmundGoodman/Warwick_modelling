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

The newest model version is also available: [Model V3](https://github.com/Warwick-iGEM-2021/modelling/blob/main/src/model.py)

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

The key features of the model can be split up into five semi-distinct sections, which are enumerated in the sections below.

In each timestep of the model, each of these features are applied to mutate the state of the population. The order in which they are applied, whilst arbitrary, slightly effects the results of the model, in the sense that different application orders would give different results given the same random seed, but any application order can reasonably be considered a adequate model of the system. In our implementation, this order is:

```
FOR EACH person in the population
	Record the state of the person
	Increase treatment
	Isolate based on treatment level
	IF product is in use
		Isolate based on product
	ENDIF
	Recovery
	Mutation
	Death
ENDFOR
Spread through the population
```

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

### Software engineering

#### Automated testing

Whilst testing strategies and reasoning for testing are discussed in the "Testing and validation" section, the implementation of the testing is a point of interest in its own right. We used the `unittest` module in Python to implement tests for the source code.

An example of a test is as follows, where we check that the boundary case of no-one being infected to start results in no infections for the entire model one. Whilst this might seem trivial, if it fails it is clear something is very wrong with the model, which might be a subtle result of a change made during development, and hence can prevent confusion about model results not making sense by showing that the problem is in the model implementation, not the analysis.

```python
class TestModel(unittest.TestCase):
    def test_empty_model(self):
        """Test that a model with no infected people always stays fully uninfected"""
        # Change parameters for the test setup and run the test
        Params.INITIALLY_INFECTED = 0
        m = run()
        self.assertEqual(m.data_handler.get_uninfected_data(),
                         [Params.POPULATION_SIZE]*Params.NUM_TIMESTEPS)
        self.assertEqual(m.data_handler.get_infected_data()[0],
                         [0]*Params.NUM_TIMESTEPS)
        reset_params()
```

An interesting note about these tests is despite the fact they are written as unit tests, which normally refers to tests with a fixed input, these can be thought of as being tested with different inputs dependent on the result of the random number generator.

```python
class TestModel(unittest.TestCase):
    def test_empty_model(self):
        """Test that a model with no infected people always stays fully uninfected"""
        # Change parameters for the test setup and run the test
        Params.INITIALLY_INFECTED = 0
        
        # Repeat the testing phase many times, with random number generation as the
        # function input differing each time
        for _ in range(100):
            m = run()
            self.assertEqual(m.data_handler.get_uninfected_data(),
                             [Params.POPULATION_SIZE]*Params.NUM_TIMESTEPS)
            self.assertEqual(m.data_handler.get_infected_data()[0],
                             [0]*Params.NUM_TIMESTEPS)
        
        reset_params()
```

If the tests are run many times, with many different resulting random number inputs, these unit tests can now be thought of as property based tests. This refers to checking that a function fulfils a property by randomly providing it with values from its input domain, and checking that the resultant outputs fulfil the property. This is a strategy which was pioneered in the functional programming language Haskell https://medium.com/criteo-engineering/introduction-to-property-based-testing-f5236229d237, and is often considered preferable to unit based tests. https://www.cognitect.com/blog/2013/11/26/better-than-unit-tests

#### Version control and CI/CD

Having implemented a robust testing strategy, we now had all the building blocks for a continuous integration/continuous development workflow, as shown below:

![CI/CD diagram](https://www.redhat.com/cms/managed-files/styles/wysiwyg_full_width/s3/ci-cd-flow-desktop.png?itok=2EX0MpQZ)

The build phase is relatively simple - writing the code in an editor of your choice, and running it with the Python interpreter, and the testing phase is discussed above.

Throughout the entire project, we used `git` as version control, due to the vast number of reasons `git` is helpful in software development. From this, we linked the project to a remote repository on GitHub, which forms the main way to access the most up to data code. This forms the merge and continuous delivery steps.

We chose not to automate publishing the code to PyPI (discussed below), which could be considered the production aspect of the modelling, as the project is still under active development, and minor changes to the repository should not necessarily be pushed, as their general stability and usefulness is not fully known.

#### Transpilation to JavaScript

In order to create the toy model, we needed to use a language which can be run client side in the browser. Since Python cannot do this, we needed to convert the source code into a language which can - with the obvious choice being JavaScript.

Instead of manually re-writing the entire model into JavaScript, we decided to use an automated tool to do it for us. This class of tool is called a transpiler, which converts between two languages in the same tier in the language complexity hierarchy (e.g. two high level languages). We considered a number of tools, with the main decision being between [Brython](https://brython.info/), a runtime transpiler which translates the Python code to JavaScript on the fly, and [Transcrypt](https://www.transcrypt.org/), a build-time transpiler which translates the code beforehand. We decided to use Transcrypt, as it offers better performance, having pre-compiled the code, and since it allows an easier integration into the JavaScript DOM.

The transpilation process was not totally seamless, as some language properties in python are not supported in JavaScript, for example named parameters and adding lists, and not all of the libraries used were supported by Transcrypt, meaning some of the `random` methods had to be implemented by hand, and the output graphs and excel exporter had to be totally removed.

In order to display the output in a visual manner, we used the `Chart.js` package, which is commonly used for client side data plotting.

#### Uploading to PyPI

Since we developed our model in python, and it follows best practices as opposed to just being a standalone script, uploading the repository to PyPI, the Python package index, was fairly trivial.

Doing this greatly simplifies the way in which the package can be distributed. Instead of cloning the repository, and running the code directly through that:

```bash
git clone https://github.com/Warwick-iGEM-2021/modelling
cd modelling/tiered-antibiotic-resistance-model
python3 model.py
```

The module can be installed using `pip` on the command line, then just imported directly in a Python file:

```bash
pip install tiered_antibiotic_resistance_model
```

```python
from tiered_antibiotic_resistance_model import *
run_and_output()
```

And the parameters of the model can be set within the other Python file by directly manipulating the `Param` object, instead of having to go into the source code and change them in the actual model, which is not a best practice.

The [PyPI page for the project is accessible here](https://pypi.org/project/tiered-antibiotic-resistance-model/2.0.1/)

### Testing and validation

It is important to remember that computer models are not infallible. It is impossible for a computer model of a system to "perfectly" emulate the real system, as that would require total simulation of the entire universe, which is evidently unfeasible. However, closely approximate models provide a wealth of information when correctly implemented, and can provide a level of abstraction to make the applicable in a wide variety of cases.

To ensure that models are sufficiently accurate to the real-world scenario they are trying to emulate, it is important to test and validate them.

#### Levels of validation

1. Grounding
2. Calibrating
3. Verification
4. Harmonization

#### Types of testing

*Reference books on how to test and validate model*

#### Manual testing

#### Automated testing

Wrote tests of the model using the Python unittest library = allows continuous integration



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

	- I might add something additional here (box plot of how much better our stuff is with different random seeds?)

### Development and future work

Throughout the development process, we presented the modelling work to other members of our team and our principal investigators, along with an external expert in the field, [Alex Darlington](https://warwick.ac.uk/fac/sci/eng/people/alexander_darlington/). Presenting our work was incredibly helpful not only for ensuring that we could explain everything fully and understandably, but also as we received useful suggestions about ways we could improve the model.

### Conclusion

Given the fact that we have tested and validated our model to be sufficiently representative of the real world, and the model output indicates that the use of the product reduces the presence of antibiotic resistant pathogenic strains in our selected scenario, we conclude that our product is beneficial.

There are a number of aspects in which we could expand our model into if we did not have the time constraints of the iGEM competition, but we believe that the model in it's current state both achieves it's goal of showing our product is beneficial, along with being a useful tool for understanding the issue of antibiotic resistance in its own right.

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
