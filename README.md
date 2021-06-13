## Microapi
Django app that handles requests to your python code

### Example
Assuming we want to create a service for a catch-the-flag game,
using which players can check the correctness of a flag, we should create
new API endpoint in ```Microapi``` app and choose "raw text" mode for it.

Assuming that our flag is 'secret-key' we can write the following code
```python3
# if `storage` is None, then it will be initialized with return value of `init`
def init():
    return 'secret-key'

# return value if `response` will be returned directly to user
# it will be encoded into json if `response` returns dict
def response(request, storage):
    if storage == '':
        return 'flag is caught by another player'
    if request == storage:
        return 'you caught the flag, send it to administrator'
    else:
        return 'incorrect flag'

# return value of this function will update existing storage value
def update(request, storage):
    if storage == '' or request != storage:
        return storage
    else:
        return ''

# if log returns not a None value, then Microapi will add it to logs
def log(request, storage):
    if storage != '' and request == storage:
        return 'flag is caught!'
```

### Web Interface snippets
- [Dashboard](https://netpipe.herokuapp.com/aRNiIhBIpmw=1b)
- [API details](https://netpipe.herokuapp.com/btcx_QcAOLM=19)

### Notes
User defined code is being evaluated using [Restricted Python](https://pypi.org/project/RestrictedPython/)
