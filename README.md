# VFrame
_VFrame_ is a method for constraining possible verbal frames based on the verbal particle and the infinitival argument of Hungarian verbs. A detailed description of the _VFrame_ algorithm can be found in English in _Indig & Vadász 2016_ (see bibliographical data at the end of the this README).

## Structure
- the main folder contains 3 scripts, these must be executed in the following order:
  - *preprocess_input_for_magyarlanc.py*: it preprocesses the test file to the [magyarlanc dependency parser](http://www.inf.u-szeged.hu/rgai/magyarlanc) (after that, the _magyarlanc_ system must be used with the *temp/to_magyarlanc* input, resulting in the *temp/to_magyarlanc_out*)
  - *annotate.py*: it runs _VFrame_ searcher
  - *eval.py*: it evaluates the results of _VFrame_ searcher
- the *temp* folder stores temporal data produced by the 3 scripts
- the *manocska* folder contains data coming from the [_Manócska_](https://github.com/ppke-nlpg/manocska) database
- the *test_data* folder contains the test set (*final_test.txt*) and the gold standard (*only_manually_annotated.txt*)

## Evaluation
Our test set (*test_data/final_test.txt*) contains 1000 clauses extracted from the Hungarian Gigaword Corpus 2.0.4. The clauses are selected according to the following criteria:

- the clause has to contain exactly one finite verb,
- in addition to this, it must have at least one verbal particle OR an infinitive,
- the finite as well as the infinite verb can be a particle verb (thus, they particle is written together with the verb).

### 'Verbal particle (PRT) - finite verb (FIN) - infinite verb (INF)' combinations with their frequencies and original examples in Hungarian:
clauses containing a detached verbal particle:
- detached PRT & no INF: 573
  - e.g. _de az élmény csak ideig-óráig villanyozta(FIN) fel(PRT)._
- detached PRT & INF without PRT: 65
  - e.g. _a köztes állásokat ki(PRT) kell(FIN) következtetni(INF) a szomszédosakból,_
- detached PRT & INF with PRT: 3
  - e.g. _Egycsatáros játékkal próbált(FIN) meg(PRT) sikert elérni(PRT+INF) a Celtic Milánóban,_

clauses NOT containing any detached verbal particles:
- FIN without PRT & INF without PRT: 225
  - e.g. _az alkotmányt is módosítani(INF) kellene(FIN),_
- FIN without PRT & INF with PRT: 120
  - e.g. _Nem tudtam(FIN) megítélni(PRT+INF),_
- FIN with PRT & INF without PRT: 10
  - e.g. _hogy elkezdtünk(PRT+FIN) gondolkozni(INF)_
- FIN with PRT & INF with PRT: 4
  - e.g. _és az egyikbe tényleg megpróbál(PRT+FIN) több utast beültetni(PRT+INF) a droszton sürgölődő hosztesz._

## References used in the README:
- Indig, Balázs – Vadász, Noémi (2016): _Windows in Human Parsing -- How Far can a Preverb Go?_ Tenth International Conference on Natural Language Processing (HrTAL2016), Dubrovnik, Croatia, September 29--30, 2016.
- [Hungarian Gigaword Corpus (Magyar Nemzeti Szövegtár 2)](http://clara.nytud.hu/mnsz2-dev/)
- Oravecz, Csaba – Váradi, Tamás – Sass, Bálint (2014):
[_The Hungarian Gigaword Corpus._](http://www.lrec-conf.org/proceedings/lrec2014/pdf/681_Paper.pdf) In: Proceedings of LREC 2014. Reykjavík. 1719–1723.
- Zsibrita, János – Vincze, Veronika – Farkas, Richárd (2013):
_magyarlanc: A Toolkit for Morphological and Dependency Parsing of Hungarian._ In: Proceedings of RANLP 2013, pp. 763–771.

# Licence
It can be used for education, research and private projects. In case you use _VFrame_, please cite one of the following articles:

Vadász Noémi, Kalivoda Ágnes, Indig Balázs. _Egy egységesített magyar igei vonzatkerettár építése és felhasználása._ XIV. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2018). 3--15. Szeged. 2018.

    @inproceedings{vadasz_kalivoda_indig_2018a,
        title = {Egy egys{\'e}ges{\'i}tett magyar igei vonzatkerett{\'a}r {\'e}p{\'i}t{\'e}se {\'e}s felhaszn{\'a}l{\'a}sa},
        booktitle = {XIV. Magyar Sz{\'a}m{\'i}t{\'o}g{\'e}pes Nyelv{\'e}szeti Konferencia (MSZNY 2018)},
        year = {2018},
        pages = {3{\textendash}15},
        publisher={Szegedi Tudom{\'a}nyegyetem Informatikai Tansz{\'e}kcsoport},
        organization = {Szegedi Tudom{\'a}nyegyetem Informatikai Int{\'e}zet},
        address = {Szeged},
        author = {Vad{\'a}sz, No{\'e}mi and Kalivoda, {\'A}gnes and Indig, Bal{\'a}zs},
        editor = {Vincze, Veronika}
    }

Indig, Balázs and Vadász, Noémi. _Windows in Human Parsing -- How Far can a Preverb Go?_ Tenth International Conference on Natural Language Processing (HrTAL2016), Dubrovnik, Croatia, September 29--30, 2016.

    @conference {indig_vadasz_2016b,
        title = {Windows in Human Parsing {\textendash} How Far can a Preverb Go?},
        booktitle = {Tenth International Conference on Natural Language Processing (HrTAL2016) 2016, Dubrovnik, Croatia, September 29-30, 2016, Proceedings},
        year = {2016},
        note = {to appear},
        publisher = {Springer},
        organization = {Springer},
        address = {Cham},
        keywords = {indba, vadno},
        author = {Indig, Bal{\'a}zs and Vad{\'a}sz, No{\'e}mi},
        editor = {Tadi{\'c}, Marko and Bekavac, Bo{\.z}o}
    }
