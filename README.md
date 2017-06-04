# MindGoWrapper
Some wrapper for sh*t quant platform MindGo.

## Usage

Reset kernel every time before running.

### Cell 0

```shell
!git clone https://github.com/Jamesits/MindGoWrapper.git
!sh -c "cd MindGoWrapper; git pull"
```

### Cell 1

```
%load_ext backtest
```

### Cell 2

```python
%%backtest --start 2015-9-1 --end 2015-10-1 --capital-base 100000 --data-frequency minute --output -

import logging
logging.basicConfig(level=logging.INFO)

def execfile(file):
    exec(open(file).read(), globals())
    
execfile('MindGoWrapper/wrapper_takeown.py')
```
