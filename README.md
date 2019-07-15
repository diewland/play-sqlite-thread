# play-sqlite-thread
Play python sqlite interface with muti-requests at the same time

### Situation
Execute 15 statements from loop in the same second.

### all-in-one.py
Stateless concept. opencnx/execute/commit/closecnx in same block. Repeat all steps in every request.
```
"1"	"thread-00"	"0"	"2019-07-15 18:07:46.427818"
"2"	"thread-01"	"1"	"2019-07-15 18:07:46.438567"
"3"	"thread-05"	"2"	"2019-07-15 18:07:46.452521"
"4"	"thread-10"	"3"	"2019-07-15 18:07:46.465197"
"5"	"thread-06"	"3"	"2019-07-15 18:07:46.468432"
"6"	"thread-13"	"4"	"2019-07-15 18:07:46.481496"
"7"	"thread-07"	"2"	"2019-07-15 18:07:46.452521"
"8"	"thread-11"	"4"	"2019-07-15 18:07:46.480924"
"9"	"thread-09"	"3"	"2019-07-15 18:07:46.465197"
"10"	"thread-08"	"4"	"2019-07-15 18:07:46.479840"
"11"	"thread-02"	"2"	"2019-07-15 18:07:46.452521"
"12"	"thread-03"	"2"	"2019-07-15 18:07:46.456293"
"13"	"thread-04"	"2"	"2019-07-15 18:07:46.452521"
"14"	"thread-12"	"4"	"2019-07-15 18:07:46.482552"
"15"	"thread-14"	"4"	"2019-07-15 18:07:46.479840"
```
ps. id, task, records, ts

### multithreadok.py
Queue concept. Open connection in queue thread. when you need to do something, put some execution to queue.
```
"1"	"thread-00"	"0"	"2019-07-15, 18:07:41.480171"
"2"	"thread-01"	"0"	"2019-07-15, 18:07:41.480698"
"3"	"thread-02"	"0"	"2019-07-15, 18:07:41.481247"
"4"	"thread-03"	"0"	"2019-07-15, 18:07:41.481768"
"5"	"thread-04"	"0"	"2019-07-15, 18:07:41.482297"
"6"	"thread-05"	"0"	"2019-07-15, 18:07:41.482806"
"7"	"thread-06"	"0"	"2019-07-15, 18:07:41.482829"
"8"	"thread-07"	"0"	"2019-07-15, 18:07:41.483350"
"9"	"thread-08"	"0"	"2019-07-15, 18:07:41.483350"
"10"	"thread-09"	"0"	"2019-07-15, 18:07:41.483879"
"11"	"thread-10"	"0"	"2019-07-15, 18:07:41.484411"
"12"	"thread-11"	"0"	"2019-07-15, 18:07:41.484939"
"13"	"thread-12"	"0"	"2019-07-15, 18:07:41.485497"
"14"	"thread-13"	"0"	"2019-07-15, 18:07:41.486033"
"15"	"thread-14"	"0"	"2019-07-15, 18:07:41.486033"
```
ps. id, task, records, ts

### Addition Library
apsw -- for multithreadok.py
```
pip install https://github.com/rogerbinns/apsw/releases/download/3.28.0-r1/apsw-3.28.0-r1.zip --global-option=fetch --global-option=--version --global-option=3.28.0 --global-option=--all --global-option=build --global-option=--enable-all-extensions
```

### References
* https://docs.python.org/2/library/sqlite3.html
* https://realpython.com/intro-to-python-threading/
* https://stackoverflow.com/a/6717275/466693
* https://stackoverflow.com/a/1830499/466693
* https://code.activestate.com/recipes/526618/
