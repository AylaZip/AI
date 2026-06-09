# Lab 7 — Probability

## Opgave 1 — To medicinske tests

| | Test A | Test B |
|---|---|---|
| Sensitivitet P(+|V) | 95% | 90% |
| Falsk positiv P(+|¬V) | 10% | 5% |

P(V) = 0.01, P(¬V) = 0.99

**Bayes' theorem:** `P(V|+) = P(+|V)·P(V) / P(+)`

### Test A
```
P(+) = P(+|V)·P(V) + P(+|¬V)·P(¬V)
     = 0.95·0.01 + 0.10·0.99
     = 0.0095 + 0.0990
     = 0.1085

P(V|+) = 0.0095 / 0.1085 ≈ 0.0876 = 8.76%
```

### Test B
```
P(+) = 0.90·0.01 + 0.05·0.99
     = 0.0090 + 0.0495
     = 0.0585

P(V|+) = 0.0090 / 0.0585 ≈ 0.1538 = 15.38%
```

**Svar:** Test B er mest indikativ. Selvom Test A har højere sensitivitet (95% vs 90%),
opvejes det af Test B's lavere falsk positive rate (5% vs 10%), hvilket giver en højere
posterior sandsynlighed P(V|+).

---

## Opgave 2 — Sjælden sygdom

P(D) = 1/10000 = 0.0001
P(+|D) = 0.99
P(-|¬D) = 0.99 → P(+|¬D) = 0.01

```
P(+) = 0.99·0.0001 + 0.01·0.9999
     = 0.000099 + 0.009999
     = 0.010098

P(D|+) = 0.000099 / 0.010098 ≈ 0.0098 = 0.98%
```

**Svar:** Det er godt at sygdommen er sjælden, fordi selv med 99% test-nøjagtighed
kommer langt de fleste positive resultater fra falske positiver. 1% falsk positiv rate
af 99,99% raske giver ~9999 gange flere falske positiver end sande positiver.
Chancen for rent faktisk at have sygdommen efter en positiv test er kun **~0,98%**.

---

## Opgave 3 — P(A)=0.4, P(B)=0.3, P(A∨B)=0.5

P(A∨B) = P(A) + P(B) - P(A∧B)

```
P(A∧B) = 0.4 + 0.3 - 0.5 = 0.2
```

Muligt interval for P(A∧B): [max(0, P(A)+P(B)-1), min(P(A), P(B))] = **[0, 0.3]**

0.2 ∈ [0, 0.3] → **Ja, det er rationelt.**

Agenten kan med rimelighed tro at A og B overlapper med sandsynlighed 0.2.

---

## Opgave 4 — P(A)=0.4, P(B)=0.3, P(A∨B)=0.7

```
P(A∧B) = 0.4 + 0.3 - 0.7 = 0
```

P(A∧B) = 0 betyder at A og B er **disjunkte (mutually exclusive)** — de kan ikke
ske samtidigt. **Ja, det er rationelt**, hvis agenten tror at A og B udelukker hinanden.

---

## Opgave 5 — Joint distribution

### Tabel

| toothache | cavity | catch | P |
|-----------|--------|-------|---|
| T | T | T | 0.108 |
| T | T | F | 0.012 |
| T | F | T | 0.016 |
| T | F | F | 0.064 |
| F | T | T | 0.072 |
| F | T | F | 0.008 |
| F | F | T | 0.144 |
| F | F | F | 0.576 |

Total: 0.108+0.012+0.016+0.064+0.072+0.008+0.144+0.576 = **1.0** ✓

### Beregninger

**P(toothache)**
```
= 0.108 + 0.012 + 0.016 + 0.064 = 0.2
```

**P(cavity)**
```
= 0.108 + 0.012 + 0.072 + 0.008 = 0.2
```

**P(toothache ∧ cavity)**
```
= 0.108 + 0.012 = 0.12
```

**P(toothache ∨ cavity)**
```
= P(toothache) + P(cavity) - P(toothache ∧ cavity)
= 0.2 + 0.2 - 0.12 = 0.28
```

**P(toothache | cavity)**
```
= P(toothache ∧ cavity) / P(cavity)
= 0.12 / 0.2 = 0.6
```

**P(cavity | toothache, catch)**
```
= P(cavity ∧ toothache ∧ catch) / P(toothache ∧ catch)
= 0.108 / (0.108 + 0.016)
= 0.108 / 0.124 ≈ 0.871
```

**P(toothache | cavity, catch)**
```
= P(toothache ∧ cavity ∧ catch) / P(cavity ∧ catch)
= 0.108 / (0.108 + 0.072)
= 0.108 / 0.18 = 0.6
```

### Conditional independence

P(toothache | cavity, catch) = **0.6**
P(toothache | cavity) = **0.6**

Da P(toothache | cavity, catch) = P(toothache | cavity), er **toothache conditionally
independent af catch givet cavity.**

**Hvad betyder det?** Når man allerede ved at der er et hul (cavity), giver det
ingen ekstra information om toothache-sandsynligheden at kende catch-status.
Kendskab til cavity "forklarer" sammenhængen mellem toothache og catch.

**Conditional independence** betyder at to hændelser A og B er uafhængige givet en
tredje hændelse C: P(A | B, C) = P(A | C). Når C er kendt, giver B ingen ekstra
information om A.
