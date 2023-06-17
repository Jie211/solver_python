import logging

import numpy as np
import numba as nb
from scipy.sparse import csr_matrix
from rich.logging import RichHandler


@nb.njit(fastmath=True, parallel=True)
def norm2_numba(array):
    norm = 0.0
    for i in nb.prange(array.shape[0]):
        norm += array[i] * array[i]
    return np.sqrt(norm)


def norm2(array):
    norm = 0.0
    for i in range(array.shape[0]):
        norm += array[i] * array[i]
    return np.sqrt(norm)


@nb.njit(fastmath=True, parallel=True)
def dot_mat_numba(indptr, indices, data, array):
    out = np.zeros(indptr.shape[0] - 1)
    for i in nb.prange(indptr.shape[0] - 1):
        tmp = 0.0
        for j in nb.prange(indptr[i], indptr[i + 1]):
            tmp += data[j] * array[indices[j]]
            out[i] = tmp
    return out


def dot_mat(mat, array):
    indptr = mat.indptr
    indices = mat.indices
    data = mat.data
    out = np.zeros(indptr.shape[0] - 1)
    for i in range(indptr.shape[0] - 1):
        tmp = 0.0
        for j in range(indptr[i], indptr[i + 1]):
            tmp += data[j] * array[indices[j]]
            out[i] = tmp
    return out


@nb.njit(fastmath=True, parallel=True)
def dot_vec_numba(array1, array2):
    out = 0.0
    for i in nb.prange(array1.shape[0]):
        out += array1[i] * array2[i]
    return out


def dot_vec(array1, array2):
    out = 0.0
    for i in range(array1.shape[0]):
        out += array1[i] * array2[i]
    return out


def get_logger(name: str):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(name)s]: %(levelname)s - %(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = logging.getLogger(name)
    return logger


def save_sparse_csr(filename, mat, b_vec):
    np.savez(filename,
             data=mat.data,
             indices=mat.indices,
             indptr=mat.indptr,
             b_vec=b_vec,
             shape=mat.shape)


def load_sparse_csr(filename):
    loader = np.load(filename)
    new_csr_mat = csr_matrix(
        (loader['data'], loader['indices'], loader['indptr']),
        shape=loader['shape']
    )
    b_vec = loader['b_vec']
    return new_csr_mat, b_vec
