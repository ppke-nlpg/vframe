# VFrame
A method for constraining possible verbal frames based on the verbal particle and the infinitival argument of Hungarian verbs.

(a detailed description comes here)

## Evaluation
Our test set (test_data/final_test.txt) contains 1000 clauses extracted from HGC 2.0.4. The clauses are selected according to the following criteria:
- the clause has to contain exactly one finite verb,
- in addition to this, it must have at least one verbal particle OR an infinitive,
- the finite as well as the infinite verb can be a particle verb (thus, they particle is written together with the verb).

### 'Verbal particle (PRT) - finite verb (FIN) - infinite verb (INF)' combinations with their frequencies and original examples in Hungarian:
clauses containing a detached verbal particle:
- detached PRT & no INF: 573

        e.g. de az élmény csak ideig-óráig villanyozta(FIN) fel(PRT).
- detached PRT & INF without PRT: 65

        e.g. a köztes állásokat ki(PRT) kell(FIN) következtetni(INF) a szomszédosakból,
- detached PRT & INF with PRT: 3

        e.g. Egycsatáros játékkal próbált(FIN) meg(PRT) sikert elérni(PRT+INF) a Celtic Milánóban,

clauses NOT containing any detached verbal particles:
- FIN without PRT & INF without PRT: 225

        e.g. az alkotmányt is módosítani(INF) kellene(FIN),
- FIN without PRT & INF with PRT: 120

        e.g. Nem tudtam(FIN) megítélni(PRT+INF),
- FIN with PRT & INF without PRT: 10

        e.g. hogy elkezdtünk(PRT+FIN) gondolkozni(INF)
- FIN with PRT & INF with PRT: 4

        e.g. és az egyikbe tényleg megpróbál(PRT+FIN) több utast beültetni(PRT+INF) a droszton sürgölődő hosztesz.
