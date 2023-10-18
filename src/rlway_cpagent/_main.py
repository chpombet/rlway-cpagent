""" Main launching functions and mechanisms
"""


from rlway_cpagent.utils.utils import greet


def main():
    """
    rlway_cpagent main launch function used as an entry point
    """

    msg_l: str = greet("Eurodecision")
    print(msg_l)
