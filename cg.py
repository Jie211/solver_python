import logging

import numpy as np
from numpy.linalg import norm
from numba import jit, types
from scipy.sparse import csr_matrix

from helper import get_logger, norm2, dot_mat, dot_vec, norm2_numba, dot_vec_numba, dot_mat_numba

logger = get_logger(__name__)


def cg_method_basic(a_mat, b_vec, max_iter=10000, epsilon=1e-10, logger_level=logging.INFO):
    # init
    x_vec = np.zeros(b_vec.shape)
    b_norm = norm2(b_vec)
    is_converged = False
    k = 0
    residual = []
    step = max_iter / 10
    logger.setLevel(logger_level)
    logger.debug("start")

    # r_0 = b - Ax_0
    r_vec = b_vec - dot_mat(a_mat, x_vec)
    # p_0 = r_0
    p_vec = r_vec.copy()
    # for k = 0, 1, 2, ...
    while k < max_iter:
        r_vec_old = r_vec
        # alpha_k = r_k * r_k / p_k * (A * p_k)
        alpha = dot_vec(r_vec_old, r_vec_old) / dot_vec(p_vec, dot_mat(a_mat, p_vec))
        # x_k+1 = x_k + alpha_k * p_k
        x_vec = x_vec + alpha * p_vec
        # r_k+1 = r_k - alpha_k * A * p_k
        r_vec = r_vec_old - alpha * dot_mat(a_mat, p_vec)
        # beta_k = r_k+1 * r_k+1 / r_k * r_k
        beta = dot_vec(r_vec, r_vec) / dot_vec(r_vec_old, r_vec_old)
        # p_k+1 = r_k+1 + beta_k * p_k
        p_vec = r_vec + beta * p_vec

        # until ||r_k||_2 / ||b||_2 < epsilon
        res = norm2(r_vec) / b_norm
        residual.append(res)
        if k % step == 0:
            logger.debug("k = %d, res = %e", k, res)

        if res <= epsilon:
            is_converged = True
            break
        k += 1
    logger.debug("done")
    return is_converged, residual, k


def cg_method_numba(a_mat, b_vec, max_iter=10000, epsilon=1e-10, logger_level=logging.INFO):
    # init
    x_vec = np.zeros(b_vec.shape)
    b_norm = norm2_numba(b_vec)
    is_converged = False
    k = 0
    residual = []
    step = max_iter / 10
    logger.setLevel(logger_level)
    logger.debug("start")

    # r_0 = b - Ax_0
    r_vec = b_vec - dot_mat_numba(a_mat.indptr, a_mat.indices, a_mat.data, x_vec)
    # p_0 = r_0
    p_vec = r_vec.copy()
    # for k = 0, 1, 2, ...
    while k < max_iter:
        r_vec_old = r_vec
        # alpha_k = r_k * r_k / p_k * (A * p_k)
        alpha = dot_vec_numba(r_vec_old, r_vec_old) / dot_vec_numba(p_vec, dot_mat_numba(a_mat.indptr, a_mat.indices, a_mat.data, p_vec))
        # x_k+1 = x_k + alpha_k * p_k
        x_vec = x_vec + alpha * p_vec
        # r_k+1 = r_k - alpha_k * A * p_k
        r_vec = r_vec_old - alpha * dot_mat_numba(a_mat.indptr, a_mat.indices, a_mat.data, p_vec)
        # beta_k = r_k+1 * r_k+1 / r_k * r_k
        beta = dot_vec_numba(r_vec, r_vec) / dot_vec_numba(r_vec_old, r_vec_old)
        # p_k+1 = r_k+1 + beta_k * p_k
        p_vec = r_vec + beta * p_vec

        # until ||r_k||_2 / ||b||_2 < epsilon
        res = norm2_numba(r_vec) / b_norm
        residual.append(res)
        if k % step == 0:
            logger.debug("k = %d, res = %e", k, res)

        if res <= epsilon:
            is_converged = True
            break
        k += 1
    logger.debug("done")
    return is_converged, residual, k

def cg_method_numpy(a_mat, b_vec, max_iter=10000, epsilon=1e-10, logger_level=logging.INFO):
    # init
    x_vec = np.zeros(b_vec.shape)
    b_norm = norm(b_vec, ord=2)
    is_converged = False
    k = 0
    residual = []
    step = max_iter / 10
    logger.setLevel(logger_level)
    logger.debug("start")

    # r_0 = b - Ax_0
    r_vec = b_vec - a_mat.dot(x_vec)
    # p_0 = r_0
    p_vec = r_vec.copy()
    # for k = 0, 1, 2, ...
    while k < max_iter:
        r_vec_old = r_vec
        # alpha_k = r_k * r_k / p_k * (A * p_k)
        alpha = r_vec_old.dot(r_vec_old) / p_vec.dot(a_mat.dot(p_vec))
        # x_k+1 = x_k + alpha_k * p_k
        x_vec = x_vec + alpha * p_vec
        # r_k+1 = r_k - alpha_k * A * p_k
        r_vec = r_vec_old - alpha * a_mat.dot(p_vec)
        # beta_k = r_k+1 * r_k+1 / r_k * r_k
        beta = r_vec.dot(r_vec) / r_vec_old.dot(r_vec_old)
        # p_k+1 = r_k+1 + beta_k * p_k
        p_vec = r_vec + beta * p_vec

        # until ||r_k||_2 / ||b||_2 < epsilon
        res = norm(r_vec, ord=2) / b_norm
        residual.append(res)
        if k % step == 0:
            logger.debug("k = %d, res = %e", k, res)

        if res <= epsilon:
            is_converged = True
            break
        k += 1
    logger.debug("done")
    return is_converged, residual, k

# csr_matrix_type = types.Opaque('scipy.sparse.spmatrix')
# ndarray_type = types.float64[:]
# tuple_type = types.Tuple((types.boolean, ndarray_type, types.int64))
#
#
# @jit(tuple_type(csr_matrix_type, ndarray_type, types.int8, types.float64), nopython=True)
# def cg_method_numba(a_mat: csr_matrix, b_vec: np.ndarray, max_iter: int = 10000, epsilon: float = 1e-10) -> tuple[bool, np.ndarray, int]:
#     # init
#     x_vec = np.zeros(b_vec.shape)
#     # b_norm = norm(b_vec, ord=np.inf)
#     b_norm = norm(b_vec)
#     is_converged = False
#     k = 0
#     residual = []
#     step = max_iter / 10
#
#     # r_0 = b - Ax_0
#     r_vec = b_vec - a_mat.dot(x_vec)
#     # p_0 = r_0
#     p_vec = r_vec.copy()
#     # for k = 0, 1, 2, ...
#     while k < max_iter:
#         r_vec_old = r_vec
#         # alpha_k = r_k * r_k / p_k * (A * p_k)
#         alpha = r_vec_old.dot(r_vec_old) / p_vec.dot(a_mat.dot(p_vec))
#         # x_k+1 = x_k + alpha_k * p_k
#         x_vec = x_vec + alpha * p_vec
#         # r_k+1 = r_k - alpha_k * A * p_k
#         r_vec = r_vec_old - alpha * a_mat.dot(p_vec)
#         # beta_k = r_k+1 * r_k+1 / r_k * r_k
#         beta = r_vec.dot(r_vec) / r_vec_old.dot(r_vec_old)
#         # p_k+1 = r_k+1 + beta_k * p_k
#         p_vec = r_vec + beta * p_vec
#
#         # until ||r_k||_inf / ||b||_inf < epsilon
#         # res = norm(r_vec, ord=np.inf) / b_norm
#         res = norm(r_vec) / b_norm
#         residual.append(res)
#
#         if res <= epsilon:
#             is_converged = True
#             break
#         k += 1
#     return is_converged, residual, k
