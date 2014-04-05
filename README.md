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
