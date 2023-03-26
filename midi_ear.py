import argparse
import pretty_midi
import random
import sys

# args: formula_len, num_bars_between_notes

PARSER = argparse.ArgumentParser(
    prog='midi_ear',
    description='Generate MIDI files for ear training along with An Improviser\'s OS')

PARSER.add_argument('-f', '--formula',
                    help='Length of the formula (from 2 to 12)',
                    choices=range(2, 13),
                    type=int,
                    required=True)
PARSER.add_argument('-b', '--bars',
                    help='Number of bars of 4 before the next note',
                    default=4,
                    type=int)
PARSER.add_argument('-r', '--random',
                    help='Randomize the order of the notes',
                    action='store_true')

ARGS = PARSER.parse_args()

KEYS = {'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
        'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
        'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
        'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
        'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
        'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
        'F#': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
        'Db': ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
        'Ab': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
        'Eb': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
        'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
        'F': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']}

FUNCTIONS = ['b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7']

# randomly pick a formula of the given length

FORMULA = random.sample(FUNCTIONS, ARGS.formula - 1)
FORMULA_SORTED = ['1'] + [f for f in FUNCTIONS if f in FORMULA]

KEY_NOTES = random.choice(list(KEYS.values()))

CHOSEN_NOTES = []

for func in FORMULA_SORTED:
    func_num_only = int(func[-1])
    note_in_question = KEY_NOTES[func_num_only - 1]
    if 'b' in func:
        if 'b' in note_in_question:
            idx_of_prev_note = KEY_NOTES.index(note_in_question) - 1
            CHOSEN_NOTES.append(KEY_NOTES[idx_of_prev_note])
        elif '#' in note_in_question:
            CHOSEN_NOTES.append(note_in_question[0])
        else:
            CHOSEN_NOTES.append(note_in_question + 'b')
    else:
        CHOSEN_NOTES.append(note_in_question)

CHOSEN_NOTES_IN_OCT = [note + '5' for note in CHOSEN_NOTES]

if ARGS.random:
    random.shuffle(CHOSEN_NOTES_IN_OCT)

MIDI_OBJ = pretty_midi.PrettyMIDI(initial_tempo=60.0)
PIANO_PROG = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
INSTRUMENT = pretty_midi.Instrument(program=PIANO_PROG)

NOTE_START_TIME = 0

for note_name in CHOSEN_NOTES_IN_OCT:
    note_number = pretty_midi.note_name_to_number(note_name)
    note = pretty_midi.Note(velocity=100,
                            pitch=note_number,
                            start=NOTE_START_TIME,
                            end=NOTE_START_TIME+4)
    INSTRUMENT.notes.append(note)
    NOTE_START_TIME += (ARGS.bars * 4)

# append rest after the last note to fill out the bar
REST_NOTE_NUMBER = pretty_midi.note_name_to_number(CHOSEN_NOTES_IN_OCT[0])
REST_NOTE = pretty_midi.Note(velocity=0,
                             pitch=REST_NOTE_NUMBER,
                             start=NOTE_START_TIME-1,
                             end=NOTE_START_TIME)
INSTRUMENT.notes.append(REST_NOTE)
    
MIDI_OBJ.instruments.append(INSTRUMENT)
FILENAME = 'formula_in_' + CHOSEN_NOTES[0] + '.mid'
MIDI_OBJ.write(FILENAME)
