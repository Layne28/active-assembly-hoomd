import gsd.hoomd
import sys

def main():
    trajname = sys.argv[1]

    traj = gsd.hoomd.open(trajname)
    trajlen = traj.__len__()
    
    if trajlen==4000:
        return 1
    else:
        return 0

main()
