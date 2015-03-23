#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   count-names.py
   
   Descp: Count and display files with same names in a specific path or in all the filesystem.
   
   Created on: 17-mar-2015
   
   Copyright 2015 Abel Serrano Juste <abeserra@ucm.es>
"""

import sys, getopt
import os                                                                                           
from collections import defaultdict

filesBlackList = []
dirsBlackList = []
tableFiles = None
tableDirs = None

def readBlackList(blackListPath):
  bl_f = open(blackListPath,'rU')
  for l in bl_f:
    l = l.rstrip()
    if (l == '' or l[1:2]=='//'): #files starting with // are comments
      continue
    elif (l[-1] == '/'):
      dirsBlackList.append(l[:-1])
    else:
      filesBlackList.append(l)
  return

def count_in_dir(path,type_to_count):
  global tableFiles, tableDirs
  for dirpath, dirs, files in os.walk(path):
    #print dirpath
    #print dirs
    #print files
    files = [f for f in files if not f[0] == '.' and not f in filesBlackList]
    dirs[:] = [d for d in dirs if (not d[0] == '.' and not d in dirsBlackList) ]
    
    if (type_to_count in ['f','a']):
      for name in files:
        #print name
        tableFiles[name].append(os.path.join(dirpath, name))
    
    if (type_to_count in ['d','a']):
      for name in dirs:
        #print name
        tableDirs[name].append(os.path.join(dirpath, name))

  return

def count_only_a_name_in_dir(path,one_name,type_to_count):
  global tableFiles, tableDirs
  for dirpath, dirs, files in os.walk(path):
    #print dirpath
    #print dirs
    #print files
    
    files = [f for f in files if not f[0] == '.' and not f in filesBlackList]
    dirs[:] = [d for d in dirs if (not d[0] == '.' and not d in dirsBlackList) ]
    
    #counting a file
    if (type_to_count in ['f','a'] and files):
      name = files[0]
      while files and (name != one_name):
        name = files[0]
        files = files[1:]
      if name == one_name:
        tableFiles.append(os.path.join(dirpath, name))
        
    #counting a dir
    if (type_to_count in ['d','a'] and dirs):
      name = dirs[0]
      while dirs and (name != one_name):
        name = dirs[0]
        dirs = dirs[1:]
      if name == one_name:
        tableDirs.append(os.path.join(dirpath, name))

  return

def print_table(table,path):
  count = 0
  for name in table.keys():
    times = len(table[name])

    if times > 1:
      print "name '%s' is repeated %d times" % (name, times)
      for ocurrence in table[name]:
        print "\t", ocurrence 
      count += 1
  
  print count,'files with the same name found in', path
  
def print_list(table,name):
  times = len(table)
  print "name '%s' is repeated %d times" % (name, times)
  for ocurrence in table:
    print "\t", ocurrence   

def usage():
  print "python count_names.py [-p path] [-n 'one name'] [-l 'blacklist file'] [-t 'a/d/f']"

def main():
  
  #parsing args
  try:
    (opts, args) = getopt.getopt(sys.argv[1:], "hp:n:l:t:", ["help", "path","name","black-list","type"])
  except getopt.GetoptError as err:
      # print help information and exit:
      print str(err) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
    
  # Init void values for options
  path = '/'
  one_name = None
  blackListPath = ''
  type_to_count = 'f'
  
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-p", "--path"):
      path = a
    elif o in ("-n", "--name"):
      one_name = a
    elif o in ("-l", "--black-list"):
      blackListPath = a
    elif o in ("-t", "--type"):
      type_to_count = a
    else:
      assert False, "unhandled option"
  
  #declare some variables
  global tableFiles, tableDirs
  if blackListPath :
    readBlackList(blackListPath)
  
   #count going over the filesystem
  print 'Processing filesystem, this can take a while...'
 
  if one_name:
    tableFiles = []
    tableDirs = []
    table = count_only_a_name_in_dir(path,one_name,type_to_count)
    print '----->DONE!!!!<-----'
    if (type_to_count in ['f','a']):
      print '==Results for processing files=='
      print_list(tableFiles,one_name)
    if (type_to_count in ['d','a']):
      print '==Results for processing dirs=='
      print_list(tableDirs,one_name)
     
  else:
    tableFiles = defaultdict(list)
    tableDirs = defaultdict(list)
    count_in_dir(path,type_to_count)
    print '----->DONE!!!!<-----'
    if (type_to_count in ['f','a']):
      print '==Results for processing files=='
      print_table(tableFiles,path)
    if (type_to_count in ['d','a']):
      print '==Results for processing dirs=='
      print_table(tableDirs,path)
  
  return 0

if __name__ == '__main__':
  main()
