from typing import Any, Dict, List
from dataclasses import dataclass

from pkg_resources import resource_filename
import numpy as np
from datetime import timedelta

from minizinc import Model, Solver, Instance

from rlway.pyosrd.osrd import OSRD
from rlway.schedules import Schedule, schedule_from_osrd
from rlway.pyosrd.agents import Agent

@dataclass
class CPAgent(Agent):

    solver_name:str

    def stops(self, osrd: OSRD) -> List[Dict[str, Any]]:
        return self.solveCpProblem(osrd)

    def solveCpProblem(self, osrd:OSRD):
        model = Model(resource_filename("rlway_cpagent.models", "zone_model.mzn"))
        solver = Solver.lookup(self.solver_name)
        instance = Instance(solver, model)

        self.load_data(instance, osrd)
        result = instance.solve(timeout=timedelta(seconds=30))
        return self.get_stops(result, osrd)

    def load_data(self, instance:Instance, osrd:OSRD):
        ref_schedule = schedule_from_osrd(osrd)
        delayed_schedule = schedule_from_osrd(self.delayed)

        zones = ref_schedule.blocks
        trains = ref_schedule.trains

        starts = ref_schedule.starts
        ends = ref_schedule.ends
        
        delayed_durations = delayed_schedule.durations

        instance["Z"] = len(zones)
        instance["T"] = len(trains)
        instance["S"] = sum([len(ref_schedule.trajectory(trainIdx)) for trainIdx in range(len(trains))])

        train_association = []
        zone_association = []
        prev_step_association = []
        min_arrival = []
        min_departure = []
        min_duration = []
        is_fixed = []

        for trainIdx in range(len(trains)):
            prev_step = 0
            for zone in ref_schedule.trajectory(trainIdx):
                train_association.append(trainIdx + 1)
                zone_association.append(zones.index(zone) + 1)
                prev_step_association.append(prev_step)
                min_arrival.append(int(starts.loc[zone][trainIdx]))
                min_departure.append(int(ends.loc[zone][trainIdx]))
                min_duration.append(int(delayed_durations.loc[zone][trainIdx]))
                is_fixed.append(True if osrd.stop_positions[trainIdx][zone]['offset'] is None else False)

                prev_step = len(train_association)

        instance["train"] = train_association
        instance["zone"] = zone_association
        instance["prev"] = prev_step_association
        instance["min_arrival"] = min_arrival
        instance["min_departure"] = min_departure
        instance["min_duration"] = min_duration
        instance["is_fixed"] = is_fixed
        
        print(f"Z = {len(zones)};")
        print(f"T = {len(trains)};")
        print(f"S = {len(train_association)};")
        print(f"train = {train_association};")
        print(f"zone = {zone_association};")
        print(f"prev = {prev_step_association};")
        print(f"min_duration = {min_duration};")
        print(f"min_arrival = {min_arrival};")
        print(f"min_departure = {min_departure};")
        
    def get_stops(self, result, osrd:OSRD) -> List[Dict[str, Any]]:
        stops = []
        print(result)
        delayed_schedule = schedule_from_osrd(self.delayed)
        zones = delayed_schedule.blocks
        trains = delayed_schedule.trains
        durations = delayed_schedule.durations
        
        new_durations = list(np.array(result['d']) - np.array(result['a']))
        
        step_idx = 0
        for trainIdx in range(len(trains)):
            for zone in delayed_schedule.trajectory(trainIdx):
                delay =  int(new_durations[step_idx]) - int(durations.loc[zone][trainIdx])
                if delay > 0:
                    delayed_schedule = delayed_schedule.add_delay(trainIdx, zone, delay)
                    stops.append({
                        "train" : trainIdx,
                        "position" : osrd.stop_positions[trainIdx][zone]['offset'],
                        "duration" : delay
                    })
                step_idx +=1
        print(f"stops : {stops}")
        delayed_schedule.plot()
        return stops
    
    def getZonePosition(self, osrd:OSRD, zone, train):
        points = osrd.points_encountered_by_train(train)
        if '<->' not in zone:
            position = next(point['offset'] for point in points if point['id'] == zone)
        else:
            pointStartId = zone.split('<->')[0]
            pointEndId = zone.split('<->')[1]
            position = max(
                next((point['offset'] for point in points if point['id'] == pointStartId), 0),
                next((point['offset'] for point in points if point['id'] == pointEndId), 0))
        
        return position
    
    def drawSchedule(self, delayed:Schedule, result):
        delayed.add_delay()
        