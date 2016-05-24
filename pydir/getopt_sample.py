import getopt, sys

def usage():
    print 'getopt_sample.py shows how to use the getopt package to set run-time options'
    print 'Usage: python getopt_sample.py [options]'
    print '   -h, --help      : this message'
    print '   -a, --opt_a     = option a [1]'
    print '   -b, --opt_b     = option b [1.e10]'
    print '   -c, --opt_c     = option c [foo.txt]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:b:c:', \
              ['help','opt_a','opt_b=','opt_c='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

# Note these inputs should match usage entries above
    opt_a  = 1
    opt_b  = 1.e10
    opt_c  = 'foo.txt'

    chopt    = ''
    for o, a in opts:
        chopt += o+a
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-a', '--opt_a'):
            opt_a = int(a)
        elif o in ('-b', '--opt_b'):
            opt_b = float(a)
        elif o in ('-c', '--opt_c'):
            opt_c = a
        else:
            assert False, 'unhandled option'

#   print out options
    print 'Option a =', opt_a
    print 'Option b =', opt_b
    print 'Option c =', opt_c
            
if __name__=='__main__':main()



