from functools import partial

import pandas as pd

from .traverser import (yield_groups,
                        get_optima_path,
                        generate_results_path)
OPTIMUM_HEADER = ['instance', 'optimum']
HEADER = ['instance', 'max_iteration', 'neighbors', 'tabu_tenure', 'reinits',
          'time', 'value']
read_csv = partial(pd.read_csv, sep=' ', header=None)

def load_main_frame():
    frames = []
    for group in sorted(yield_groups()):
        optima = read_csv(get_optima_path(group)).rename(
            dict(enumerate(OPTIMUM_HEADER)), axis=1)[OPTIMUM_HEADER]

        measurements = read_csv(generate_results_path(group)).rename(
            dict(enumerate(HEADER)), axis=1)[HEADER]

        frame = optima.merge(measurements, how='inner', on='instance')
        frame['group'] = group
        frame = frame[[frame.columns[-1], *frame.columns[:-1]]]
        frames.append(frame)
    frame = pd.concat(frames, ignore_index=True)
    frame['relative_error'] = (frame.optimum - frame.value) / frame.optimum 
    return frame

frame = load_main_frame()

index_20 = frame[frame.group.str.contains('20-')].index
index_50 = frame[frame.group.str.contains('50-')].index