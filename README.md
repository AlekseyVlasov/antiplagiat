# Antiplagiat script

Script for comparing two python files on the subject of cheating. Made as a part of selection test 
for ML course conducted by 'Tinkoff'.

## Installation

Clone the repo

## Usage

```bash
python3 compare.py input.txt scores.txt
```
where input.txt has form:

```text
files/main.py plagiat1/main.py
files/loss.py plagiat2/loss.py
files/loss.py files/loss.py
```
files to compare in pairs.

scores.txt is the file for the answers:
```text
0.63
0.84
0.153
```