# Integrational tests for interpretation system

These tests include various scenarios for personal account and Atlas Pro interpretation.

The repo has the following structure:

```plain
.
├── README.md
├── cases
│   ├── genetics
│   │   └── genetics*.production.test.yml
│   ├── genetics_and_questionnaire
│   │   ├── genetics-and-questionnaire*.rawdata.rsid.test.txt
│   │   └── genetics-and-questionnaire*.test.yml
│   ├── haplogroups
│   │   ├── haplogroups*.rawdata.rsid.test.txt
│   │   └── haplogroups*.test.yml
│   ├── pharmacogenetics
│   │   └── pharmacogenetics*.test.yml
│   ├── questionnaire
│   │   ├── questionnaire*.rawdata.rsid.test.txt // Empty SNP files because only questionnaire is available
│   │   └── questionnaire*.test.yml
│   └── recommendations
│       └── recommendations*.test.yml
├── results
└── support
    └── genetics_and_questionnaire
```

- `cases` — all the test cases;
  - `genetics` — genetics only tests;
  - `genetics_and_questionnaire` — the most integrational tests;
  - `haplogroups` — tests for haplogroups calculation algorythm;
  - `pharmacogenetics` — tests for PGx after haplotype calculation. Haplotype calculation tests are in [diplotype-combinatorial-tests repo](https://git.abg.ltd/analytical-dept/diplotype/diplotype-combinatorial-tests);
  - `questionnaire` — test users which have only questionnaire;
- `results` — directory for test results; is under gitignore;
- `support` — directory with support files and tools for the test cases. Must have the same structure as the `cases` dyrectory.
