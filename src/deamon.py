import daemon

from data_scrubber import main 

with daemon.DaemonContext():
  main()
