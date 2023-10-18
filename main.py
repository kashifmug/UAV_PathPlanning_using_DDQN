import argparse
import os

from src.CPP.Environment import CPPEnvironmentParams, CPPEnvironment


from utils import *


def main_cpp(p):
    env = CPPEnvironment(p)

    env.run()




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', action='store_true', help='Activates usage of GPU')
    parser.add_argument('--generate_config', action='store_true', help='Enable to write default config only')
    parser.add_argument('--config', default=None, help='Path to config file')
    parser.add_argument('--id', default=None, help='If set overrides the logfile name and the save name')

    parser.add_argument('--params', nargs='*', default=None)

    parser.add_argument('--cpp', action='store_true', help='Run Coverage Path Planning')


    args = parser.parse_args()

    if args.generate_config:
        if args.cpp:
            generate_config(CPPEnvironmentParams(), "config/cpp.json")
        else:
            print("Specify which config to generate")
        exit(0)

    if args.config is None:
        print("Config file needed!")
        exit(1)

    if not args.gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    params = read_config(args.config)

    if args.params is not None:
        params = override_params(params, args.params)

    if args.id is not None:
        params.model_stats_params.save_model = "models/" + args.id
        params.model_stats_params.log_file_name = args.id

    if args.cpp:
        main_cpp(params)

