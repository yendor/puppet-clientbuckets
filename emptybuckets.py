#!/usr/bin/env python

import getopt, sys, os, re, time
import traceback

class EmptyBuckets:
    def __init__(self):
        self.output_filename = ""
        self.bucketdir = "/var/lib/puppet/clientbucket"
        self.verbose = True

        self.files = {}
        self.pattern = None
        shortargs = 'b:'
        longargs = ['bucketdir=']

        options, self.pattern = getopt.getopt(sys.argv[1:], shortargs, longargs)

        for opt, arg in options:
            if opt in ('-b', '--bucketdir'):
                self.bucketdir = os.path.abspath(arg)
        
        if len(self.pattern) != 1:
            print >> sys.stderr, "You must specify a single substring pattern of file paths in the file bucket to delete"
            sys.exit(1)
        
        self.search()
    
    def search(self):
        full_path = os.path.abspath(self.bucketdir)
        if os.path.exists(full_path):
            self.walk(full_path)
        else:
            print >> sys.stderr, "WARNING: The path %s does not exist" % (full_path)
    
    def walk(self, start):
        try:
            if os.path.isdir(start) and not os.path.islink(start):
                for name in os.listdir(start):
                    path = os.path.join(start,name)       
                    if os.path.isfile(path):
                        if name == "paths" and self.paths_contain_pattern(path):
                            # print "Removing %s, %s and %s" % (path, os.path.join(start, "contents"), start)
                            os.unlink(path)
                            os.unlink(os.path.join(start, "contents"))
                            os.rmdir(start)
                            return
                    elif os.path.isdir(path) and not os.path.islink(path):
                        self.walk(path)
        except OSError:
            traceback.print_exc(file=sys.stdout)
            
    def paths_contain_pattern(self, pathsfile):
        f = open(pathsfile, 'r')
        for line in f:
            if self.pattern[0] in line:
                return True
        return False
        
            
    def cleanup(self, bucket):
        print "rm -rf %s" % (bucket)

if __name__ == "__main__":
    s = EmptyBuckets()
