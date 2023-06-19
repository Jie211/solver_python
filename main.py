import argparse
import logging
import sys
import time

import numpy as np

from cg import cg_method_basic, cg_method_cupy, cg_method_numba, cg_method_numpy
from helper import create_fig, get_logger, load_sparse_csr, load_sparse_csr_cupy, save_fig

logger = get_logger("solver")
logger_level = logging.INFO


def main_handler(args: argparse.Namespace):
    mat_file = str(args.base_dir) + "/" + str(args.target_matrix) + ".npz"
    max_inter = args.iterate_max
    epsilon = args.epsilon
    use_numba = args.numba
    use_numpy = args.numpy
    fig_output_path = args.figure_output_path
    use_cupy = args.cupy
    figure = args.figure
    logger.info("mat_file: %s, max_inter: %d, epsilon: %e, numpy: %s, numba: %s, cupy: %s", mat_file, max_inter, epsilon,
                use_numpy, use_numba, use_cupy)

    if use_cupy:
        mat_csr, b_vec = load_sparse_csr_cupy(mat_file)
    else:
        mat_csr, b_vec = load_sparse_csr(mat_file)
    if args.conjugate_gradient_method:
        logger.info("CG method")
        time_start = time.perf_counter()
        if use_numpy:
            logger.info("use numpy")
            is_converged, residual, k = \
                cg_method_numpy(mat_csr, b_vec, max_iter=max_inter, epsilon=epsilon, logger_level=logger_level)
        elif use_numba:
            is_converged, residual, k = \
                cg_method_numba(mat_csr, b_vec, max_iter=max_inter, epsilon=epsilon, logger_level=logger_level)
        elif use_cupy:
            is_converged, residual, k = \
                cg_method_cupy(mat_csr, b_vec, max_iter=max_inter, epsilon=epsilon, logger_level=logger_level)
        else:
            is_converged, residual, k = \
                cg_method_basic(mat_csr, b_vec, max_iter=max_inter, epsilon=epsilon, logger_level=logger_level)
        time_end = time.perf_counter()
        time_elapsed = time_end - time_start
        logger.info("is_converged = %s, loop = %s, time = %d s", is_converged, k, time_elapsed)

        if figure:
            fig = create_fig(np.arange(1, k), residual, "CG Method/"+str(args.target_matrix),
                             "loop", "residual", epsilon=epsilon, plot_epsilon=True)
            save_fig(fig, str(fig_output_path) + "/"
                     + str(args.target_matrix) + "_" + str(max_inter) + "_" + str(epsilon) + "_cg.png")
            logger.info("save figure Done")

    return None


def main(argv=None):
    if argv is None:
        argv = []
    if 0 != len(argv):
        sys.argv = argv

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-cg", "--conjugate_gradient_method", action="store_true", help="CG method")
    parser.add_argument("-t", "--target_matrix", type=str, help="target matrix name")
    parser.add_argument("-b", "--base_dir", type=str, help="base directory", default="./matrix")
    parser.add_argument("-output", "--figure_output_path", type=str, help="figure output path", default="./figure")
    parser.add_argument("-imax", "--iterate_max", type=int, help="max iteration", default=10000)
    parser.add_argument("-e", "--epsilon", type=float, help="epsilon", default=1e-10)
    parser.add_argument("-np", "--numpy", action="store_true", help="use numpy", default=False)
    parser.add_argument("-nb", "--numba", action="store_true", help="use numba", default=False)
    parser.add_argument("-f", "--figure", action="store_true", help="create figure", default=False)
    parser.add_argument("-cp", "--cupy", action="store_true", help="use cupy", default=False)

    parser.set_defaults(handler=main_handler)
    args = parser.parse_args()
    logger.debug("args: %s", args)

    if args.verbose:
        global logger_level
        logger_level = logging.DEBUG
        logger.setLevel(logger_level)
    if args.target_matrix is None:
        parser.print_help()
        return None
    if args.figure:
        args.verbose = False

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()
        return None
    return None


if __name__ == "__main__":
    main(sys.argv)
