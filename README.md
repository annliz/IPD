# IPD Online (but not online)

Usable interface for running and testing code for the Iterated Prisoner's Dilemma game :)

# Get Started

1. **Download code.** Clone the repository:
    ```bash
    git clone https://github.com/annliz/IPD
    ```

2. **Get spreadsheet API key.** For security reasons, the API key is not included in the Github repository. *You need this key to run the code*. Contact Annli for the key. Then, download this file and move it into the folder `ipd_local`. Make sure it is still named `service_account.json`.

3. **Install poetry.** This project uses the Python dependency manager `poetry`, which you can install with:
    ```
    pip3 install poetry
    export PATH=$PATH:~/.local/bin
    ```

4. **Get access to submission and results spreadsheets.** This is where students submit their code, and where result are logged. Ask Annli for access to the Google sheets.

# Running a Simulation

1. **Navigate to folder.** In your terminal, navigate to the folder `ipd_local` to run the simulation on your machine.

2. **Specify game parameters.** Edit the file `game_specs.py` to change game parameters such as noise level and score matrix.

3. **Run the game.** Run the actual simulation:
    ```bash
    poetry shell # to enter the environment
    python3 main.py
    ```

4. **View results.** View the results of the game at the results spreadsheet that has been shared with you. This sheet only saves the results of the latest run, so if you want to save these results permanently, create a copy.

5. **Read error log.** All submissions that had issues of any sort are logged in `ipd.log`. Make sure to read this file and notify students of their issues so they can fix their code.


# ipd_local Details

Currently, this folder contains the main utility of this project. `ipd_local` allows the user to run the IPD locally. Within this folder, `ipd_local` contains the code that runs the actual game, while `tests` contains all tests for the code.

## Simulation code

To run the game, the user runs `main.py`. The following files in the subfolder `ipd_local` are then called on to run the simulation:

- `game_specs.py`: The user can modify this file in order to change the specifications of the game, such as number of rounds, noise level, etc.

- `default_functions.py`: Stores a set of default IPD strategies as functions that can be included in the game.

- `get_inputs.py`: Retrieves all student code submissions from Google sheets, filters them for errors, and formats them to be used in the simulation.

- `simulation.py`: Runs the actual simulation of the IPD, using the inputted functions and game specs. Outputs the raw data of the game results to local files `latest_raw_out.json` and `latest_specs.json`.

- `data_analysis.py`: Takes the raw results of the game, calculates player scores and rankings, and updates the IPD results spreadsheet with the information.

## Tests

All the tests for the simulation are located in the `tests` subfolder. Integration tests are run in `integration_test.py`, while the rest of the files contain unit tests.

To run a specific test, navigate to the `tests` folder and run the following command:
```bash
poetry shell
pytest TESTFILENAME
```
To run all tests, run:
```bash
poetry shell
pytest
```

# Future Features and Bugs

Future work on this project can be split into three categories: improvements for the current system, new features for the current system, and completely new systems.

## Improvements for current system

1. **Security.** The top priority feature to fix. Currently, the simulation processes student code by simply executing it blind. This obviously is unideal as students can theoretically submit anything into their pastebin files, allowing them to potentially tamper with the simulation or with the user's machine. As such, future work on this project should consider sandboxing student functions such that it cannot interact with the rest of the environment.

2. **Efficiency.** From quantumish: "I optimized the simulation step by using a thread pool to play matchups in parallel (which itself was hacky as it necessitated stripping functions down to bytecode when sending them across threads and reassembling them on the other end). Despite using 16 threads for the pool, the sim only ran about 2x faster, so there's likely a lot of overhead that can be reduced after some profiling/investigation. On top of that, the same strategy functions are run a lot, and so JIT compiling them either implicitly via PyPy or explicitly using Numba could probably net some speedups (although they didn't have much of an effect in initial tests)."

## New features for current system

1. **Input/output UI.** Currently, the user specifies game parameters by editing a small python file, `game_specs.py`, and all problems are logged simply to a file, `ipd.log`. This is functional but slightly scuffed. A simple UI could make this process more streamlined.

2. **Specific search.** The results of the latest game are stored locally in `latest_raw_out.json`, including the series of plays for each matchup. These moves are omitted when the scores are logged onto the spreadsheet, for volume reasons. However, it may potentially be of interest to view the results of a specific matchup, for which a simple searching function may be helpful.

3. **Write functions easier.** Create some sort of tutorial or scaffolding to aid students who are inexperienced in writing Python code. Perhaps even allow them to follow simple templates.

## Entirely new systems

1. **Website.** The folder `ipd-online` is the initial attempt at being able to run the IPD online. The advantages of this would be the user not having to download and install various packages, as well as presumably better UI. However, there is no clean way to be able to run Python code on the browser, thus this idea was paused.

2. **Distributed simulation.** Idea courtesy of zbuster05. Running hundreds of rounds of games for each matchup between hundreds of different functions takes a while. In order to speed up the process, we could potentially distribute the running of the simulation across machines, such that the rounds one student's functions plays are run on their specific device, then having them all send their results to a central location. This idea will make the simulation faster, but is much more complicated to implement and control.