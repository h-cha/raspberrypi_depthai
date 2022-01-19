import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('compare_distance',type=float, help="Perform tracking on full RGB frame", default=1)
    parser.add_argument('dangerous_distance', type=int, help="Perform tracking on full RGB frame", default=1)
    parser.add_argument('-ff', '--full_frame', action="store_true", help="Perform tracking on full RGB frame", default=False)
    parser.add_argument('-tp', '--tracking_target_person', action="store_true", help="Perform tracking person", default=False)

    return parser.parse_args()