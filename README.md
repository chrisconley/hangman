#### Random

```
time cat build/splits/9 | python2.7 bits.py - --config games/01-random.cfg --reset-memory --limit 25011
```

```
Average Score:  15.4326896166 22.1743632802

real	12m42.964s
user	12m42.115s
sys	0m0.870s
```

#### Naive

```
time cat build/splits/9 | python2.7 bits.py - --config games/02-naive.cfg --reset-memory --limit 25011
```


```
Average Score:  9.28483467274 16.3595218104

real	14m58.874s
user	14m57.871s
sys	0m1.049s
```

#### Feedback Distinct

```
time cat build/splits/9 | python2.7 bits.py - --config games/03-feedback-distinct.cfg --reset-memory --limit 25011
```

```
```

#### Feedback Positional

```
time cat build/splits/9 | python2.7 bits.py - --config games/05-feedback-positional.cfg --reset-memory --limit 25011
```

```
Average Score:  1.40973971453 5.97277198033

real	1m29.261s
user	1m29.064s
sys	0m0.201s
```

#### Maximize Information

```
time cat build/splits/9 | python2.7 bits.py - --config games/06-entropy-mismatched-scorers.cfg --reset-memory --limit 25011
```

```
Average Score:  1.66422773979 5.09367878134

real	1m29.895s
user	1m29.674s
sys	0m0.227s
```

#### Optimize

```
time cat build/splits/9 | python2.7 bits.py - --config games/07-entropy-same-scorer.cfg --reset-memory --limit 25011
```

```
Average Score:  1.38179201151 5.37903322538

real	1m28.110s
user	1m27.906s
sys	0m0.209s
```
