# midi_ear
Generate MIDI files for ear training along with Wayne Krantz's An Improviser's OS

This script creates a MIDI file in a random key with a user-defined number of notes to work with. By default, a new note is presented to the ear every 4 bars. All of this is operating within 4/4 for now.

To better understand the approach behind formulas as applied to keys in Western tonality, please check out [An Improviser's OS](https://waynekrantz.bandcamp.com/merch/wayne-krantz-an-improvisers-os-2nd-edition).

## Setup
```
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Usage
Run the script, then import the MIDI file into your favorite DAW.

```
options:
  -h, --help            show this help message and exit
  -f {2,3,4,5,6,7,8,9,10,11,12}, --formula {2,3,4,5,6,7,8,9,10,11,12}
                        Length of the formula (from 2 to 12)
  -b BARS, --bars BARS  Number of bars of 4 before the next note
  -r, --random          Randomize the order of the notes
```

## Examples
```
# generate a midi file with a 3-note formula
python midi_ear.py -f 5
# generate a midi file with an 8-note formula, randomizing their order
python midi_ear.py -f 8 -r
# do the same thing but play a new note every 2 bars
python midi_ear.py -f 8 -b 2 -r
```
