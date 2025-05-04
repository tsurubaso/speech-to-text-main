import os

try:
    pipe = open(r'//./pipe/FromSrvPipe', 'r') #pipe = open(r'//./pipe/ToSrvPipe', 'r')
    print("✅ Pipe is open and accessible.")
    pipe.close()
except Exception as e:
    print(f"❌ Failed to open pipe: {e}")
