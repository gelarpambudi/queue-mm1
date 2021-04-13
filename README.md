# M/M/1 QUEUE SIMULATION

### Requirements
* pip
  ```sh
    pip install numpy pandas
  ```

### Usage
* Help Menu
   ```sh
    python mm1.py --help
    usage: mm1.py [-h] [--num_experiment NUM_EXPERIMENT] [--out OUT]
              [--lamda LAMDA] [--miu MIU] [--duration DURATION]

    M/M/1 Queue Simulation

    optional arguments:
    -h, --help            show this help message and exit
    --num_experiment NUM_EXPERIMENT
                            Number of experiment
    --out OUT             output file (*.xlsx)
    --lamda LAMDA         arrival rate
    --miu MIU             service rate
    --duration DURATION   simulation duration (in minutes)
   ```

* How to run
   ```sh
    python mm1.py <arguments>
   ```

### Reference
[@Simulating a Queueing System in Python](https://towardsdatascience.com/simulating-a-queuing-system-in-python-8a7d1151d485)

