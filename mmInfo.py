import scipy.io as sio
import numpy as np
import sys

from helper import save_sparse_csr

argv = sys.argv
if len(argv) != 2:
    print('Usage: python %s [MatrixMarket file]' % argv[0])
    quit()
target = argv[1]
(size_x, size_y, _, _, field, symmetry) = sio.mminfo(target)
mat = sio.mmread(target)

file_type = mat.getformat()
min_all = mat.min()
max_all = mat.max()
nnz = mat.getnnz()
nnz_row = mat.getnnz(1)
min_nnz = min(nnz_row)
max_nnz = max(nnz_row)
ave_nnz = np.average(nnz_row)
zero = float(size_x * size_x - nnz) / float(size_x * size_x) * 100.0

print("対称性 = %s" % symmetry)
print("格納形式 = %s" % file_type)
if symmetry == 'symmetric':
    print("次元数 = %d" % (size_x * size_x))
else:
    print("X-サイズ = %d" % size_x)
    print("Y-サイズ = %d" % size_y)
print("非ゼロ要素数 = %d" % nnz)
print("ゼロ要素割合 = %.3f%%" % zero)
print("行最大非ゼロ要素数 = %d" % max_nnz)
print("行最小非ゼロ要素数 = %d" % min_nnz)
print("行平均非ゼロ要素数 = %d" % ave_nnz)
print("最大要素数 = %.16e" % max_all)
print("最小要素数 = %.16e" % min_all)

mat_csr = mat.tocsr()
x_vec = []
for i in range(mat_csr.shape[0]):
    x_vec.append(1)
b_vec = mat_csr.dot(x_vec)
print('未知ベクトルを1になるように右辺ベクトルを生成　完了')

save_sparse_csr(argv[1].replace('.mtx', '.npz'), mat_csr, b_vec)