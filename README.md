# Mustang-Gold-Slot-Simulator

A Python-based simulator for the Mustang Gold slot machine game. This tool performs statistical analysis of the game's RTP (Return to Player), hit rates, and other metrics through Monte Carlo simulations.

## Features

- Simulates base game, free spins, and bonus games
- Calculates RTP for different game modes
- Provides hit rate statistics
- Supports configurable number of simulations
- Includes profiling for performance analysis

## Requirements

- Python 3.6+
- numpy
- pandas
- tqdm

## Installation

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulator with default settings (10 million simulations):
```bash
python Main.py
```

Run with custom number of simulations:
```bash
# 1,000 simulations
python Main.py -l1000

# 1,000,000 simulations
python Main.py -l1000k

# 10,000,000 simulations
python Main.py -l10m
```

Additional options:
- `-verbose`: Show detailed progress during simulation
- `-indata`: Print input data structures for verification
- `-h` or `-help`: Show help information

## Output

The simulator outputs:
- RTP (Return to Player) statistics
- Hit rates for base game, free spins, and bonus games
- Frequency of free spin triggers and retriggers
- Performance profiling information

## Files

- `Main.py`: Main simulation script
- `base.csv`: Reel configuration for base game
- `free.csv`: Reel configuration for free spins
- `LICENSE`: GPL v3 license
- `requirements.txt`: Python dependencies

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Author

Todor Balabanov (todor.balabanov@gmail.com)
Velbazhd Software LLC (http://veldsoft.eu/)
