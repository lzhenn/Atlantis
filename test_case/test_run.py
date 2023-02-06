import sys
CWD=sys.path[0]
sys.path.append(CWD+'/../')

from Atlantis import pipeline

pipeline.waterfall()
