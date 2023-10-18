import argparse
import os

import numpy as np

from src.CPP.Environment import CPPEnvironmentParams, CPPEnvironment

from utils import override_params, read_config

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import tensorflow as tf


def eval_logs(event_path):
    event_acc = EventAccumulator(event_path, size_guidance={'tensors': 100000})
    event_acc.Reload()

    _, _, vals = zip(*event_acc.Tensors('successful_landing'))
    has_landed = [tf.make_ndarray(val) for val in vals]

    _, _, vals = zip(*event_acc.Tensors('cr'))
    cr = [tf.make_ndarray(val) for val in vals]

    _, _, vals = zip(*event_acc.Tensors('cral'))
    cral = [tf.make_ndarray(val) for val in vals]

    _, _, vals = zip(*event_acc.Tensors('boundary_counter'))
    boundary_counter = [tf.make_ndarray(val) for val in vals]

    print("Successful Landing:", sum(has_landed) / len(has_landed))
    print("Collection ratio:", sum(cr) / len(cr))
    print("Collection ratio and landed:", sum(cral) / len(cral))




def cpp_mc(args, params: CPPEnvironmentParams):
    try:
        env = CPPEnvironment(params)
        env.agent.load_weights(args.weights)

        env.eval(int(args.samples), show=args.show)
    except AttributeError:
        print("Not overriding log dir, eval existing:")

    eval_logs("logs/training/" + args.id + "/test")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', required=True, help='Path to weights')
    parser.add_argument('--config', required=True, help='Config file for agent shaping')
    parser.add_argument('--id', required=False, help='Id for exported files')
    parser.add_argument('--samples', required=True, help='Id for exported files')
    parser.add_argument('--seed', default=None, help="Seed for repeatability")
    parser.add_argument('--show', default=False, help="Show individual plots, allows saving")
    parser.add_argument('--params', nargs='*', default=None)


    # CPP Params
    parser.add_argument('--cpp', action='store_true', help='Run Coverage Path Planning')

    args = parser.parse_args()

    if args.seed:
        np.random.seed(int(args.seed))

    params = read_config(args.config)

    if args.params is not None:
        params = override_params(params, args.params)

    if args.id is not None:
        params.model_stats_params.save_model = "models/" + args.id
        params.model_stats_params.log_file_name = args.id

    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    if args.cpp:
        cpp_mc(args, params)

