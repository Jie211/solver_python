## Setup

https://python-poetry.org/docs/#installation
```
poetry install
```

## Setup Matrix

Sparse symmetric positive definite matrix

[BCSSTK14](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/bcsstruc2/bcsstk14.html)

[BCSSTK17](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/bcsstruc2/bcsstk17.html)

[C3DKT3M2](https://math.nist.gov/pub/MatrixMarket2/misc/cylshell/s3dkt3m2.mtx.gz)

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

```
wget https://math.nist.gov/pub/MatrixMarket2/misc/cylshell/s3dkt3m2.mtx.gz
gunzip -d s3dkt3m2.mtx.gz
mv s3dkt3m2.mtx matrix/
python src/mmInfo.py matrix/s3dkt3m2.mtx
```

## Run
```
❯ python main.py -h
usage: main.py [-h] [-v] [-cg] [-t TARGET_MATRIX] [-b BASE_DIR] [-fout FIGURE_OUTPUT_PATH] [-imax ITERATE_MAX] [-e EPSILON] [-np] [-nb] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose
  -cg, --conjugate_gradient_method
                        CG method
  -t TARGET_MATRIX, --target_matrix TARGET_MATRIX
                        target matrix name
  -b BASE_DIR, --base_dir BASE_DIR
                        base directory
  -fout FIGURE_OUTPUT_PATH, --figure_output_path FIGURE_OUTPUT_PATH
                        figure output path
  -imax ITERATE_MAX, --iterate_max ITERATE_MAX
                        max iteration
  -e EPSILON, --epsilon EPSILON
                        epsilon
  -np, --numpy          use numpy
  -nb, --numba          use numba
  -f, --figure          create figure
```

```
# cg
python main.py -v -cg -t bcsstk17 -imax 30000 -e 1e-10
```

## Figure

![BCSSTK14](https://raw.githubusercontent.com/Jie211/solver_python/main/figure/bcsstk14_30000_1e-09_cg.png)

![BCSSTK17](https://raw.githubusercontent.com/Jie211/solver_python/main/figure/bcsstk17_30000_1e-09_cg.png)

![S3DKT3M2](https://raw.githubusercontent.com/Jie211/solver_python/main/figure/s3dkt3m2_900000_1e-09_cg.png)


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

CentOS7 8v/16GB
### bcsstk14
```
# basic
(solver-py3.9) [gchen@gchen-sandbox]~/solver_python% python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9
[06/18/23 10:36:44] INFO     [2023-06-18 10:36:44,983][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: False, numba: False     main.py:19
                    INFO     [2023-06-18 10:36:44,999][solver]: INFO - CG method                                                                                                main.py:23
[06/18/23 10:52:17] INFO     [2023-06-18 10:52:17,165][solver]: INFO - is_converged = True, loop = 11496, time = 932 s     

# with numpy
(solver-py3.9) [gchen@gchen-sandbox]~/solver_python% python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9 -np
[06/18/23 10:52:27] INFO     [2023-06-18 10:52:27,320][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: True, numba: False      main.py:19
                    INFO     [2023-06-18 10:52:27,337][solver]: INFO - CG method                                                                                                main.py:23
                    INFO     [2023-06-18 10:52:27,339][solver]: INFO - use numpy                                                                                                main.py:26
[06/18/23 10:52:29] INFO     [2023-06-18 10:52:29,725][solver]: INFO - is_converged = True, loop = 11498, time = 2 s      

# with numba
(solver-py3.9) [gchen@gchen-sandbox]~/solver_python% python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9 -nb
[06/18/23 10:52:33] INFO     [2023-06-18 10:52:33,731][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: False, numba: True      main.py:19
                    INFO     [2023-06-18 10:52:33,747][solver]: INFO - CG method                                                                                                main.py:23
[06/18/23 10:52:38] INFO     [2023-06-18 10:52:38,157][solver]: INFO - is_converged = True, loop = 11286, time = 4 s              

# numba with SVML
poetry add icc_rt
(solver-py3.9) [gchen@gchen-sandbox]~/solver_python% python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9 -nb
[06/18/23 10:54:51] INFO     [2023-06-18 10:54:51,941][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: False, numba: True      main.py:19
                    INFO     [2023-06-18 10:54:51,958][solver]: INFO - CG method                                                                                                main.py:23
[06/18/23 10:54:56] INFO     [2023-06-18 10:54:56,027][solver]: INFO - is_converged = True, loop = 11286, time = 4 s           

# numba with openmp
pyenv install anaconda3-2023.03
pyenv local anaconda3-2023.03
conda create -n solver_openmp python=3.9 --no-default-packages
conda activate solver_openmp
conda install numba cffi -c drtodd13 -c conda-forge --override-channels
conda install rich scipy
https://www.openmp.org/wp-content/uploads/OpenMPBoothTalk-PyOMP.pdf
(solver-py3.9) [gchen@gchen-sandbox]~/solver_python% python main.py -cg -t bcsstk14 -imax 30000 -e 1e-9 -nb
[06/18/23 11:54:51] INFO     [2023-06-18 11:54:51,941][solver]: INFO - mat_file: ./matrix/bcsstk14.npz, max_inter: 30000, epsilon: 1.000000e-09, numpy: False, numba: True      main.py:19
                    INFO     [2023-06-18 11:54:51,958][solver]: INFO - CG method                                                                                                main.py:23
[06/18/23 11:54:56] INFO     [2023-06-18 11:54:56,027][solver]: INFO - is_converged = True, loop = 11286, time = 4 s     
```

```
# k8s

# numpy 2core
solver-job-xmqh5 solver [06/19/23 23:44:00] INFO     [2023-06-19 23:44:00,801][solver]: INFO  main.py:22
solver-job-xmqh5 solver                              - mat_file: /app/bcsstk17.npz,
solver-job-xmqh5 solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-xmqh5 solver                              numpy: True, numba: False
solver-job-xmqh5 solver                     INFO     [2023-06-19 23:44:00,822][solver]: INFO  main.py:27
solver-job-xmqh5 solver                              - CG method
solver-job-xmqh5 solver                     INFO     [2023-06-19 23:44:00,824][solver]: INFO  main.py:30
solver-job-xmqh5 solver                              - use numpy
solver-job-xmqh5 solver [06/19/23 23:44:16] INFO     [2023-06-19 23:44:16,781][solver]: INFO  main.py:41
solver-job-xmqh5 solver                              - is_converged = True, loop = 21024,
solver-job-xmqh5 solver                              time = 15 s

# numpy 4core
+ solver-job-6x8r7 › solver
solver-job-6x8r7 solver [06/19/23 23:44:37] INFO     [2023-06-19 23:44:37,179][solver]: INFO  main.py:22
solver-job-6x8r7 solver                              - mat_file: /app/bcsstk17.npz,
solver-job-6x8r7 solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-6x8r7 solver                              numpy: True, numba: False
solver-job-6x8r7 solver                     INFO     [2023-06-19 23:44:37,201][solver]: INFO  main.py:27
solver-job-6x8r7 solver                              - CG method
solver-job-6x8r7 solver                     INFO     [2023-06-19 23:44:37,203][solver]: INFO  main.py:30
solver-job-6x8r7 solver                              - use numpy
solver-job-6x8r7 solver [06/19/23 23:45:04] INFO     [2023-06-19 23:45:04,145][solver]: INFO  main.py:41
solver-job-6x8r7 solver                              - is_converged = True, loop = 20961,
solver-job-6x8r7 solver                              time = 26 s
- solver-job-6x8r7 › solver

# numpy 8core
+ solver-job-cgh9d › solver
solver-job-cgh9d solver [06/19/23 23:45:25] INFO     [2023-06-19 23:45:25,251][solver]: INFO  main.py:22
solver-job-cgh9d solver                              - mat_file: /app/bcsstk17.npz,
solver-job-cgh9d solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-cgh9d solver                              numpy: True, numba: False
solver-job-cgh9d solver                     INFO     [2023-06-19 23:45:25,270][solver]: INFO  main.py:27
solver-job-cgh9d solver                              - CG method
solver-job-cgh9d solver                     INFO     [2023-06-19 23:45:25,271][solver]: INFO  main.py:30
solver-job-cgh9d solver                              - use numpy
solver-job-cgh9d solver [06/19/23 23:45:46] INFO     [2023-06-19 23:45:46,989][solver]: INFO  main.py:41
solver-job-cgh9d solver                              - is_converged = True, loop = 21036,
solver-job-cgh9d solver                              time = 21 s

# numpy 16core
+ solver-job-rtdbd › solver
solver-job-rtdbd solver [06/19/23 23:47:46] INFO     [2023-06-19 23:47:46,931][solver]: INFO  main.py:22
solver-job-rtdbd solver                              - mat_file: /app/bcsstk17.npz,
solver-job-rtdbd solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-rtdbd solver                              numpy: True, numba: False
solver-job-rtdbd solver                     INFO     [2023-06-19 23:47:46,957][solver]: INFO  main.py:27
solver-job-rtdbd solver                              - CG method
solver-job-rtdbd solver                     INFO     [2023-06-19 23:47:46,959][solver]: INFO  main.py:30
solver-job-rtdbd solver                              - use numpy
solver-job-rtdbd solver [06/19/23 23:48:18] INFO     [2023-06-19 23:48:18,799][solver]: INFO  main.py:41
solver-job-rtdbd solver                              - is_converged = True, loop = 20961,
solver-job-rtdbd solver                              time = 31 s

# numpy 32core
+ solver-job-v7nlr › solver
solver-job-v7nlr solver [06/19/23 23:49:07] INFO     [2023-06-19 23:49:07,316][solver]: INFO  main.py:22
solver-job-v7nlr solver                              - mat_file: /app/bcsstk17.npz,
solver-job-v7nlr solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-v7nlr solver                              numpy: True, numba: False
solver-job-v7nlr solver                     INFO     [2023-06-19 23:49:07,352][solver]: INFO  main.py:27
solver-job-v7nlr solver                              - CG method
solver-job-v7nlr solver                     INFO     [2023-06-19 23:49:07,355][solver]: INFO  main.py:30
solver-job-v7nlr solver                              - use numpy
solver-job-v7nlr solver [06/19/23 23:49:46] INFO     [2023-06-19 23:49:46,961][solver]: INFO  main.py:41
solver-job-v7nlr solver                              - is_converged = True, loop = 20966,
solver-job-v7nlr solver                              time = 39 s

# numpy 64core
+ solver-job-6znpr › solver
solver-job-6znpr solver [06/19/23 23:50:21] INFO     [2023-06-19 23:50:21,416][solver]: INFO  main.py:22
solver-job-6znpr solver                              - mat_file: /app/bcsstk17.npz,
solver-job-6znpr solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-6znpr solver                              numpy: True, numba: False
solver-job-6znpr solver                     INFO     [2023-06-19 23:50:21,439][solver]: INFO  main.py:27
solver-job-6znpr solver                              - CG method
solver-job-6znpr solver                     INFO     [2023-06-19 23:50:21,441][solver]: INFO  main.py:30
solver-job-6znpr solver                              - use numpy
solver-job-6znpr solver [06/19/23 23:50:48] INFO     [2023-06-19 23:50:48,569][solver]: INFO  main.py:41
solver-job-6znpr solver                              - is_converged = True, loop = 21024,
solver-job-6znpr solver                              time = 27 s
- solver-job-6znpr › solver

########################

# numba 2core
+ solver-job-n4swt › solver
solver-job-n4swt solver [06/19/23 23:33:20] INFO     [2023-06-19 23:33:20,028][solver]: INFO  main.py:22
solver-job-n4swt solver                              - mat_file: /app/bcsstk17.npz,
solver-job-n4swt solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-n4swt solver                              numpy: False, numba: True
solver-job-n4swt solver                     INFO     [2023-06-19 23:33:20,051][solver]: INFO  main.py:27
solver-job-n4swt solver                              - CG method
solver-job-n4swt solver [06/19/23 23:33:41] INFO     [2023-06-19 23:33:41,038][solver]: INFO  main.py:41
solver-job-n4swt solver                              - is_converged = True, loop = 21074,
solver-job-n4swt solver                              time = 20 s
- solver-job-n4swt › solver

# numba 4core
+ solver-job-4mpnh › solver
solver-job-4mpnh solver [06/19/23 23:34:53] INFO     [2023-06-19 23:34:53,378][solver]: INFO  main.py:22
solver-job-4mpnh solver                              - mat_file: /app/bcsstk17.npz,
solver-job-4mpnh solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-4mpnh solver                              numpy: False, numba: True
solver-job-4mpnh solver                     INFO     [2023-06-19 23:34:53,408][solver]: INFO  main.py:27
solver-job-4mpnh solver                              - CG method
solver-job-4mpnh solver [06/19/23 23:35:07] INFO     [2023-06-19 23:35:07,622][solver]: INFO  main.py:41
solver-job-4mpnh solver                              - is_converged = True, loop = 21006,
solver-job-4mpnh solver                              time = 14 s
- solver-job-4mpnh › solver

# numba 8core
+ solver-job-59c7q › solver
solver-job-59c7q solver [06/19/23 23:35:51] INFO     [2023-06-19 23:35:51,596][solver]: INFO  main.py:22
solver-job-59c7q solver                              - mat_file: /app/bcsstk17.npz,
solver-job-59c7q solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-59c7q solver                              numpy: False, numba: True
solver-job-59c7q solver                     INFO     [2023-06-19 23:35:51,615][solver]: INFO  main.py:27
solver-job-59c7q solver                              - CG method
solver-job-59c7q solver [06/19/23 23:36:01] INFO     [2023-06-19 23:36:01,412][solver]: INFO  main.py:41
solver-job-59c7q solver                              - is_converged = True, loop = 20966,
solver-job-59c7q solver                              time = 9 s
- solver-job-59c7q › solver


# numba 16core
+ solver-job-6k5rx › solver
solver-job-6k5rx solver [06/19/23 23:36:21] INFO     [2023-06-19 23:36:21,248][solver]: INFO  main.py:22
solver-job-6k5rx solver                              - mat_file: /app/bcsstk17.npz,
solver-job-6k5rx solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-6k5rx solver                              numpy: False, numba: True
solver-job-6k5rx solver                     INFO     [2023-06-19 23:36:21,271][solver]: INFO  main.py:27
solver-job-6k5rx solver                              - CG method
solver-job-6k5rx solver [06/19/23 23:36:31] INFO     [2023-06-19 23:36:31,608][solver]: INFO  main.py:41
solver-job-6k5rx solver                              - is_converged = True, loop = 21015,
solver-job-6k5rx solver                              time = 10 s
- solver-job-6k5rx › solver

# numba 32core
+ solver-job-69knc › solver
solver-job-69knc solver [06/19/23 23:37:14] INFO     [2023-06-19 23:37:14,625][solver]: INFO  main.py:22
solver-job-69knc solver                              - mat_file: /app/bcsstk17.npz,
solver-job-69knc solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-69knc solver                              numpy: False, numba: True
solver-job-69knc solver                     INFO     [2023-06-19 23:37:14,652][solver]: INFO  main.py:27
solver-job-69knc solver                              - CG method
solver-job-69knc solver [06/19/23 23:37:24] INFO     [2023-06-19 23:37:24,325][solver]: INFO  main.py:41
solver-job-69knc solver                              - is_converged = True, loop = 20903,
solver-job-69knc solver                              time = 9 s
- solver-job-69knc › solver

# numba 64core
+ solver-job-6mr7j › solver
solver-job-6mr7j solver [06/19/23 23:38:16] INFO     [2023-06-19 23:38:16,067][solver]: INFO  main.py:22
solver-job-6mr7j solver                              - mat_file: /app/bcsstk17.npz,
solver-job-6mr7j solver                              max_inter: 30000, epsilon: 1.000000e-09,
solver-job-6mr7j solver                              numpy: False, numba: True
solver-job-6mr7j solver                     INFO     [2023-06-19 23:38:16,100][solver]: INFO  main.py:27
solver-job-6mr7j solver                              - CG method
solver-job-6mr7j solver [06/19/23 23:38:35] INFO     [2023-06-19 23:38:35,750][solver]: INFO  main.py:41
solver-job-6mr7j solver                              - is_converged = True, loop = 20940,
solver-job-6mr7j solver                              time = 19 s

core	numpy	numba
 2	15	20
 4	26	14
 8	21	9
 16	31	10
 32	39	9
 64	27	19
 
 
# jupitor
# numpy
[06/20/23 09:16:39] INFO     [2023-06-20 09:16:39,483][solver]: INFO  ]8;id=56663;file://main.py\main.py]8;;\:]8;id=320704;file://main.py#22\22]8;;\
                             - mat_file: ./matrix/bcsstk17.npz,                 
                             max_inter: 30000, epsilon: 1.000000e-09,           
                             numpy: True, numba: False                          
                    INFO     [2023-06-20 09:16:39,583][solver]: INFO  ]8;id=471894;file://main.py\main.py]8;;\:]8;id=378988;file://main.py#27\27]8;;\
                             - CG method                                        
                    INFO     [2023-06-20 09:16:39,587][solver]: INFO  ]8;id=50280;file://main.py\main.py]8;;\:]8;id=878982;file://main.py#30\30]8;;\
                             - use numpy                                        
[06/20/23 09:17:28] INFO     [2023-06-20 09:17:28,732][solver]: INFO  ]8;id=281444;file://main.py\main.py]8;;\:]8;id=965601;file://main.py#41\41]8;;\
                             - is_converged = True, loop = 20961,               
                             time = 49 s    

# numba 2core
[06/20/23 09:19:17] INFO     [2023-06-20 09:19:17,183][solver]: INFO  ]8;id=437272;file://main.py\main.py]8;;\:]8;id=177239;file://main.py#22\22]8;;\
                             - mat_file: ./matrix/bcsstk17.npz,                 
                             max_inter: 30000, epsilon: 1.000000e-09,           
                             numpy: False, numba: True                          
                    INFO     [2023-06-20 09:19:17,287][solver]: INFO  ]8;id=513870;file://main.py\main.py]8;;\:]8;id=461616;file://main.py#27\27]8;;\
                             - CG method                                        
[06/20/23 09:19:51] INFO     [2023-06-20 09:19:51,567][solver]: INFO  ]8;id=846316;file://main.py\main.py]8;;\:]8;id=670173;file://main.py#41\41]8;;\
                             - is_converged = True, loop = 21074,               
                             time = 34 s     

# numba 4core
[06/20/23 09:20:08] INFO     [2023-06-20 09:20:08,053][solver]: INFO  ]8;id=278055;file://main.py\main.py]8;;\:]8;id=581289;file://main.py#22\22]8;;\
                             - mat_file: ./matrix/bcsstk17.npz,                 
                             max_inter: 30000, epsilon: 1.000000e-09,           
                             numpy: False, numba: True                          
                    INFO     [2023-06-20 09:20:08,130][solver]: INFO  ]8;id=337200;file://main.py\main.py]8;;\:]8;id=208491;file://main.py#27\27]8;;\
                             - CG method                                        
[06/20/23 09:20:32] INFO     [2023-06-20 09:20:32,702][solver]: INFO  ]8;id=206033;file://main.py\main.py]8;;\:]8;id=593269;file://main.py#41\41]8;;\
                             - is_converged = True, loop = 21006,               
                             time = 24 s                              

# cupy
[06/20/23 09:52:41] INFO     [2023-06-20 09:52:41,465][solver]: INFO  ]8;id=604059;file://main.py\main.py]8;;\:]8;id=967457;file://main.py#23\23]8;;\
                             - mat_file: ./matrix/bcsstk17.npz,                 
                             max_inter: 30000, epsilon: 1.000000e-09,           
                             numpy: False, numba: False, cupy: True             
[06/20/23 09:52:42] INFO     [2023-06-20 09:52:42,512][solver]: INFO  ]8;id=157744;file://main.py\main.py]8;;\:]8;id=608545;file://main.py#31\31]8;;\
                             - CG method                                        
[06/20/23 09:53:21] INFO     [2023-06-20 09:53:21,268][solver]: INFO  ]8;id=306277;file://main.py\main.py]8;;\:]8;id=299987;file://main.py#48\48]8;;\
                             - is_converged = True, loop = 21020,               
                             time = 38 s
```