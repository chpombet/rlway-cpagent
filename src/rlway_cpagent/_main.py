""" Main launching functions and mechanisms
"""

from rlway.pyosrd.osrd import OSRD

from rlway_cpagent.cp_agent import CPAgent
from rlway.schedules import Schedule, schedule_from_osrd

import matplotlib.pyplot as plt


def main():
    """
    rlway_cpagent main launch function used as an entry point
    """
    sim = OSRD(use_case='station_capacity2', dir='tmp')
    sim.reset_delays()
    sim.add_delay('train0', time_threshold=150, delay=800.)
    regulated = sim.regulate(agent=CPAgent("cp_agent", "gecode"))
    ref_schedule = schedule_from_osrd(sim)
    delayed_schedule = schedule_from_osrd(sim.delayed())
    regulated_schedule = schedule_from_osrd(regulated)
    
    ref_schedule.plot()
    delayed_schedule.plot()
    regulated_schedule.plot()
