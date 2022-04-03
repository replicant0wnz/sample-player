#!/usr/bin/python3

import mido
import mpv
import yaml

# Read config
config = open('sampler.yaml')
config_yaml = yaml.load(config)

# Make checking events a tad cleaner
def check_event(event, note=0, velocity=0):
    event_string = "note_on channel=0 note=%s velocity=%s time=0" % (note, velocity)
    if str(event) == event_string:
        return True
    else:
        return None

# Get config
inport = mido.open_input(config_yaml['device'])
player = {} 

# Iterate over midi events
for x in inport:
    for sample in config_yaml['samples']:
        sample_name = sample['name']
        # Create player for sample if it doesn't exist
        if sample_name not in player:
            player[sample_name] = mpv.MPV(ytdl=True)
        # Play sample
        if check_event(x, note=sample['note'], velocity=127):
            player[sample_name].play(sample['file'])
            print("On  : " + sample['description'] )
        # Stop sample
        if check_event(x, note=sample['note'], velocity=0):
            player[sample_name].terminate()
            del player[sample_name] 
            print("Off : " + sample['description'] )
