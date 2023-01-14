import random
import subprocess
import os
import sys

#list of 55 ltl formula from 
pattern = list()
pattern.append({'ltl' : "[] ( ! p )", 'ptype' : "Absense", 'mtype' : "Globally", 'size' : 1})
pattern.append({'ltl' : "<> r -> ( ! p U r )", 'ptype' : "Absense", 'mtype' : "Before R", 'size' : 2})
pattern.append({'ltl' : "[] ( q -> [] ( ! p ) )", 'ptype' : "Absense", 'mtype' : "After Q", 'size' : 2})
pattern.append({'ltl' : "[] ( ( q && ! r && <> r ) -> ( ! p U r ) )", 'ptype' : "Absense", 'mtype' : "Between Q and R", 'size' : 3})
pattern.append({'ltl' : "[] ( q && ! r -> ( ! p U ( r || [] ! p ) ) )", 'ptype' : "Absense", 'mtype' : "After Q until R", 'size' : 3})

pattern.append({'ltl' : "<> ( p )", 'ptype' : "Existence", 'mtype' : "Globally", 'size' : 1})
pattern.append({'ltl' : "! r U ( ( p && ! r ) || [] ! r )", 'ptype' : "Existence", 'mtype' : "Before R", 'size' : 2})
pattern.append({'ltl' : "[] ( ! q ) || <> ( q && <> p )", 'ptype' : "Existence", 'mtype' : "After Q", 'size' : 3})
pattern.append({'ltl' : "[] ( q && ! r -> ( ! r U ( ( p && ! r ) || [] ! r ) ) )", 'ptype' : "Existence", 'mtype' : "Between Q and R", 'size' : 3})
pattern.append({'ltl' : "[] ( q && ! r -> ( ! r U ( p && ! r ) ) )", 'ptype' : "Existence", 'mtype' : "After Q until R", 'size' : 2})

pattern.append({'ltl' : "( ! p U ( ( p U ( ( ! p U ( ( p U ( [] ! p || [] p ) ) || [] ! p ) ) || [] p ) ) || [] ! p ) )", 'ptype' : "Bounded Existence", 'mtype' : "Globally", 'size' : 9})
pattern.append({'ltl' : "<> r -> ( ( ! p && ! r ) U ( r || ( ( p && ! r ) U  ( r || ( ( ! p && ! r ) U ( r || ( ( p && ! r ) U ( r || ( ! p U r ) ) ) ) ) ) ) ) )", 'ptype' : "Bounded Existence", 'mtype' : "Before R", 'size' : 6})
pattern.append({'ltl' : "<> q -> ( ! q U ( q && ( ! p U ( ( p U ( ( ! p U ( ( p U ( [] ! p || [] p ) ) || [] ! p ) ) || [] p ) ) || [] ! p ) ) ) )", 'ptype' : "Bounded Existence", 'mtype' : "After Q", 'size' : 11})
pattern.append({'ltl' : "[] ( ( q && <> r ) -> ( ( ! p && ! r ) U ( r || ( ( p && ! r ) U ( r || ( ( ! p && ! r ) U ( r || ( ( p && ! r ) U ( r || ( ! p U r ) ) ) ) ) ) ) ) ) )", 'ptype' : "Bounded Existence", 'mtype' : "Between Q and R", 'size' : 6})
pattern.append({'ltl' : "[] ( q -> ( ( ! p && ! r ) U ( r || ( ( p && ! r ) U ( r || ( ( ! p && ! r ) U ( r || ( ( p && ! r ) U ( r || ( ! p U ( r || [] ! p ) ) || [] p ) ) ) ) ) ) ) ) )", 'ptype' : "Bounded Existence", 'mtype' : "After Q until R", 'size' : 8})

pattern.append({'ltl' : "[] ( p )", 'ptype' : "Universality", 'mtype' : "Globally", 'size' : 1})
pattern.append({'ltl' : "<> r -> ( p U r )", 'ptype' : "Universality", 'mtype' : "Before R", 'size' : 2})
pattern.append({'ltl' : "[] ( q -> [] ( p ) )", 'ptype' : "Universality", 'mtype' : "After Q", 'size' : 2})
pattern.append({'ltl' : "[] ( ( q && ! r && <> r ) -> ( p U r ) )", 'ptype' : "Universality", 'mtype' : "Between Q and R", 'size' : 3})
pattern.append({'ltl' : "[] ( q && ! r -> ( p U ( r || [] p ) ) )", 'ptype' : "Universality", 'mtype' : "After Q until R", 'size' : 3})

pattern.append({'ltl' : "! p U ( s || [] ! p )", 'ptype' : "Precedence", 'mtype' : "Globally", 'size' : 2})
pattern.append({'ltl' : "<> r -> ( ! p U ( s || r ) )", 'ptype' : "Precedence", 'mtype' : "Before R", 'size' : 2})
pattern.append({'ltl' : "[] ! q || <> ( q && ( p U ( s || [] ! p ) ) )", 'ptype' : "Precedence", 'mtype' : "After Q", 'size' : 4})
pattern.append({'ltl' : "[] ( ( q && ! r && <> r ) -> ( ! p U ( s || r ) ) )", 'ptype' : "Precedence", 'mtype' : "Between Q and R", 'size' : 3})
pattern.append({'ltl' : "[] ( q && ! r -> ( ! p U ( ( s || r ) || [] ! p ) ) )", 'ptype' : "Precedence", 'mtype' : "After Q until R", 'size' : 3})

pattern.append({'ltl' : "[] ( p -> <> s )", 'ptype' : "Response", 'mtype' : "Globally", 'size' : 2})
pattern.append({'ltl' : "<> r -> ( p -> ( ! r U ( s && ! r ) ) ) U r", 'ptype' : "Response", 'mtype' : "Before R", 'size' : 3})
pattern.append({'ltl' : "[] ( q -> [] ( p -> <> s ) )", 'ptype' : "Response", 'mtype' : "After Q", 'size' : 3})
pattern.append({'ltl' : "[] ( ( q && ! r && <> r ) -> ( p -> ( ! r U ( s && ! r ) ) ) U r )", 'ptype' : "Response", 'mtype' : "Between Q and R", 'size' : 4})
pattern.append({'ltl' : "[] ( q && ! r -> ( p -> ( ! r U ( s && ! r ) ) ) U ( r || [] ( p -> ( ! r U ( s && ! r ) ) ) ) )", 'ptype' : "Response", 'mtype' : "After Q until R", 'size' : 5})

pattern.append({'ltl' : "<> p -> ( ! p U ( s && ! p && X ( ! p U t ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "Globally", 'size' : 4})
pattern.append({'ltl' : "<> r -> ( ! p U ( r || ( s && ! p && X ( ! p U t ) ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "Before R", 'size' : 4})
pattern.append({'ltl' : "( [] ! q ) || ( ! q U ( q && <> p -> ( ! p U ( s && ! p && X ( ! p U t ) ) ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "After Q", 'size' : 6})
pattern.append({'ltl' : "[] ( ( q && <> r ) -> ( ! p U ( r || ( s && ! p && X ( ! p U t ) ) ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "Between Q and R", 'size' : 5})
pattern.append({'ltl' : "[] ( q -> ( <> p -> ( ! p U ( r || ( s && ! p && X ( ! p U t ) ) ) ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "After Q until R", 'size' : 4})

pattern.append({'ltl' : "( <> ( s && X <> t ) ) -> ( ( ! s ) U p ) )", 'ptype' : "Precedence Chain", 'mtype' : "Globally", 'size' : 4})
pattern.append({'ltl' : "<> r -> ( ( ! ( s && ( ! r ) && X ( ! r U ( t && ! r ) ) ) ) U ( r || p ) )", 'ptype' : "Precedence Chain", 'mtype' : "Before R", 'size' : 4})
pattern.append({'ltl' : "( [] ! q ) || ( ( ! q ) U ( q && ( ( <> ( s && X <> t ) ) -> ( ( ! s ) U p ) ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "After Q", 'size' : 6})
pattern.append({'ltl' : "[] ( ( q && <> r ) -> ( ( ! ( s && ( ! r ) && X ( ! r U ( t && ! r ) ) ) ) U ( r || p ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "Between Q and R", 'size' : 5})
pattern.append({'ltl' : "[] ( q -> ( ! ( s && ( ! r ) && X ( ! r U ( t && ! r ) ) ) U ( r || p ) || [] ( ! ( s && X <> t ) ) ) )", 'ptype' : "Precedence Chain", 'mtype' : "After Q until R", 'size' : 5})

pattern.append({'ltl' : "[] ( s && X <> t -> X ( <> ( t && <> p ) ) )", 'ptype' : "Response Chain", 'mtype' : "Globally", 'size' : 6})
pattern.append({'ltl' : "<> r -> ( s && X ( ! r U t ) -> X ( ! r U ( t && <> p ) ) ) U r", 'ptype' : "Response Chain", 'mtype' : "Before R", 'size' : 7})
pattern.append({'ltl' : "[] ( q -> [] ( s && X <> t -> X ( ! t U ( t && <> p ) ) ) )", 'ptype' : "Response Chain", 'mtype' : "After Q", 'size' : 6})
pattern.append({'ltl' : "[] ( ( q && <> r ) -> ( s && X ( ! r U t ) -> X ( ! r U ( t && <> p ) ) ) U r )", 'ptype' : "Response Chain", 'mtype' : "Between Q and R", 'size' : 8})
pattern.append({'ltl' : "[] ( q -> ( s && X ( ! r U t ) -> X ( ! r U ( t && <> p ) ) ) U ( r || [] ( s && X ( ! r U r ) -> X ( ! r U ( t && <> p ) ) ) ) )", 'ptype' : "Response Chain", 'mtype' : "After Q until R", 'size' : 13})

pattern.append({'ltl' : "[] ( p -> <> ( s && X <> t ) )", 'ptype' : "Response Chain", 'mtype' : "Globally", 'size' : 4})
pattern.append({'ltl' : "<> r -> ( p -> ( ! r U ( s && ! r && X ( ! r U t ) ) ) ) U r", 'ptype' : "Response Chain", 'mtype' : "Before R", 'size' : 5})
pattern.append({'ltl' : "[] ( q -> [] ( p -> ( s && X <> t ) ) )", 'ptype' : "Response Chain", 'mtype' : "After Q", 'size' : 3})
pattern.append({'ltl' : "[] ( ( q && <> r ) -> ( p -> ( ! r U ( s && ! r && X ( ! r U t ) ) ) ) U r )", 'ptype' : "Response Chain", 'mtype' : "Between Q and R", 'size' : 6})
pattern.append({'ltl' : "[] ( q -> ( p -> ( ! r U ( s && ! r && X ( ! r U t ) ) ) ) U ( r || [] ( p -> ( s && X <> t ) ) ) )", 'ptype' : "Response Chain", 'mtype' : "After Q until R", 'size' : 8})

pattern.append({'ltl' : "[] ( p -> <> ( s && ! z && X ( ! z U t ) ) )", 'ptype' : "Constrained Chain", 'mtype' : "Globally", 'size' : 4})
pattern.append({'ltl' : "<> r -> ( p -> ( ! r U ( s && ! r && ! z && X ( ( ! r && ! z ) U t ) ) ) ) U r", 'ptype' : "Constrained Chain", 'mtype' : "Before R", 'size' : 5})
pattern.append({'ltl' : "[] ( q -> [] ( p -> ( s && ! z && X ( ! z U t ) ) ) )", 'ptype' : "Constrained Chain", 'mtype' : "After Q", 'size' : 4})
pattern.append({'ltl' : "[] ( ( q && <> r ) -> ( p -> ( ! r U ( s && ! r && ! z && X ( ( ! r && ! z ) U t ) ) ) ) U r )", 'ptype' : "Constrained Chain", 'mtype' : "Between Q and R", 'size' : 6})
pattern.append({'ltl' : "[] ( q -> ( p -> ( ! r U ( s && ! r && ! z && X ( ( ! r && ! z ) U t ) ) ) ) U ( r || [] ( p -> ( s && ! z && X ( ! z U t ) ) ) ) )", 'ptype' : "Constrained Chain", 'mtype' : "After Q until R", 'size' : 8})

pattern.append({'ltl' : "<> ( a && b )", 'ptype' : "Test", 'mtype' : "Test", 'size' : 1})

def getAllPattern():
	return pattern;

def getAllPatternByType(ptype):
	res = list()
	for patt in pattern:
		if(patt['ptype'] == ptype):
			res.append(patt)
	return res

def getAllPatternBySize(size):
	res = list()
	for patt in pattern:
		if(patt['size'] == size):
			res.append(patt)
	return res

def getPattern():
	n = random.randint(0, len(pattern))
	return pattern[n];

def getPatternByType(mtype):
	res = list()
	for patt in pattern:
		if(patt['ptype'] == ptype):
			res.append(patt)
	n = random.randint(0, len(res))
	return res[n]

def getPatternBySize(size):
	res = list()
	for patt in pattern:
		if(patt['size'] == size):
			res.append(patt)
	n = random.randint(0, len(res))
	return res[n]

def createFile(formula, fileName):
	cwd = os.getcwd()
	os.chdir(cwd + "/ltl3tools-0.0.8")
	s = subprocess.getstatusoutput("./ltl2mon \"" + formula + "\"")
	os.chdir(cwd)

	file = open(fileName, "w")
	for line in s:
		if(line != 0):
			file.write(line)
	file.close()

if __name__ == "__main__":
	if(len(sys.argv) == 3 and sys.argv[1].isnumeric()):
		patt = getAllPattern()
		ltl = patt[int(sys.argv[1])]
		print(ltl['ltl'])
		createFile(str(ltl['ltl']), sys.argv[2])
	elif(len(sys.argv) == 3 and not(sys.argv[1].isnumeric())):
		print(sys.argv[1])
		createFile(str(sys.argv[1]), sys.argv[2])
	else:
		print("Not a valid argument")
		print("Valid Arguments:")
		print("<int> fileName \t <int>-th pattern ltl to be stored in fileName")
		print("\"ltl\" fileName \t to produce the mentioned valid ltl in fileName")