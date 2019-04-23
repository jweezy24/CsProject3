import sys
import os

os.system('export PYTHONPATH="$PYTHONPATH:$HOME/.python"')

sys.path.append("./server")
sys.path.append("./pong")
sys.path.append("./tests")

os.system("python3 ./server/serverMain.py")
