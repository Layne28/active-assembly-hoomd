import gsd.hoomd
import sys

def main():
    trajname = sys.argv[1]

    traj = gsd.hoomd.open(trajname)
    trajlen = traj.__len__()
    print(trajlen)
    
    #if trajlen==4000:
    #    print(1)
    #    return 1
    #else:
    #    #print('not finished')
    #    print(0)
    #    return 0

main()
