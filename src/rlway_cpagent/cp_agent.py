from typing import Any, Dict, List
from dataclasses import dataclass

from importlib.resources import path as resource_path

from minizinc import Model, Solver, Instance, Driver

from rlway.pyosrd.osrd import OSRD
from rlway.schedules import Schedule, schedule_from_osrd
from rlway.pyosrd.agents import Agent

@dataclass
class CPAgent(Agent):

    minizinc_path:str
    solver_name:str

    def stops(self, osrd:OSRD) -> List[Dict[str, Any]]:
        self.solveCpProblem(osrd)
        return []

    def solveCpProblem(self, osrd:OSRD):
        model = Model(resource_path("models", "zone_model.mzn"))
        solver = Solver.lookup(self.solver_name)
        instance = Instance(solver, model)

        self.load_data(instance, osrd)
        result = instance.solve()
        print(result)

    def load_data(self, instance:Instance, osrd:OSRD):
        schedule = schedule_from_osrd(osrd)

        zones = schedule.blocks
        trains = schedule.trains

        starts = schedule.starts
        ends = schedule.ends

        instance["Z"] = len(zones)
        instance["T"] = len(trains)
        instance["S"] = sum([len(schedule.trajectory(trainIdx)) for trainIdx in range(len(trains))])

        train_association = []
        zone_association = []
        prev_step_association = []
        min_arrival = []
        min_departure = []
        min_duration = []

        for trainIdx in range(len(trains)):
            prev_step = 0
            for zone in schedule.trajectory(trainIdx):
                train_association.append(trainIdx + 1)
                zone_association.append(zones.index(zone) + 1)
                prev_step_association.append(prev_step)
                min_arrival.append(int(starts.loc[zone][trainIdx]))
                min_departure.append(int(ends.loc[zone][trainIdx]))
                min_duration.append(min_departure[-1] - min_arrival[-1])

                prev_step = len(train_association)

        instance["train"] = train_association
        instance["zone"] = zone_association
        instance["prev"] = prev_step_association
        instance["min_arrival"] = min_arrival
        instance["min_departure"] = min_departure
        instance["min_duration"] = min_duration