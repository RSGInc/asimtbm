import os
import pandas as pd

from activitysim.core import tracing
from activitysim.core import inject
from activitysim.core import pipeline

from activitysim.core.config import setting


def setup_working_dir():

    example_dir = os.path.join(os.path.dirname(__file__), os.pardir)
    os.chdir(example_dir)

    tracing.delete_output_files('csv')
    tracing.delete_output_files('txt')
    tracing.delete_output_files('log')
    tracing.delete_output_files('h5')


def test_example():

    setup_working_dir()

    # importing asimtbm also registers injectibles
    import asimtbm

    trace_od = inject.get_injectable('trace_od')
    assert trace_od == {'o': 3, 'd': 32}

    asimtbm.config_logger()

    output_files = os.listdir(os.path.join(os.getcwd(), 'output')).remove('.gitignore')
    assert not output_files

    models = setting('models')
    expected_models = [
        'destination_choice',
        'write_data_dictionary',
        'write_tables',
    ]
    assert models == expected_models

    pipeline.run(models)

    # tables will no longer be available after pipeline is closed
    pipeline.close_pipeline()

    output_files = os.listdir(os.path.join(os.getcwd(), 'output'))
    final_output_files = [
        'final_od_table.csv',
        'final_trips.csv',
        'final_zone_summary.csv',
    ]
    trace_output_files = [
        'trace.segment_od_hbwh.csv',
        'trace.segment_od_hbwl.csv',
        'trace.segment_od_hbwm.csv',
    ]
    other_output_files = [
        'asimtbm.log',
        'data_dict.txt',
        'pipeline.h5',
    ]

    for file in final_output_files + trace_output_files + other_output_files:
        assert file in output_files

    expected_trace_header = [
        'orig', 'dest', 'impedance', 'dest_park_cost', 'size',
        'no_size', 'utils', 'sum_utils', 'probs',
    ]
    for file in trace_output_files:
        trace_df = pd.read_csv(os.path.join(os.getcwd(), 'output', file))
        assert trace_df.shape == (1, len(expected_trace_header))
        assert sorted(trace_df.columns.values) == sorted(expected_trace_header)
        assert trace_df.orig[0] == trace_od['o']
        assert trace_df.dest[0] == trace_od['d']
