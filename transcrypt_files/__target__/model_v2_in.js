// Transcrypt'ed from Python, 2021-09-14 22:27:51
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {choice, random, seed} from './random.js';
var __name__ = '__main__';
export var NUM_TIMESTEPS = 50;
export var POPULATION_SIZE = 5000;
export var NUM_RESISTANCE_TYPES = 3;
export var PROBABILITY_GENERAL_RECOVERY = 0.01;
export var PROBABILITY_TREATMENT_RECOVERY = 0.2;
export var PROBABILITY_MUTATION = 0.02;
export var PROBABILITY_MOVE_UP_TREATMENT = 0.2;
export var ISOLATION_THRESHOLD = 2;
export var PROBABILITY_DEATH = 0.01;
export var PROBABILITY_SPREAD = 1;
export var NUM_SPREAD_TO = 1;
export var PRODUCT_IN_USE = true;
export var PROBABILIY_PRODUCT_DETECT = 0.5;
export var RANDOM_SEED = 0;
export var REPORT_PROGRESS = true;
export var REPORT_PERCENTAGE = 5;
export var PRINT_DATA = true;
export var OUTPUT_PADDING = len (str (POPULATION_SIZE));
export var REPORT_MOD_NUM = int (NUM_TIMESTEPS / (100 / REPORT_PERCENTAGE));
export var RESISTANCE_NAMES = (function () {
	var __accu0__ = [];
	for (var i = 0; i < NUM_RESISTANCE_TYPES; i++) {
		__accu0__.append (str (i + 1));
	}
	return __accu0__;
}) ();
export var Infection =  __class__ ('Infection', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, resistances) {
		if (typeof resistances == 'undefined' || (resistances != null && resistances.hasOwnProperty ("__kwargtrans__"))) {;
			var resistances = null;
		};
		if (resistances !== null) {
			self.resistances = resistances;
		}
		else {
			self.resistances = (function () {
				var __accu0__ = [];
				for (var py_name of RESISTANCE_NAMES) {
					__accu0__.append ([py_name, false]);
				}
				return dict (__accu0__);
			}) ();
		}
	});},
	get make_resistant () {return __get__ (this, function (self, resistance) {
		self.resistances [resistance] = true;
	});},
	get is_resistant () {return __get__ (this, function (self, resistance) {
		return self.resistances [resistance];
	});},
	get get_tier () {return __get__ (this, function (self) {
		for (var i of py_reversed (range (NUM_RESISTANCE_TYPES))) {
			if (self.resistances [RESISTANCE_NAMES [i]] == true) {
				return i;
			}
		}
		return -(1);
	});},
	get get_resistances_string () {return __get__ (this, function (self) {
		var string = ','.join ((function () {
			var __accu0__ = [];
			for (var [k, v] of self.resistances.py_items ()) {
				if (v) {
					__accu0__.append (k);
				}
			}
			return __accu0__;
		}) ());
		if (string == '') {
			return '#';
		}
		return string;
	});},
	get duplicate () {return __get__ (this, function (self) {
		return Infection (__kwargtrans__ ({resistances: (function () {
			var __accu0__ = [];
			for (var [k, v] of self.resistances.py_items ()) {
				__accu0__.append ([k, v]);
			}
			return dict (__accu0__);
		}) ()}));
	});},
	get __repr__ () {return __get__ (this, function (self) {
		var resistances_string = self.get_resistances_string ();
		if (resistances_string == '#') {
			return 'infected';
		}
		return 'infected with resistances: {}'.format (resistances_string);
	});}
});
export var Treatment =  __class__ ('Treatment', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, drug) {
		if (typeof drug == 'undefined' || (drug != null && drug.hasOwnProperty ("__kwargtrans__"))) {;
			var drug = RESISTANCE_NAMES [0];
		};
		self.drug = drug;
	});},
	get next_treatment () {return __get__ (this, function (self) {
		var drug_index = RESISTANCE_NAMES.index (self.drug);
		if (drug_index < NUM_RESISTANCE_TYPES - 1) {
			self.drug = RESISTANCE_NAMES [drug_index + 1];
		}
	});},
	get treats_infection () {return __get__ (this, function (self, infection) {
		return !(infection.is_resistant (self.drug));
	});},
	get duplicate () {return __get__ (this, function (self) {
		return Treatment (__kwargtrans__ ({drug: self.drug}));
	});},
	get __repr__ () {return __get__ (this, function (self) {
		if (self.drug !== null) {
			return 'treated with drug: {}'.format (self.drug);
		}
		return 'untreated';
	});}
});
export var Person =  __class__ ('Person', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, infection, treatment, isolated, immune, alive) {
		if (typeof infection == 'undefined' || (infection != null && infection.hasOwnProperty ("__kwargtrans__"))) {;
			var infection = null;
		};
		if (typeof treatment == 'undefined' || (treatment != null && treatment.hasOwnProperty ("__kwargtrans__"))) {;
			var treatment = null;
		};
		if (typeof isolated == 'undefined' || (isolated != null && isolated.hasOwnProperty ("__kwargtrans__"))) {;
			var isolated = false;
		};
		if (typeof immune == 'undefined' || (immune != null && immune.hasOwnProperty ("__kwargtrans__"))) {;
			var immune = false;
		};
		if (typeof alive == 'undefined' || (alive != null && alive.hasOwnProperty ("__kwargtrans__"))) {;
			var alive = true;
		};
		self.infection = infection;
		self.treatment = treatment;
		self.isolated = isolated;
		self.immune = immune;
		self.alive = alive;
	});},
	get recover_from_infection () {return __get__ (this, function (self) {
		self.__init__ (__kwargtrans__ ({immune: true}));
	});},
	get mutate_infection () {return __get__ (this, function (self) {
		if (self.infection !== null && self.treatment !== null) {
			self.infection.make_resistant (self.treatment.drug);
		}
	});},
	get increase_treatment () {return __get__ (this, function (self) {
		if (self.treatment !== null) {
			self.treatment.next_treatment ();
		}
	});},
	get correct_treatment () {return __get__ (this, function (self) {
		if (self.treatment !== null) {
			return self.treatment.treats_infection (self.infection);
		}
		return false;
	});},
	get spread_infection () {return __get__ (this, function (self, other) {
		if (self.infection === null) {
			return null;
		}
		var directional = other.infection === null || self.infection.get_tier () > other.infection.get_tier ();
		var susceptible = !(other.immune) && other.alive;
		var contactable = !(self.isolated) && !(other.isolated);
		if (directional && susceptible && contactable) {
			other.infection = self.infection.duplicate ();
		}
	});},
	get isolate () {return __get__ (this, function (self) {
		self.isolated = true;
	});},
	get deisolate () {return __get__ (this, function (self) {
		self.isolated = false;
	});},
	get die () {return __get__ (this, function (self) {
		self.alive = false;
	});},
	get duplicate () {return __get__ (this, function (self) {
		return Person (__kwargtrans__ ({infection: (self.infection === null ? null : self.infection.duplicate ()), treatment: (self.treatment === null ? null : self.treatment.duplicate ()), isolated: self.isolated, immune: self.immune, alive: self.alive}));
	});},
	get __repr__ () {return __get__ (this, function (self) {
		if (!(self.alive)) {
			return 'Dead person';
		}
		else if (self.immune) {
			return 'Immune person';
		}
		else if (self.infection !== null) {
			return 'Person {} and {}'.format (self.infection, self.treatment);
		}
		return 'Uninfected person';
	});}
});
export var Model =  __class__ ('Model', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, population) {
		if (typeof population == 'undefined' || (population != null && population.hasOwnProperty ("__kwargtrans__"))) {;
			var population = null;
		};
		if (population === null) {
			self.population = (function () {
				var __accu0__ = [];
				for (var _ = 0; _ < POPULATION_SIZE; _++) {
					__accu0__.append (Person ());
				}
				return __accu0__;
			}) ();
		}
		else {
			self.population = population;
		}
		self.data_handler = DataHandler ();
	});},
	get run () {return __get__ (this, function (self) {
		self.data_handler.__init__ ();
		for (var _ = 0; _ < NUM_TIMESTEPS; _++) {
			for (var person of self.population) {
				self.data_handler.record_person (person);
				if (person.infection !== null && person.alive) {
					if (person.treatment === null) {
						person.treatment = Treatment ();
					}
					else {
						if (decision (PROBABILITY_MOVE_UP_TREATMENT)) {
							person.increase_treatment ();
						}
						if (PRODUCT_IN_USE && decision (PROBABILIY_PRODUCT_DETECT)) {
							if (person.infection.resistances [str (ISOLATION_THRESHOLD)]) {
								person.isolate ();
							}
						}
						else if (int (person.treatment.drug) >= ISOLATION_THRESHOLD) {
							person.isolate ();
						}
					}
					var general_recovery = decision (PROBABILITY_GENERAL_RECOVERY);
					var treatment_recovery = person.correct_treatment () && decision (PROBABILITY_TREATMENT_RECOVERY);
					if (general_recovery || treatment_recovery) {
						person.recover_from_infection ();
					}
					if (decision (PROBABILITY_MUTATION)) {
						person.mutate_infection ();
					}
					if (decision (PROBABILITY_DEATH)) {
						person.die ();
					}
				}
			}
			var updated_population = (function () {
				var __accu0__ = [];
				for (var p of self.population) {
					__accu0__.append (p.duplicate ());
				}
				return __accu0__;
			}) ();
			for (var person of self.population) {
				if (person.infection !== null && decision (PROBABILITY_SPREAD)) {
					for (var receiver of sample (updated_population, NUM_SPREAD_TO)) {
						person.spread_infection (receiver);
					}
				}
			}
			self.population = updated_population.__getslice__ (0, null, 1);
			self.data_handler.process_timestep_data ();
		}
	});},
	get __repr__ () {return __get__ (this, function (self) {
		return 'Model';
	});}
});
export var decision = function (probability) {
	return random () < probability;
};
export var sample = function (population, k) {
	if (!((0 <= k && k <= len (population)))) {
		var __except0__ = ValueError ('Sample larger than population or is negative');
		__except0__.__cause__ = null;
		throw __except0__;
	}
	var indices = list (range (len (population)));
	var sample = [];
	for (var _ = 0; _ < k; _++) {
		var index = choice (indices);
		indices.remove (index);
		sample.append (population [index]);
	}
	return sample;
};
export var DataHandler =  __class__ ('DataHandler', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		self.time = [];
		self.ys_data = (function () {
			var __accu0__ = [];
			for (var _ = 0; _ < 4 + NUM_RESISTANCE_TYPES; _++) {
				__accu0__.append ([]);
			}
			return __accu0__;
		}) ();
		self.labels = (['Infected'] + list (map ((function __lambda__ (x) {
			return 'Resistance ' + x;
		}), RESISTANCE_NAMES))) + ['Dead', 'Immune', 'Uninfected'];
		self.non_disjoint = [[]];
		self.non_disjoint_labels = ['Isolated'];
		self.timestep = -(1);
		self._new_timestep_vars ();
	});},
	get _new_timestep_vars () {return __get__ (this, function (self) {
		self.num_infected_stages = (function () {
			var __accu0__ = [];
			for (var _ = 0; _ < NUM_RESISTANCE_TYPES + 1; _++) {
				__accu0__.append (0);
			}
			return __accu0__;
		}) ();
		self.num_dead = 0;
		self.num_immune = 0;
		self.num_uninfected = 0;
		self.num_isolated = 0;
		self.timestep++;
	});},
	get record_person () {return __get__ (this, function (self, person) {
		if (person.immune) {
			self.num_immune++;
		}
		else if (!(person.alive)) {
			self.num_dead++;
		}
		else if (person.infection === null) {
			self.num_uninfected++;
		}
		else {
			self.num_infected_stages [person.infection.get_tier () + 1]++;
		}
		if (person.isolated) {
			self.num_isolated++;
		}
	});},
	get _preprocess_disjoint_labels () {return __get__ (this, function (self) {
		if (GRAPH_TYPE == 'line') {
			var datas = [];
			for (var i = 0; i < NUM_RESISTANCE_TYPES + 1; i++) {
				datas.append ((function () {
					var __accu0__ = [];
					for (var x of zip (...self.ys_data.__getslice__ (i, -(3), 1))) {
						__accu0__.append (sum (x));
					}
					return __accu0__;
				}) ());
			}
			datas.extend (self.ys_data.__getslice__ (-(3), null, 1));
			datas.extend (self.non_disjoint);
			var final_labels = self.labels + self.non_disjoint_labels;
			return tuple ([datas, final_labels]);
		}
		return tuple ([self.ys_data, self.labels]);
	});},
	get _print_current_data () {return __get__ (this, function (self) {
		print ('uninfected: {}, immune: {}, dead: {}, infected: {}, isolated: {}'.format (str (self.num_uninfected), str (self.num_immune), str (self.num_dead), ('[' + ', '.join ((function () {
			var __accu0__ = [];
			for (var x of self.num_infected_stages) {
				__accu0__.append (str (x));
			}
			return __accu0__;
		}) ())) + ']', str (self.num_isolated)));
	});},
	get _report_model_state () {return __get__ (this, function (self) {
		if (__mod__ (self.timestep, REPORT_MOD_NUM) == 0) {
			if (REPORT_PROGRESS && !(PRINT_DATA)) {
				print ('{}% complete'.format (int ((self.timestep / int (NUM_TIMESTEPS / 10)) * 10)));
			}
			if (PRINT_DATA) {
				if (REPORT_PROGRESS) {
					print ('{}% complete'.format (str (int ((self.timestep / int (NUM_TIMESTEPS / 10)) * 10))), __kwargtrans__ ({end: ' - '}));
				}
				self._print_current_data ();
			}
		}
	});},
	get process_timestep_data () {return __get__ (this, function (self) {
		for (var [j, v] of enumerate (self.num_infected_stages)) {
			self.ys_data [j].append (v);
		}
		self.ys_data [len (self.ys_data) - 3].append (self.num_dead);
		self.ys_data [len (self.ys_data) - 2].append (self.num_immune);
		self.ys_data [len (self.ys_data) - 1].append (self.num_uninfected);
		self.non_disjoint [0].append (self.num_isolated);
		self.time.append (self.timestep);
		self._report_model_state ();
		self._new_timestep_vars ();
	});}
});
if (__name__ == '__main__') {
	if (RANDOM_SEED !== null) {
		seed (RANDOM_SEED);
	}
	var population = (function () {
		var __accu0__ = [];
		for (var _ = 0; _ < POPULATION_SIZE - 10; _++) {
			__accu0__.append (Person ());
		}
		return __accu0__;
	}) ();
	for (var _ = 0; _ < 10; _++) {
		population.append (Person (__kwargtrans__ ({infection: Infection ()})));
	}
	var m = Model (__kwargtrans__ ({population: population}));
	m.run ();
}

//# sourceMappingURL=model_v2_in.map