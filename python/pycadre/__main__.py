from pycadre import cadre_model
import pycadre.load_params
from mpi4py import MPI
from repast4py import parameters, random
import time


def main():
    parser = parameters.create_args_parser()
    args = parser.parse_args()

    params_list = pycadre.load_params.load_params(args.parameters_file, args.parameters)
    
    # Set seed from params, but before derived params are evaluated.
    if 'random.seed' in params_list:
        random.init(int(params_list['random.seed']))
    else:
        # repast4py should do this when random is imported
        # but for now do it explicitly here
        random.init(int(time.time()))

    model = cadre_model.Model(params=params_list, comm=MPI.COMM_WORLD)
    # model.run(params=params_list)
    model.start()


if __name__ == "__main__":
    tic = time.perf_counter()
    main()
    toc = time.perf_counter()
    print(f"Model ran in  {toc-tic:0.2f} seconds")
