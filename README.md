#### local judge



run: [solution name]

$ judge [run] [solution name] [input] [output] [other --online] [-v --verbose]
$ judge [x] [x.input y.input generator] [x.output] --online
$ judge generator

* stdin: default x.input
* stdin: choose terminal / y.input
* stdin: choose generator
* stdout: default terminal
* stdout: choose x.output / y.output
* stderr: warn
* redirect to create if x.cpp && x.input && x.output is missing



open: [solution name]

$ judge open x

* open solution x in default text editor



create: x.cpp x.input x.output

$ judge create x

* abort if template.cpp template.h is missing
* abort if x.input || x.output exists
* prompt to open with subl x.cpp if x.cpp exists
* prompt to open with subl after create



compare: x.answer

* ...

rename: rename x y

* rename x.cpp x.input x.output ... to y.cpp y.input y.output

