from typing import List, Callable, Iterable
from inspect import isgenerator
from dataclasses import dataclass

import numpy as np

from problems import definitions


@dataclass
class StateTransition:
    """
    Holds two states to define a new type with named parameters (old and new state) to be semantically acessed
    """

    old_state: definitions.ProblemDefinition.state
    new_state: definitions.ProblemDefinition.state


class LambdaWeights:
    """
    Encapsulates lambda configuration to be used to update heuristic success.

    The success s(h) of h is initialized with zero at the beginning of
    the period of p_u iterations. After using h in an iteration, s(h) is increased by δi
    if the resulting solution is of the corresponding quality:
    δ1 The new solution is the best one found so far.
    δ2 The new solution improves the current solution.
    δ3 The new solution does not improve the current solution, but is accepted.
    """
    def __init__(
        self,
        accepted_state_weight: float,
        improved_state_weight: float,
        best_state_weight: float,
    ):
        if accepted_state_weight > improved_state_weight or improved_state_weight > best_state_weight:
            raise ValueError(
                "Arguments should be so that accepted_state_weight < improved_state_weight < best_state_weight"
            )
        self.accepted_state_weight = accepted_state_weight
        self.improved_state_weight = improved_state_weight
        self.best_state_weight = best_state_weight


class ALNSProbParameters:
    """
    Encapsulates probabilities attributes of ALNS metaheuristic
    """
    def __init__(
        self,
        lambda_weights: LambdaWeights,
        rho: float,
        destroy_heuristics_len: int,
        repair_heuristics_len: int,
    ) -> None:
        self.lambda_weights = lambda_weights
        self.rho = rho

        self.destroy_prob = np.ones(destroy_heuristics_len) / destroy_heuristics_len
        self.repair_prob = np.ones(repair_heuristics_len) / repair_heuristics_len

        self.destroy_heuristics_sucess = np.zeros(destroy_heuristics_len)
        self.repair_heuristics_sucess = np.zeros(repair_heuristics_len)
        
        self.times_used_destroy_heuristics = np.zeros(destroy_heuristics_len)
        self.times_used_repair_heuristics = np.zeros(repair_heuristics_len)


class ALNSIter:
    """
    Implements destroy and repair methods to be used on ALNS.
    """

    def __init__(
        self,
        destroy_heuristics: Iterable[Callable[[float, definitions.ProblemDefinition.state], definitions.ProblemDefinition.state]],
        repair_heuristics: Iterable[Callable[[definitions.ProblemDefinition.state], definitions.ProblemDefinition.state]],
        scoring_function: Callable[[definitions.ProblemDefinition.state], float],
        acceptance_function: Callable[[StateTransition], bool],
        prob_parameters: ALNSProbParameters,
    ):
        if not destroy_heuristics or not repair_heuristics:
            raise ValueError("Needs to have at least one destroy and one repair heuristic defined")
        if isgenerator(destroy_heuristics) or isgenerator(repair_heuristics):
            raise ValueError("Can't use a generator since heuristics will be itered upon multiple times")

        self.destroy_heuristics = destroy_heuristics
        self.repair_heuristics = repair_heuristics
        self.scoring_function = scoring_function
        self.acceptance_function = acceptance_function
        self.best_state = None
        self.current_state = None
        self.prob_parameters = prob_parameters

    def _destroy(self, destruction_parameter: float, state: definitions.ProblemDefinition.state) -> definitions.ProblemDefinition.state:
        """
        Selects a destroy heuristic at random, use it to deconstruct given state
        and returns an incomplete state
        """
        dh_func_idx = np.random.choice(len(self.destroy_heuristics), p=self.prob_parameters.destroy_prob)
        dh_func = self.destroy_heuristics[dh_func_idx]
        incomplete_state = dh_func(destruction_parameter, state)
        return incomplete_state, dh_func_idx

    def _repair(self, state: definitions.ProblemDefinition.state) -> definitions.ProblemDefinition.state:
        """
        Selects a repair heuristic at random, use it to reconstruct an incomplete
        state and returns the new state
        """
        rh_func_idx = np.random.choice(len(self.destroy_heuristics), p=self.prob_parameters.destroy_prob)
        rh_func = self.repair_heuristics[rh_func_idx]
        new_state = rh_func(state)
        return new_state, rh_func_idx

    def update_heuristics_probabilities(self, prob_parameters: ALNSProbParameters):
        """
        Updates all heuristics probabilities. Can be called upon after any amount of iteractions.
        """
        destroy_used_more_than_zero_mask = prob_parameters.times_used_destroy_heuristics != 0
        repair_used_more_than_zero_mask = prob_parameters.times_used_repair_heuristics != 0

        # formula to calc new probability of used heuristics
        def calc_new_prob(rho, heuristics_prob, heuristics_success, times_used):
            new_heuristics_prob = 1 - rho * heuristics_prob + rho * heuristics_success / times_used
            return new_heuristics_prob

        # updating used heuristics probabilities
        prob_parameters.destroy_prob[destroy_used_more_than_zero_mask] = calc_new_prob(
            prob_parameters.rho,
            prob_parameters.destroy_prob[destroy_used_more_than_zero_mask],
            prob_parameters.destroy_heuristics_sucess[destroy_used_more_than_zero_mask],
            prob_parameters.times_used_destroy_heuristics[destroy_used_more_than_zero_mask],
        )
        prob_parameters.repair_prob[repair_used_more_than_zero_mask] = calc_new_prob(
            prob_parameters.rho,
            prob_parameters.repair_prob[repair_used_more_than_zero_mask],
            prob_parameters.repair_heuristics_sucess[repair_used_more_than_zero_mask],
            prob_parameters.times_used_repair_heuristics[repair_used_more_than_zero_mask],
        )

        # updating unused heuristics probabilities
        unused_destroy_mask = np.logical_not(destroy_used_more_than_zero_mask)
        prob_parameters.destroy_prob[unused_destroy_mask] = (
            1 - prob_parameters.rho * prob_parameters.destroy_prob[unused_destroy_mask]
        )
        unused_repair_mask = np.logical_not(repair_used_more_than_zero_mask)
        prob_parameters.repair_prob[unused_repair_mask] = (
            1 - prob_parameters.rho * prob_parameters.repair_prob[unused_repair_mask]
        )

    def do_alns_iteraction(self, destruction_parameter: float, state: definitions.ProblemDefinition.state) -> definitions.ProblemDefinition.state:
        """
        Do one iteraction of ALNS with destroy and repair heuristics given to class object. Returns new state.
        """
        incomplete_state, dh_idx = self._destroy(destruction_parameter, state)
        new_state, rh_idx = self._repair(incomplete_state)
        new_state_score = self.scoring_function(new_state)
        isaccepted = self.acceptance_function(StateTransition(self.current_state, new_state))
        success_increment = 0
        if isaccepted:
            self.current_state = new_state
            success_increment = self.prob_parameters.lambda_weights.accepted_state_weight

        if new_state_score < self.scoring_function(self.current_state):
            success_increment = self.prob_parameters.lambda_weights.improved_state_weight

        if new_state_score < self.scoring_function(self.best_state):
            self.best_state = new_state
            success_increment = self.prob_parameters.lambda_weights.best_state_weight

        self.prob_parameters.destroy_heuristics_sucess[dh_idx] += success_increment
        self.prob_parameters.times_used_destroy_heuristics[dh_idx] += 1
        self.prob_parameters.repair_heuristics_sucess[rh_idx] += success_increment
        self.prob_parameters.times_used_repair_heuristics[rh_idx] += 1
