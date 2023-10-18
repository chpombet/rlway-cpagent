""" Main launching functions and mechanisms
"""

from rlway.pyosrd.osrd import OSRD

from rlway_cpagent.cp_agent import CPAgent


def main():
    """
    rlway_cpagent main launch function used as an entry point
    """
    sim = OSRD(use_case='c2y13s', dir='tmp')
    agent = CPAgent("cp_agent", "/mnt/c/Program Files/MiniZinc/minizinc.exe", "gecode")
    agent.stops(sim)
