## Hangman strategies in python

Until I get a proper README up, check out the following the lightning talk for a quick overview:

<a href="https://www.youtube.com/watch?v=dSSNLyaZBUU">
<img src="https://cloud.githubusercontent.com/assets/4130/2675446/19b8c5ee-c119-11e3-9dac-7a2f40ce0453.png"/>
</a>

## Setup

Set up a virtual environment and activate it

```
python3.5 -mvenv ~/venv/hangman
source ~/venv/hangman/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Prepare `./build/` with processed dictionary files

```
make split
```

## Running Different Strategies


#### Random

```
time cat build/splits/9 | python play.py - --config games/01-random.cfg --reset-memory --limit 25011
```

```
Average Score:  15.4326896166 22.1743632802

real	12m42.964s
user	12m42.115s
sys	0m0.870s
```

#### Naive

```
time cat build/splits/9 | python play.py - --config games/02-naive.cfg --reset-memory --limit 25011
```


```
Average Score:  9.28483467274 16.3595218104

real	14m58.874s
user	14m57.871s
sys	0m1.049s
```

#### Feedback Distinct

```
time cat build/splits/9 | python play.py - --config games/03-feedback-distinct.cfg --reset-memory --limit 25011
```

```
Average Score:  7.02450921594 14.1903562433

real	13m47.919s
user	13m47.074s
sys	0m0.877s
```

#### Feedback Positional

```
time cat build/splits/9 | python play.py - --config games/05-feedback-positional.cfg --reset-memory --limit 25011
```

```
Average Score:  1.40973971453 5.97277198033

real	1m29.261s
user	1m29.064s
sys	0m0.201s
```

#### Maximize Information

```
time cat build/splits/9 | python play.py - --config games/06-entropy-mismatched-scorers.cfg --reset-memory --limit 25011
```

```
Average Score:  1.66422773979 5.09367878134

real	1m29.895s
user	1m29.674s
sys	0m0.227s
```

#### Optimize

```
time cat build/splits/9 | python play.py - --config games/07-entropy-same-scorer.cfg --reset-memory --limit 25011
```

```
Average Score:  1.38179201151 5.37903322538

real	1m28.110s
user	1m27.906s
sys	0m0.209s
```
