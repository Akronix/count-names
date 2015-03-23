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

blackList = []

def readBlackList(blackListPath):
  bl_f = open(blackListPath,'rU')
  for l in bl_f:
    blackList.append(l.rstrip())
  return blackList

def count_in_dir(table,path):
  for dirpath, dirs, files in os.walk(path):
    #print dirpath
    #print dirs
    #print files
    
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if (not d[0] == '.' and not d in blackList) ]
    
    for name in files:
      #print name
      table[name].append(os.path.join(dirpath, name))
      
def count_only_a_name_in_dir(table,path,file_name):
  for dirpath, dirs, files in os.walk(path):
    #print dirpath
    #print dirs
    #print files
    
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if (not d[0] == '.' and not d in blackList) ]
    
    for name in files:
      if (name == file_name):
        table[name].append(os.path.join(dirpath, name))

def usage():
  print "python count_names.py [-p path] [-f 'file name'] [-b 'blacklist file']"

def main():
  
  #parsing args
  try:
    (opts, args) = getopt.getopt(sys.argv[1:], "hp:f:l:", ["help", "path","file-name","black-list"])
  except getopt.GetoptError as err:
      # print help information and exit:
      print str(err) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
    
  # Init void values for options
  path = '/'
  file_name = None
  blackListPath = ''
  
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-p", "--path"):
      path = a
    elif o in ("-f", "--file-name"):
      file_name = a
    elif o in ("-l", "--black-list"):
      blackListPath = a
    else:
      assert False, "unhandled option"
  
  #init variables
  table = defaultdict(list)
  
  if blackListPath :
    blackList = readBlackList(blackListPath)
  
  print 'Processing filesystem, this can take a while...'
  #count going over the filesystem
  if not file_name:
    count_in_dir(table,path)
  else:
    count_only_a_name_in_dir(table,path,file_name)
  
  print '----->DONE!!!!<-----'
  #output
  count = 0
  for name in table.keys():
    times = len(table[name])
    if times > 1:
      print 'name:', name, 'is repeated:', times, 'times.'
      for ocurrence in table[name]:
        print "\t", ocurrence 
      count += 1
  
  print count,'files with the same name in', path 
  return 0

if __name__ == '__main__':
  main()
