import yapdi 

from scrubber import main 

if __name__ == "__main__":
  daemon = yapdi.Daemon()
  daemon.daemonize()
  main()
