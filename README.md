#### local judge

---

```
usage: judge [-h] {create,run,rename,open} ...

positional arguments:
  {create,run,rename,open}
                        sub-command help
    create              create solution
    run                 run solution (default)
    rename              rename solution
    open                open solution

optional arguments:
  -h, --help            show this help message and exit
```

---

```
usage: judge create [-h] [-v] sol_name

positional arguments:
  sol_name       create solution

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  show verbose output
```

---

```
usage: judge run [-h] [-i I [I ...]] [-o O] [-v] [-oj] [-std STD] sol_name

positional arguments:
  sol_name             run solution

optional arguments:
  -h, --help           show this help message and exit
  -i I [I ...]         specify input sources (stdin case_1.in ...)
  -o O                 specify output destination (stdout / case_1.out / ...)
  -v, --verbose        show verbose output
  -oj, --online_judge  run solution as online judge
  -std STD             specify c++ standard

```

---

```
usage: judge rename [-h] [-v] sol_name new_name

positional arguments:
  sol_name       solution to rename
  new_name       new name for solution

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  show verbose output

```

---

```
usage: judge open [-h] [-v] sol_name

positional arguments:
  sol_name       solution to open

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  show verbose output
```

---



> run: [solution name]
> 
> $ judge [run] [solution name] [input] [output] [other --online] [-v --verbose]
> $ judge [x] [x.input y.input generator] [x.output] --online
> $ judge generator
> 
> * stdin: default x.input
> * stdin: choose terminal / y.input
> * stdin: choose generator
> * stdout: default terminal
> * stdout: choose x.output / y.output
> * stderr: warn
> * redirect to create if x.cpp && x.input && x.output is missing
> 
> 
> 
> open: [solution name]
> 
> $ judge open x
> 
> * open solution x in default text editor
> 
> 
> 
> create: x.cpp x.input x.output
> 
> $ judge create x
> 
> * abort if template.cpp template.h is missing
> * abort if x.input || x.output exists
> * prompt to open with subl x.cpp if x.cpp exists
> * prompt to open with subl after create
> 
> 
> 
> compare: x.answer
> 
> * ...
> 
> rename: rename x y
> 
> * rename x.cpp x.input x.output ... to y.cpp y.input y.output
> 
> 