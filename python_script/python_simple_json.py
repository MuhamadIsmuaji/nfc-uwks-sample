#import simplejson
import json as simplejson

def main():
    data = simplejson.dumps({"tests": "35"})
    print data
main()
# 

# import sys

# def do_some(a):
#     print 'test1'
#     time.sleep(30)
#     print 'test2'

# if __name__ == '__main__':
#     print 'Now the python scritp running'
#     time.sleep(20)
#     a = sys.argv[1]
#     if a:
#     print 'Now print something'
#     T = do_some(a)