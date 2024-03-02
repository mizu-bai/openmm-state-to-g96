from dataclasses import dataclass
from typing import Tuple
from xml.dom import minidom

import numpy as np


@dataclass
class StateMol:
    timestep: Tuple[int, float]
    position: np.array
    velocity: np.array
    box_vectors: np.array

    @staticmethod
    def from_file(
        file: str
    ) -> "StateMol":
        dom_tree = minidom.parse(file)

        # parse timestep
        time_count = dom_tree.documentElement.getAttribute("stepCount")
        time_count = int(time_count)

        time = dom_tree.documentElement.getAttribute("time")
        time = float(time)

        # parse box vector
        box_vectors = []

        box_vec_elem = dom_tree.documentElement.getElementsByTagName(
            "PeriodicBoxVectors")[0]

        for (dim_idx, dim) in enumerate(["A", "B", "C"]):
            dim_elem = box_vec_elem.getElementsByTagName(dim)[0]
            box_vectors.append(
                float(dim_elem.getAttribute(["x", "y", "z"][dim_idx]))
            )

        box_vectors = np.array(box_vectors)

        # parse position
        position = []
        pos_elem_list = dom_tree.documentElement.getElementsByTagName(
            "Positions")[0].getElementsByTagName("Position")

        for pos_elem in pos_elem_list:
            pos = []
            for axis in ["x", "y", "z"]:
                pos.append(float(pos_elem.getAttribute(axis)))

            position.append(pos)

        position = np.array(position)

        # parse velocity
        velocity = []
        vel_elem_list = dom_tree.documentElement.getElementsByTagName(
            "Velocities")[0].getElementsByTagName("Velocity")

        for vel_elem in vel_elem_list:
            vel = []
            for axis in ["x", "y", "z"]:
                vel.append(float(vel_elem.getAttribute(axis)))

            velocity.append(vel)

        velocity = np.array(velocity)

        state = StateMol(
            timestep=[time_count, time],
            position=position,
            velocity=velocity,
            box_vectors=box_vectors,
        )

        return state
