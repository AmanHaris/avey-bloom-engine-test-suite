# Avey Bloom Engine Test Suite
This tool is meant to help with rapid testing and iteration through ideas for the avey bloom engine in a de-coupled and easy-to-use manner. Furthermore, it is designed to easily select through different options for the testing (testing through all claims, random sampling, etc.) and automatically produce reports that present all meaningful statistical analyses.

## How to test

- Tweak algorithm code **only** in the files PLE.py/MUE.py/PPV.py
- Run run.py for the tests, using options to select which claimsets to use, how to sample, which functions to test (PLE/MUE/PPV), and so on (see options section)
- Results will be versioned and stored in the Results directory

## How to run

**Step 1:** Activate the venv

Create a virtual environment (if it is initial setup):

```
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv venv
```

Activate venv (always):

```
source ./venv/bin/activate
```

**Step 2:** install any dependencies

```
pip3 install -r requirements.txt
```

**Step 3:** run run.py

Default:
```
python3 run.py
```

With options:
```
python3 run.py -c Seib -f PLE --sampling ALL
```

## Options

If no options are provided, the default behavior is to test through all available claim sets available, sampling all the claims, and running all the functions (PLE, MUE, PPV).

- -c for claimset. At the moment, only Seib is available
- -f for function. At the moment, only PLE is available
- --sampling for how the claimset is sampled. At the moment, only ALL is available
