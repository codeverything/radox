from signal import signal, SIGINT
import simple_colors
import sys

def handler(sig, frame):
   sys.exit(0)

def info():
   signal(SIGINT, handler)
   print("Compiled Successfully   "+simple_colors.green("DONE"))
   print("Your Project is ready and serving now")
   print(simple_colors.red("WARNING!! This is a Development server don't use it on production"))
   print(" -> Running server at http://127.0.0.1:3301")
   print(" -> Press Ctrl+C to exit")
