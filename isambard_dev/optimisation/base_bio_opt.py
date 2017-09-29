"""Base class for bio-inspired optimizers."""

from concurrent import futures
import datetime
import os
import sys

from deap import base, creator, tools
import numpy
import matplotlib.pylab as plt

from external_programs.profit import run_profit


def default_build(spec_seq_params):
    specification, sequence, params = spec_seq_params
    model = specification(*params)
    model.pack_new_sequences(sequence)
    return model


def buff_interaction_eval(ampal):
    return ampal.buff_interaction_energy.total_energy


def buff_internal_eval(ampal):
    return ampal.buff_internal_energy.total_energy


def make_rmsd_eval(reference_ampal):
    def rmsd_eval(ampal):
        ca, bb, aa = run_profit(
            ampal.pdb, reference_ampal,
            path1=False, path2=False)
        return bb
    return rmsd_eval


class BaseOptimizer:
    """Abstract base class for the evolutionary optimizers.

    Notes
    -----
    Not intended to be used directly, see the evolutionary
    optimizers for full documentation.
    """

    def __init__(self, specification, build_fn=None, eval_fn=None, **kwargs):
        self._params = {}
        self._params['specification'] = specification
        self._params.update(**kwargs)
        if sys.platform == 'win32':
            self._params['mp_disabled'] = True
            print('Multiprocessing for this module is currently unavailable'
                  'on Windows, only a single process will be used.')
        self.build_fn = build_fn
        self.eval_fn = eval_fn
        self.population = None
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        self.toolbox = base.Toolbox()
        self.parameter_log = []

    @classmethod
    def buff_interaction_eval(cls, specification, **kwargs):
        """Creates optimizer with default build and BUFF interaction eval.

        Notes
        -----
        Any keyword arguments will be propagated down to BaseOptimizer.

        Parameters
        ----------
        specification: ampal.assembly.specification
            Any assembly level specification.
        """
        instance = cls(build_fn=default_build,
                       eval_fn=buff_interaction_eval,
                       specification=specification,
                       **kwargs)
        return instance

    @classmethod
    def buff_internal_eval(cls, specification, **kwargs):
        """Creates optimizer with default build and BUFF interaction eval.
        
        Notes
        -----
        Any keyword arguments will be propagated down to BaseOptimizer.

        Parameters
        ----------
        specification: ampal.assembly.specification
            Any assembly level specification.
        """
        instance = cls(build_fn=default_build,
                       eval_fn=buff_internal_eval,
                       specification=specification,
                       **kwargs)
        return instance

    @classmethod
    def rmsd_eval(cls, specification, reference_ampal, **kwargs):
        """Creates optimizer with default build and RMSD eval.
        
        Notes
        -----
        Any keyword arguments will be propagated down to BaseOptimizer.

        Parameters
        ----------
        specification: ampal.assembly.specification
            Any assembly level specification.
        """
        eval_fn = make_rmsd_eval(reference_ampal)
        instance = cls(build_fn=default_build,
                       eval_fn=eval_fn,
                       specification=specification,
                       mp_disabled=True,
                       **kwargs)
        return instance

    def parse_individual(self, individual):
        """Converts a deap individual into a full list of parameters.
        Parameters
        ----------
        individual: deap individual from optimization
            Details vary according to type of optimization, but
            parameters within deap individual are always between -1
            and 1. This function converts them into the values used to
            actually build the model

        Returns
        -------
        fullpars: list
            Full parameter list for model building.
        """
        scaled_ind = []
        for i in range(len(self._params['value_means'])):
            scaled_ind.append(self._params['value_means'][i] + (
                individual[i] * self._params['value_ranges'][i]))
        fullpars = list(self._params['arrangement'])
        for k in range(len(self._params['variable_parameters'])):
            for j in range(len(fullpars)):
                if fullpars[j] == self._params['variable_parameters'][k]:
                    fullpars[j] = scaled_ind[k]
        return fullpars

    def run_opt(self, popsize, numgen, processors,
                plot=False, log=False, store_params=True, **kwargs):
        """
        Runs the optimizer.
        :param popsize:
        :param numgen:
        :param processors:
        :param plot:
        :param log:
        :param kwargs:
        :return:
        """
        self._params['popsize'] = popsize
        self._params['numgen'] = numgen
        self._params['processors'] = processors
        self._params['plot'] = plot
        self._params['log'] = log
        self._params['store_params'] = store_params
        # allows us to pass in additional arguments e.g. neighbours
        self._params.update(**kwargs)
        self.halloffame = tools.HallOfFame(1)
        self.stats = tools.Statistics(lambda thing: thing.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)
        self.logbook = tools.Logbook()
        self.logbook.header = ["gen", "evals"] + self.stats.fields
        self._params['model_count'] = 0
        start_time = datetime.datetime.now()
        self.initialize_pop()
        for g in range(self._params['numgen']):
            self.update_pop()
            self.halloffame.update(self.population)
            self.logbook.record(gen=g, evals=self._params['evals'],
                                **self.stats.compile(self.population))
            print(self.logbook.stream)
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time
        self._params['time_taken'] = time_taken
        print("Evaluated {0} models in total".format(
            self._params['model_count']))
        print("Best fitness is {0}".format(self.halloffame[0].fitness))
        print("Best parameters are {0}".format(self.parse_individual(
            self.halloffame[0])))
        for i, entry in enumerate(self.halloffame[0]):
            if entry > 0.95:
                print(
                    "Warning! Parameter {0} is at or near maximum allowed "
                    "value\n".format(i + 1))
            elif entry < -0.95:
                print(
                    "Warning! Parameter {0} is at or near minimum allowed "
                    "value\n".format(i + 1))
        if self._params['log']:
            self.log_results()
        if self._params['plot']:
            print('----Minimisation plot:')
            plt.figure(figsize=(5, 5))
            plt.plot(range(len(self.logbook.select('min'))),
                     self.logbook.select('min'))
            plt.xlabel('Iteration', fontsize=20)
            plt.ylabel('Score', fontsize=20)
        return

    def parameters(self, sequence, value_means, value_ranges, arrangement):
        """Relates the individual to be evolved to the full parameter string.

        Parameters
        ----------
        sequence: str
            Full amino acid sequence for specification object to be
            optimized. Must be equal to the number of residues in the
            model.
        value_means: list
            List containing mean values for parameters to be optimized.
        value_ranges: list
            List containing ranges for parameters to be optimized.
            Values must be positive.
        arrangement: list
            Full list of fixed and variable parameters for model
            building. Fixed values are the appropriate value. Values
            to be varied should be listed as 'var0', 'var1' etc,
            and must be in ascending numerical order.
            Variables can be repeated if required.
        """
        self._params['sequence'] = sequence
        self._params['value_means'] = value_means
        self._params['value_ranges'] = value_ranges
        self._params['arrangement'] = arrangement
        if any(x <= 0 for x in self._params['value_ranges']):
            raise ValueError("range values must be greater than zero")
        self._params['variable_parameters'] = []
        for i in range(len(self._params['value_means'])):
            self._params['variable_parameters'].append(
                "".join(['var', str(i)]))
        if len(set(arrangement).intersection(
                self._params['variable_parameters'])) != len(
                    self._params['value_means']):
            raise ValueError("argument mismatch!")
        if len(self._params['value_ranges']) != len(
                self._params['value_means']):
            raise ValueError("argument mismatch!")
        return

    def assign_fitnesses(self, targets):
        self._params['evals'] = len(targets)
        px_parameters = zip([self._params['specification']] * len(targets),
                            [self._params['sequence']] * len(targets),
                            [self.parse_individual(x) for x in targets])
        if (self._params['processors'] == 1) or (self._params['mp_disabled']):
            models = map(self.build_fn, px_parameters)
            fitnesses = map(self.eval_fn, models)
        else:
            with futures.ProcessPoolExecutor(
                    max_workers=self._params['processors']) as executor:
                models = executor.map(self.build_fn, px_parameters)
                fitnesses = executor.map(self.eval_fn, models)
        tars_fits = list(zip(targets, fitnesses))
        if 'store_params' in self._params:
            if self._params['store_params']:
                self.parameter_log.append(
                    [(self.parse_individual(x[0]), x[1]) for x in tars_fits])
        for ind, fit in tars_fits:
            ind.fitness.values = (fit,)
        return

    def generate(self):
        raise NotImplementedError("Will depend on optimizer type")

    def initialize_pop(self):
        raise NotImplementedError("Will depend on optimizer type")

    def update_pop(self):
        raise NotImplementedError("Will depend on optimizer type")

    def log_results(self):
        """Saves files for the minimization.

        Notes
        -----
        Currently saves a logfile with best individual and a pdb of
        the best model.
        """
        best_ind = self.halloffame[0]
        model_params = self.parse_individual(
            best_ind)  # need to change name of 'params'
        if 'output_path' in self._params:
            output_path = self._params['output_path']
        else:
            output_path = os.getcwd()
        if 'run_id' in self._params:
            run_id = self._params['run_id']
        else:
            run_id = '{:%Y%m%d-%H%M%S}'.format(
                datetime.datetime.now())
        with open('{0}/{1}_opt_log.txt'.format(
                output_path, run_id), 'w') as log_file:
            log_file.write('\nEvaluated {0} models in total\n'.format(
                self._params['model_count']))
            log_file.write('Run ID is {0}\n'.format(run_id))
            log_file.write('Best fitness is {0}\n'.format(
                self.halloffame[0].fitness))
            log_file.write(
                'Parameters of best model are {0}\n'.format(model_params))
            log_file.write(
                'Best individual is {0}\n'.format(self.halloffame[0]))
            for i, entry in enumerate(self.halloffame[0]):
                if entry > 0.95:
                    log_file.write(
                        "Warning! Parameter {0} is at or near maximum allowed "
                        "value\n".format(i + 1))
                elif entry < -0.95:
                    log_file.write(
                        "Warning! Parameter {0} is at or near minimum allowed "
                        "value\n".format(i + 1))
            log_file.write('Minimization history: \n{0}'.format(self.logbook))
        with open('{0}/{1}_opt_best_model.pdb'.format(
                output_path, run_id), 'w') as output_file:
            output_file.write(self.best_model.pdb)
        return

    @property
    def best_model(self):
        """Rebuilds the top scoring model from an optimisation.

        Returns
        -------
        model: AMPAL
            Returns an AMPAL model of the top scoring parameters.

        Raises
        ------
        NameError:
            Raises a name error if the optimiser has not been run.
        """
        if not hasattr(self, 'halloffame'):
            raise NameError('No best model found, have you ran the optimiser?')
        model = self.build_fn(*self.parse_individual(self.halloffame[0]))
        model.pack_new_sequences(self._params['sequence'])
        return model

    def make_energy_funnel_data(self, cores=1):
        """Compares models created during the minimisation to the best model.

        Returns
        -------
        energy_rmsd_gen: [(float, float, int)]
            A list of triples containing the BUFF score, RMSD to the
            top model and generation of a model generated during the
            minimisation.
        """
        if not self.parameter_log:
            raise AttributeError(
                'No parameter log data to make funnel, have you ran the '
                'optimiser?')
        model_cls = self._params['specification']
        gen_tagged = []
        for gen, models in enumerate(self.parameter_log):
            for model in models:
                gen_tagged.append((model[0], model[1], gen))
        sorted_pps = sorted(gen_tagged, key=lambda x: x[1])
        top_result = sorted_pps[0]
        top_result_model = model_cls(*top_result[0])
        if (cores == 1) or (sys.platform == 'win32'):
            energy_rmsd_gen = map(
                self.funnel_rebuild,
                [(x, top_result_model,
                  self._params['specification']) for x in sorted_pps[1:]])
        else:
            with futures.ProcessPoolExecutor(
                    max_workers=self._params['processors']) as executor:
                energy_rmsd_gen = executor.map(
                    self.funnel_rebuild,
                    [(x, top_result_model, self._params['specification'])
                     for x in sorted_pps[1:]])
        return list(energy_rmsd_gen)

    @staticmethod
    def funnel_rebuild(psg_trm_spec):
        """Rebuilds a model and compares it to a reference model.

        Parameters
        ----------
        psg_trm: (([float], float, int), AMPAL, specification)
            A tuple containing the parameters, score and generation for a
            model as well as a model of the best scoring parameters.

        Returns
        -------
        energy_rmsd_gen: (float, float, int)
            A triple containing the BUFF score, RMSD to the top model
            and generation of a model generated during the minimisation.
        """
        param_score_gen, top_result_model, specification = psg_trm_spec
        params, score, gen = param_score_gen
        model = specification(*params)
        rmsd = top_result_model.rmsd(model)
        return rmsd, score, gen


__author__ = 'Andrew R. Thomson, Christopher W. Wood, Gail J. Bartlett'
