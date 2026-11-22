# Independent reviewer findings (address every item)

The one-line fix in toc.py treats a valueless or empty id as missing, so the heading gets a generated id. The change is minimal, tests pass, and a changelog entry is included.


