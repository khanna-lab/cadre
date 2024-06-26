from pycadre import cadre_model
import pycadre.load_params
from mpi4py import MPI
from repast4py import parameters, random
import time


def main(comm, parameters_file, parameters):
    # parser = parameters.create_args_parser()
    # args = parser.parse_args()

    params_list = pycadre.load_params.load_params(parameters_file, parameters)

    # Set seed from params
    if "BASE_SEED" in params_list:
        seed = int(params_list["BASE_SEED"])
        random.init(seed)
    else:
        # repast4py should do this when random is imported
        # but for now do it explicitly here
        seed = int(time.time())
        random.init(seed)

    print("Random seed:", seed)
    rng = random.default_rng
    print("RNG: ", rng)
    print("RNG type:", type(rng))

    model = cadre_model.Model(params=params_list, comm=comm)
    # model.run(params=params_list)
    model.start()


if __name__ == "__main__":
    tic = time.perf_counter()
    parser = parameters.create_args_parser()
    args = parser.parse_args()
    main(MPI.COMM_WORLD, args.parameters_file, args.parameters)
    toc = time.perf_counter()
    print(f"Model ran in  {toc-tic:0.2f} seconds")
