#!/usr/bin/env python
import argparse
from collections import defaultdict
import fnmatch
import json
import os
import sys

import re


def analyze_hangman_log(data):
    game_log = data['log']
    return {
        'turns': len(game_log),
        'reward': sum([1 for t in game_log if t['result'] != '!']),
        'pain': sum([1 for t in game_log if t['result'] == '!']),
    }


def _get_percents(response):
    if len(response) > 4:  # TODO: Fix this - will need to pass in codeword length
        raise RuntimeError('Mastermind codeword of length 4 is only supported')
    result = 0.0
    for character in response:
        if character == 'B':
            result += 0.33333
        elif character == 'W':
            result += 0.33333/2.0
        else:
            raise ValueError('Response must only include "B" or "W"')
    return result


def analyze_mastermind_log(data):
    game_log = data['log']
    return {
        'turns': len(game_log),
        'reward': sum([_get_percents(t['result']) for t in game_log]),
        'pain': sum([1.0-_get_percents(t['result']) for t in game_log]),
    }

def analyze_game_log(data):
    if data['game'] == 'hangman':
        return analyze_hangman_log(data)
    elif data['game'] == 'mastermind': # TODO: Build mastermind analyzer
        return analyze_mastermind_log(data)
    else:
        raise RuntimeError('Unrecognized game {}'.format(data['game']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-directory')
    parser.add_argument('--out-file', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    games = defaultdict(list)

    for root, dirnames, filenames in os.walk(args.input_directory):
        for filename in fnmatch.filter(filenames, '*.jsonl'):
            filepath = os.path.join(root, filename)
            print(filepath, file=sys.stderr)
            with open(filepath) as f:
                for line in f:
                    # line = re.sub("'", '"', line.strip())
                    data = json.loads(line)
                    game_key = (
                        data['game'],
                        data['strategy']['model'],
                        (
                            data['strategy']['foci']['reward'],
                            data['strategy']['foci']['info'],
                            data['strategy']['foci']['speed'],
                        )
                    )

                    analysis = analyze_game_log(data)
                    games[game_key].append(analysis)

    aggregates = {}
    for game_key, analyses in games.items():
        average_turns = sum([a['turns'] for a in analyses])/len(analyses)
        average_reward = sum([a['reward'] for a in analyses]) / len(analyses)
        average_pain = sum([a['pain'] for a in analyses]) / len(analyses)
        stats = {
            'average_turns': average_turns,
            'average_reward': average_reward,
            'average_pain': average_pain,
        }
        aggregates[game_key] = stats

    for game_key, stats in aggregates.items():
        print(json.dumps({'game_key': game_key, 'stats': stats}), file=args.out_file)
