#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import shutil
import subprocess
import time


# import requests
# def download(url, dest):
# 	# print("download {0} {1}".format(url, dest))
# 	r = requests.get(url, allow_redirects=True)
# 	with open(dest, "ab") as fdest:
# 		fdest.write(r.content)

def fcopy(fpath_from, fpath_to):
	# print("copying {0} {1}".format(fpath_from, fpath_to))
	shutil.copyfile(fpath_from, fpath_to)


def fdelete(fpath):
	# print("deleting {0}".format(fpath))
	os.remove(fpath)


def frename(fpath_old, fpath_new):
	# print("frename {0} {1}".format(fpath_old, fpath_new))
	os.rename(fpath_old, fpath_new)


def fcreate(fpath):
	# print("fcreate {0}".format(fpath))
	with open(fpath, "a"):
		pass


def fexist(fpath):
	# print("fexist {0}".format(fpath))
	return os.path.isfile(fpath)


def compile_sol(sol, online_judge, standard, verbose):
	# print("compile {0}", online_judge)
	
	compiler = "g++" # clang
	# compiler = "g++-5" # gcc
	standard = "-std=c++11" if standard is None else "-std={0}".format(standard)
	optimizer = "-O2"
	precompile_link = "" # clang
	# precompile_link = "-I/usr/include -L/usr/lib" # gcc
	precompile_template = "-I{0}".format(sol.judge_path) if not online_judge else ""
	extra_flag = "" # http://codeforces.com/blog/entry/15547
	stack_size = "-Wl,-stack_size,0x10000000" # clang
	# stack_size = "-Wl,--stack=0x10000000" # gcc
	define_symbol = "-DHHHDEBUG" if not online_judge else ""
	output_binary = "-o {0}".format(sol.binary)
	input_sources = "{0}".format(sol.source)

	full_command = [compiler, standard, optimizer, precompile_link, precompile_template, extra_flag, stack_size, define_symbol, output_binary, input_sources]
	full_command = " ".join(full_command)
	

	completed = subprocess.run(full_command, stdin=None, input=None, stdout=None, stderr=None, shell=True, timeout=None, check=False)
	# class subprocess.CompletedProcess
	# args
	# returncode
	# stdout
	# stderr
	# check_returncode()

	# print(online_judge)
	# print("define_symbol: {0}".format(define_symbol))
	# print(full_command)
	# print(completed.returncode)

	if 0 == completed.returncode:
		return True
	else:
		if verbose:
			print("{0}".format(full_command))
		return False


def run_sol(sol, input_sources, output_dest, verbose):
	# print("run")

	# 
	# https://docs.python.org/3/library/subprocess.html
	# 

	STDIN = "stdin"
	STDOUT = "stdout"

	if input_sources is None:
		input_sources = []
		if fexist(sol.default_input):
			input_sources.append(sol.default_input)
		else:
			input_sources.append(STDIN)
	else:
		input_sources = ["{0}/{1}".format(sol.cwd, input_source) if input_source != STDIN else STDIN for input_source in input_sources]
	
	# print("input_sources:")
	# print(input_sources)

	if output_dest is None:
		output_dest = STDOUT
	else:
		if output_dest != STDOUT:
			output_dest = "{0}/{1}".format(sol.cwd, output_dest)
			if fexist(output_dest):
				fdelete(output_dest)
	
	# print("output_dest:")
	# print(output_dest)

	full_command = "{0}".format(sol.binary)

	# http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate
	# http://stackoverflow.com/questions/10363853/reading-writing-to-a-popen-subprocess
	# http://stackoverflow.com/questions/18344932/python-subprocess-call-stdout-to-file-stderr-to-file-display-stderr-on-scree
	# http://stackoverflow.com/questions/89228/calling-an-external-command-in-python

	for ieach in range(0, len(input_sources)):
		each = input_sources[ieach]
		this_command = full_command
		if each != STDIN:
			this_command += " < {0}".format(each)
		if output_dest != STDOUT:
			this_command += " >> {0}".format(output_dest)

		# print("full_command:\n{0}".format(full_command))
		# print("this_command:\n{0}".format(this_command))
		
		time_start = time.perf_counter()
		completed = subprocess.run(this_command, stdin=None, input=None, stdout=None, stderr=None, shell=True, timeout=None, check=False)
		time_end = time.perf_counter()
		time_used = (time_end - time_start) * 1000

		delimiter = "----{0}------------------------------".format(" Time: {0:4.0f} ms ".format(time_used) if verbose else "---------------")
		if verbose or ieach	!= len(input_sources) - 1:
			if output_dest == STDOUT:
				print(delimiter)
			else:
				with open(output_dest, "a") as output_dest_f:
					output_dest_f.write(delimiter)
					output_dest_f.write("\n")


		if 0 != completed.returncode:
			return False

	return True


def cleanup_sol(sol):
	# print("cleanup_sol")
	if fexist(sol.binary):
		fdelete(sol.binary)


def template_exist(sol):
	# print("template_exist")
	exist = fexist(sol.template_header) and fexist(sol.template_source)
	return exist


def solution_exist(sol):
	# print("solution_exist {0}".format(sol.name))

	sol_exist = False
	msg = ""
	sol_exist = sol_exist or fexist(sol.source)
	sol_exist = sol_exist or fexist(sol.binary)
	sol_exist = sol_exist or fexist(sol.default_input)
	sol_exist = sol_exist or fexist(sol.default_output)

	if sol_exist:
		msg = "{0}.cpp / {0} / {0}.input / {0}.output already exists".format(sol.name)
	return sol_exist, msg


def create_sol(sol):
	# print("create_sol")

	# download(sol.template_source_url, sol.source)
	fcopy(sol.template_source, sol.source)
	fcreate(sol.default_input)
	# fcreate(sol.default_output)


def rename_sol(sol, sol_new):
	# print("rename_sol")
	sol_new_exist, msg = solution_exist(sol_new)
	if sol_new_exist:
		print("[ERROR] {0}.".format(msg))
		return 

	if fexist(sol.source):
		frename(sol.source, sol_new.source)
	if fexist(sol.binary):
		frename(sol.binary, sol_new.binary)
	if fexist(sol.default_input):
		frename(sol.default_input, sol_new.default_input)
	if fexist(sol.default_output):
		frename(sol.default_output, sol_new.default_output)


def open_sol(sol):
	# print("open_sol")
	os.system("{0} {1}".format(sol.application, sol.cwd))


def init_SOL(sol_name):
	TEMPLATE_ENABLE = True
	TEMPLATE_NAME = "template"
	# TEMPLATE_HEADER_URL = "https://gist.githubusercontent.com/cly753/70b633d36bc9b32e81c8/raw/2c65661ba2eca59892c9006bcca82ce191e857a2/template.h"
	# TEMPLATE_SOURCE_URL = "https://gist.githubusercontent.com/cly753/fdc989edc770c8c16e88/raw/d52bc75e21c207a82f7a1897f1b19ba423201bdc/template.cpp"

	APPLICATION = "subl"
	

	JUDGE_PATH = os.path.dirname(os.path.realpath(__file__))
	CWD = os.getcwd()

	# print(JUDGE_PATH)
	# print(CWD)

	class Nothing():
		pass
	SOL = Nothing()
	SOL.judge_path = JUDGE_PATH
	SOL.cwd = CWD
	SOL.name = sol_name
	SOL.source = "{0}/{1}.cpp".format(CWD, sol_name)
	SOL.binary = "{0}/{1}".format(CWD, sol_name)
	SOL.default_input = "{0}/{1}.input".format(CWD, sol_name)
	SOL.default_output = "{0}/{1}.output".format(CWD, sol_name)
	SOL.template_enable = TEMPLATE_ENABLE
	SOL.template = TEMPLATE_NAME
	SOL.template_header = "{0}/{1}.h".format(SOL.judge_path, SOL.template)
	SOL.template_source = "{0}/{1}.cpp".format(SOL.judge_path, SOL.template)
	# SOL.template_header_url = TEMPLATE_HEADER_URL
	# SOL.template_source_url = TEMPLATE_SOURCE_URL
	SOL.application = APPLICATION

	if not template_exist(SOL):
		print("[ERROR] template header not found at \n{0}\n{1}".format(SOL.template_header, SOL.template_source))
		exit(0)
	# if not template_exist(SOL):
	# 	download(SOL.template_header_url, SOL.template_header)
	return SOL


def create_solution(args):
	# print("create_solution")
	# print(args)
	sol = init_SOL(args.sol_name)

	sol_exist, msg = solution_exist(sol)
	if sol_exist:
		yes = input("[ERROR] {0}, open in default editor (y)? ".format(msg, sol.name))
		if yes == "y":
			open_sol(sol)
	else:
		create_sol(sol)
		yes = input("solution {0} created, open in default editor (y)? ".format(sol.name))
		if yes == "y":
			open_sol(sol)


def run_solution(args):
	# print("run_solution")
	# print(args)
	sol = init_SOL(args.sol_name)
	
	sol_exist, msg = solution_exist(sol)
	if not sol_exist:
		yes = input("[ERROR] solution {0} not found, create (y)? ".format(sol.name))
		if yes == "y":
			create_sol(sol)
			if args.verbose:
				print("solution {0} created.".format(sol.name))
			yes = input("open solution {0} in default editor (y)? ".format(sol.name))
			if yes == "y":
				open_sol(sol)
		return 

	if not fexist(sol.source):
		yes = input("[ERROR] solution {0} source {1} not found, rename the rest and create (y)? ".format(sol.name, sol.source))
		if yes == "y":
			new_name = input("rename the rest to : ")
			sol_new = init_SOL(new_name)
			rename_sol(sol, sol_new)

			if args.verbose:
				print("solution renamed {0} -> {1}.".format(args.sol_name, args.new_name))

			create_sol(sol)
			if args.verbose:
				print("solution {0} created.".format(sol.name))
			yes = input("open solution {0} in default editor (y)? ".format(sol.name))
			if yes == "y":
				open_sol(sol)
		return 

	# from pprint import pprint
	# pprint(args.i)
	# pprint(args.o)
	# pprint(args.oj)

	compile_success = compile_sol(sol, args.online_judge, args.std, args.verbose)
	if not compile_success:
		print("[ERROR] Compilation Error.")
	else:
		run_success = run_sol(sol, args.i, args.o, args.verbose)
		if not run_success:
			print("[ERROR] Runtime Error.")

	cleanup_sol(sol)


def rename_solution(args):
	# print("rename_solution")
	# print(args)
	sol = init_SOL(args.sol_name)
	sol_new = init_SOL(args.new_name)

	rename_sol(sol, sol_new)

	sol = sol_new
	if args.verbose:
		print("solution renamed {0} -> {1}.".format(args.sol_name, args.new_name))


def open_solution(args):
	# print("open_solution")
	# print(args)
	sol = init_SOL(args.sol_name)

	sol_exist, msg = solution_exist(sol)
	if not sol_exist:
		yes = input("[ERROR] solution {0} not found, create (y)? ".format(sol.name))
		if yes == "y":
			create_sol(sol)
			if args.verbose:
				print("solution {0} created.".format(sol.name))
			open_sol(sol)
	else:
		open_sol(sol)
	

def set_default_subparser(self, name, args=None):
	# http://stackoverflow.com/a/26379693/3315185
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()

    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed
    """
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)


def get_args():
	argparse.ArgumentParser.set_default_subparser = set_default_subparser

	parser = argparse.ArgumentParser(allow_abbrev=False)
	subparsers = parser.add_subparsers(help="sub-command help")

	create_parser = subparsers.add_parser("create", help="create solution")

	create_parser.add_argument("sol_name", type=str, help="create solution")
	create_parser.add_argument("-v", "--verbose", action="store_true", help="show verbose output")
	create_parser.set_defaults(func=create_solution)



	run_parser = subparsers.add_parser("run", help="run solution (default)")

	run_parser.add_argument("sol_name", type=str, help="run solution")
	run_parser.add_argument("-i", type=str, nargs="+", help="specify input sources (stdin case_1.in ...)")
	run_parser.add_argument("-o", type=str, help="specify output destination (stdout / case_1.out / ...)")
	run_parser.add_argument("-v", "--verbose", action="store_true", help="show verbose output")
	run_parser.add_argument("-oj", "--online_judge", action="store_true", help="run solution as online judge")
	run_parser.add_argument("-std", type=str, help="specify c++ standard")
	run_parser.set_defaults(func=run_solution)



	rename_parser = subparsers.add_parser("rename", help="rename solution")

	rename_parser.add_argument("sol_name", type=str, help="solution to rename")
	rename_parser.add_argument("new_name", type=str, help="new name for solution")
	rename_parser.add_argument("-v", "--verbose", action="store_true", help="show verbose output")
	rename_parser.set_defaults(func=rename_solution)



	open_parser = subparsers.add_parser("open", help="open solution")

	open_parser.add_argument("sol_name", type=str, help="solution to open")
	open_parser.add_argument("-v", "--verbose", action="store_true", help="show verbose output")
	open_parser.set_defaults(func=open_solution)



	parser.set_default_subparser("run")
	args = parser.parse_args()
	return args


def judge():
	args = get_args()
	args.func(args)


if __name__ == "__main__":
	judge()