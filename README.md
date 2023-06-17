## Setup

https://python-poetry.org/docs/#installation
```
poetry install
```

## Setup Matrix

Sparse symmetric positive definite matrix

[BCSSTK14](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/bcsstruc2/bcsstk14.html)

[BCSSTK17](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/bcsstruc2/bcsstk17.html)

```
wget https://math.nist.gov/pub/MatrixMarket2/Harwell-Boeing/bcsstruc2/bcsstk14.mtx.gz
gunzip -d bcsstk14.mtx.gz
mv bcsstk14.mtx matrix/
python mmInfo.py matrix/bcsstk14.mtx
```

```
wget https://math.nist.gov/pub/MatrixMarket2/Harwell-Boeing/bcsstruc2/bcsstk17.mtx.gz
gunzip -d bcsstk17.mtx.gz
mv bcsstk17.mtx matrix/
python mmInfo.py matrix/bcsstk17.mtx
```

反復の結果が正解に近づいたかどうかを確認するため、
予めに未知ベクトルを1になるように、右辺ベクトルを作成する。
```
$$ A\boldsymbol{x}=\boldsymbol{b} $$
```

## Run
```
❯ python main.py -h
usage: main.py [-h] [-v] [-cg] [-t TARGET_MATRIX] [-b BASE_DIR] [-imax ITERATE_MAX] [-e EPSILON] [-np] [-nb]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose
  -cg, --conjugate_gradient_method
                        CG method
  -t TARGET_MATRIX, --target_matrix TARGET_MATRIX
                        target matrix name
  -b BASE_DIR, --base_dir BASE_DIR
                        base directory
  -imax ITERATE_MAX, --iterate_max ITERATE_MAX
                        max iteration
  -e EPSILON, --epsilon EPSILON
                        epsilon
  -np, --numpy          use numpy
  -nb, --numba          use numba
```

```
# cg
python main.py -v -cg -t bcsstk17 -imax 30000 -e 1e-10
```

## Benchmark
Apple M1 Pro
### bcsstk14
```
# basic
❯ python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9
[06/17/23 21:42:28] INFO     [2023-06-17 21:42:28,303][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: False, numba:     main.py:19
                             False
                    INFO     [2023-06-17 21:42:28,310][solver]: INFO - CG method                                                                                          main.py:23
[06/17/23 21:49:16] INFO     [2023-06-17 21:49:16,777][solver]: INFO - is_converged = True, loop = 11496, time = 408 s       

# with numpy
❯ python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9 -np
[06/17/23 21:42:21] INFO     [2023-06-17 21:42:21,810][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: True, numba:      main.py:19
                             False
                    INFO     [2023-06-17 21:42:21,817][solver]: INFO - CG method                                                                                          main.py:23
                    INFO     [2023-06-17 21:42:21,826][solver]: INFO - use numpy                                                                                          main.py:26
[06/17/23 21:42:23] INFO     [2023-06-17 21:42:23,112][solver]: INFO - is_converged = True, loop = 11314, time = 1 s                                                      main.py:34

# with numba
❯ python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9 -nb
[06/17/23 22:07:07] INFO     [2023-06-17 22:07:07,763][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: False, numba: True                                                           main.py:19
                    INFO     [2023-06-17 22:07:07,770][solver]: INFO - CG method                                                                                                                                                     main.py:23
[06/17/23 22:07:13] INFO     [2023-06-17 22:07:13,938][solver]: INFO - is_converged = True, loop = 11293, time = 6 s          
```