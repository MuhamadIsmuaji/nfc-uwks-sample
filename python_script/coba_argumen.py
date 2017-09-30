import sys
import json as simplejson

data = simplejson.dumps({"Param 1" : sys.argv[1], "Param 2" : sys.argv[2]})

print data
