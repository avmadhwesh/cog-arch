import sys

import json
import uuid
import math
from typing import List, Dict, Optional
from itertools import chain
import datetime
from copy import deepcopy
import os
from os import path
import subprocess
import random

import cairo
sys.path.append("build")
import py_random_points

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 800
OUTPUT_DIR = "build/stimuli"

# number_of_points: mean, sd
# simulation details: stimuli_maker.py commit: e61a2c633ed8c1476ec02df29b74c014980ea3da
# 100000 stims per number of points
# These are the means and sds when grouped by number of points.
# Generate this using stimuli_analysis.py and get these values using
# stimuli_analysis.R
STD_VZ_TABLE = {
    10: (1.25,  1.03),
    15: (1.03,  1.00),
    20: (0.924, 0.992),
    25: (0.873, 0.979),
    30: (0.864, 0.971),
    35: (0.867, 0.962),
    40: (0.880, 0.952),
    45: (0.907, 0.948),
    50: (0.945, 0.940),
    55: (0.979, 0.935),
    60: (1.03,  0.927),
    65: (1.08,  0.917),
    70: (1.14,  0.915),
    75: (1.20,  0.915),
    80: (1.26,  0.909),
    85: (1.32,  0.910),
    90: (1.39,  0.901),
    95: (1.46,  0.893),
    100: (1.55,  0.897),
}

class Stimulus:
    def __init__(self, number_of_points, output):
        self.base_uuid: str = output["base_uuid"]
        self.unique_uuid: str = str(uuid.uuid4())
        self.number_of_points: int = number_of_points
        self.z_score: float = output["z_score"]
        self.vacuumed_z_score: float = output["vacuumed_z_score"]
        self.std_vaccumed_z_score: float = std_vz_score(
            number_of_points, self.vacuumed_z_score
        )
        self.points: List[Dict[str, int]] = output["points"]
        self.flipped: bool = False
        self.group: Optional[str] = None
        self.practice_stimulus = False

    def to_dict(self):
        return {
            "base_uuid": self.base_uuid,
            "unique_uuid": self.unique_uuid,
            "number_of_points": self.number_of_points,
            "z_score": self.z_score,
            "vacuumed_z_score": self.vacuumed_z_score,
            "std_vaccumed_z_score": self.std_vaccumed_z_score,
            "flipped": self.flipped,
            "group": self.group,
            "points": self.points,
            "practice_stimulus": self.practice_stimulus
        }

    def __repr__(self):
        return f"<Stimulus n={self.number_of_points}>"

    def flip(self):
        new_stimulus = deepcopy(self)
        new_stimulus.unique_uuid = str(uuid.uuid4())
        new_stimulus.flipped = True
        for point in new_stimulus.points:
            point["x"] = CANVAS_WIDTH - point["x"]
            point["y"] = CANVAS_HEIGHT - point["y"]
        return new_stimulus

    def save_to_png(self, path):
        with cairo.ImageSurface(
            cairo.FORMAT_ARGB32, CANVAS_WIDTH, CANVAS_HEIGHT
        ) as surface:
            ctx = cairo.Context(surface)
            ctx.set_source_rgb(1, 1, 1)
            ctx.rectangle(0, 0, 800, 500)
            ctx.fill()
            ctx.set_source_rgb(0, 0, 0)
            for point in self.points:
                ctx.arc(point["x"], point["y"], 5, 0, math.pi * 2)
                ctx.fill()
            surface.write_to_png(path)

    @classmethod
    def generate(cls, number_of_points):
        return cls(number_of_points, py_random_points.make_points(number_of_points))


def std_vz_score(number_of_points, vzscore):
    mean, sd = STD_VZ_TABLE[number_of_points]
    return (vzscore - mean) / sd


def random_half_split(input_list):
    length = len(input_list)
    assert length % 2 == 0, "List not even"
    list_ = deepcopy(input_list)
    random.shuffle(list_)
    return (list_[0 : length // 2], list_[length // 2 :])


NUM_PER_GROUP = 3


GROUPS = [
    dict(name="disperse", range=(0.95, 1.05), stimuli=[]),
    dict(name="clustered", range=(-2.05, -1.95), stimuli=[]),
    dict(name="very_clustered", range=(-3.55, -3.45), stimuli=[])
]


def main():
    # unique_uuid: Stimulus
    stimuli: Dict[str, Stimulus] = {}
    # unique_uuid: info_dict
    stimuli_info: dict = {}
    
    for number_of_points in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100):
        print(number_of_points)
        for group in GROUPS:
            name = group['name']
            low, high = group['range']
            group_array = group['stimuli']
            stimuli_for_n_points = []
            while len(stimuli_for_n_points) < NUM_PER_GROUP:
                stimulus = Stimulus.generate(number_of_points)
                if low < stimulus.std_vaccumed_z_score < high:
                    stimulus.group = name                    
                    stimuli_for_n_points.append(stimulus)
            group_array.extend(stimuli_for_n_points)

                    
    for group in GROUPS:
        for stimulus in group['stimuli']:
            stimuli_info[stimulus.unique_uuid] = deepcopy(stimulus.to_dict())
            stimuli[stimulus.unique_uuid] = stimulus


    experimental_unique_uuids = []
    for group in GROUPS:
        for stimulus in group['stimuli']:
            experimental_unique_uuids.append(stimulus.unique_uuid)

    random.shuffle(experimental_unique_uuids)
        
    # Practice stimuli

    practice_stimuli = [Stimulus.generate(n) for n in (10, 15, 25)]
    for stim in practice_stimuli:
        stim.practice_stimulus = True
        stimulus_info = deepcopy(stim.to_dict())
        stimuli[stim.unique_uuid] = stim
        stimuli_info[stim.unique_uuid] = stimulus_info

    # Outputting the files
    os.mkdir(OUTPUT_DIR)
    with open(
        path.join(OUTPUT_DIR, "stimuli_info.json"), "w"
    ) as f:  # pylint: disable=invalid-name
        json.dump(stimuli_info, f)

    with open(
        path.join(OUTPUT_DIR, "experimental_unique_uuids.json"), "w"
    ) as f:  # pylint: disable=invalid-name
        json.dump(experimental_unique_uuids, f)

    with open(
        path.join(OUTPUT_DIR, "practice_uuids.json"), "w"
    ) as f:
        json.dump([s.unique_uuid for s in practice_stimuli], f)

    with open(
        path.join(OUTPUT_DIR, "generation_info.json"), "w"
    ) as f:  # pylint: disable=invalid-name
        json.dump(
            {
                "generation_time": datetime.datetime.now().isoformat(),
                "generation_code_commit_hash": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"]
                )
                .decode()
                .strip(),
            },
            f,
        )

    stimuli_json_dir = path.join(OUTPUT_DIR, "stimuli_json")
    os.mkdir(stimuli_json_dir)
    for unique_uuid, stimulus in stimuli.items():
        with open(
            path.join(stimuli_json_dir, unique_uuid + ".json"), "w"
        ) as f:  # pylint: disable=invalid-name
            json.dump(stimulus.to_dict(), f)

    stimuli_images_dir = path.join(OUTPUT_DIR, "stimuli_images")
    os.mkdir(stimuli_images_dir)
    for unique_uuid, stimulus in stimuli.items():
        filepath = path.join(stimuli_images_dir, unique_uuid + ".png")
        stimulus.save_to_png(filepath)

if __name__ == "__main__":
    main()
