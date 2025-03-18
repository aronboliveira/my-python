import os
from datetime import datetime
def generate_tags(dirc, doc_restric = False, remove_underscore = False):
  start = datetime.now()
  print('Starting writing of the html file...')
  js = []
  css = []
  for r, _, fs in os.walk(dirc):
    for f in fs:
      if f.endswith('.js'):
        js.append(os.path.join(r, f))
      elif f.endswith('.css'):
        css.append(os.path.join(r, f))
  html = '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n'
  try:
    for c in css:
      basename = os.path.splitext(os.path.basename(c))[0]
      if (remove_underscore) and basename.startswith('_'):
        basename = basename[1:]
      link = f'<link rel="stylesheet" href="{os.path.relpath(c, dirc).replace("\\", "/")}" id="{basename}" class="next-css-chunk" />\n'
      if (doc_restric):
        if ((os.path.relpath(c, dirc).startswith('docs/')) or (os.path.relpath(c, dirc).startswith('docs\\'))):
          html += link
      else:
        html += link
  except Exception as e:
      print(f'Error generating link tags: {e}')
  html += "</head>\n<body>\n"
  order = [
        "webpack",
        "polyfills",
        "buildManifest",
        "ssgManifest",
        "framework",
        "layout",
        "main",
        "main-app",
        "app",
        "page",
        "23",
        "475",
        "7ce798d6",
        "859",
        "fd9d1056",
        "error"
    ]
  js.sort(key=lambda js_path: next((i for i, k in enumerate(order) if os.path.splitext(os.path.basename(js_path))[0].lstrip('_').startswith(k)), len(order)))
  try:
    for j in js:
      basename = os.path.splitext(os.path.basename(c))[0]
      if (remove_underscore) and basename.startswith('_'):
        basename = basename[1:]      
      script = f'<script {'defer' if not (basename.startswith('webpack') or basename.startswith('polyfills') or basename.startswith('buildManifest') or basename.startswith('ssgManifest') or basename.startswith('framework-') or basename.startswith('layout-') or basename.startswith('main-') or basename.startswith('app-')) else ''} type="text/javascript" cross-origin="anonymous" referrerpolicy="strict-origin-when-cross-origin" src="{os.path.relpath(j, dirc).replace("\\", "/")}" id="{basename}" class="next-js-chunk"></script>\n'
      if (doc_restric):
        if ((os.path.relpath(c, dirc).startswith('docs/')) or (os.path.relpath(c, dirc).startswith('docs\\'))):
          html += script
      else:
        html += script
  except Exception as e:
    print(f'Error generating script tags: ${e}')
  html += '</body>\n</html>'
  outp = os.path.join(dirc, 'output.html')
  with open(outp, 'w') as file:
    file.write(html)
  finish = datetime.now()
  print(f'Writing of html file finished in {finish - start}')
generate_tags(os.getcwd(), True)
