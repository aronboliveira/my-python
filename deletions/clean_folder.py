import os
import time
from datetime import datetime, timedelta
limit = datetime.now() - timedelta(days=30)
def clean_folder() -> None:
  cwd = os.getcwd()
  script = os.path.basename(__file__)
  for r, ds, fs in os.walk(cwd, topdown=False, followlinks=False):
    for f in fs:
      if f == script:
        continue
      fpath = os.path.join(r, f)
      if os.path.isfile(fpath) and datetime.fromtimestamp(os.path.getmtime(fpath)) < limit:
          try:
            os.remove(fpath)
          except Exception:
            pass
    for d in ds:
      dpath = os.path.join(r, d)
      if os.path.isdir(dpath) and datetime.fromtimestamp(os.path.getmtime(dpath)) < limit:
        try:
          os.rmdir(dpath)
        except Exception:
          pass
if __name__ == '__main__':
  while True:
    clean_folder()
    time.sleep(2592000)