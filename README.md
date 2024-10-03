# Layered CA/Browser Forum requirements

## Introduction

The tools in this directory help to convert the existing documents in to a structured repository, it's the intention that we start working on the structured repository and only build the final documents.

The advantage of this setup is that you will no longer have to work with extremely large files and that it could help us to move to a BR of BR's section by section with minimal bootstrapping work.

The baseline requirements (BR) are incorporated unless the target document type includes a file for the same section with a weight of 000.

In following example each target document BR, CS, SMIME defines it's own introduction, when building the target document only one of these documents will be included:

```sh
000_BR_INTRODUCTION.md
000_CS_INTRODUCTION.md
000_SMIME_INTRODUCTION.md
```

If the weight of the CS and/or SMIME was different, like 001 in the example below, both the BR and the CS or SMIME introduction would be included if the target was CS or SMIME:

```sh
000_BR_INTRODUCTION.md
001_CS_INTRODUCTION.md
001_SMIME_INTRODUCTION.md
```

## Reserved layers

To facilitate special formatting of certain layers the following layers are reserved for a specific purpose.

| Layer   | Description                   |
| :------ | :---------------------------- |
| 800-899 | Auditors and Assessors        |
| 900-999 | CA Control Statements, CP/CPS |

## Usage

Transform documents:

```sh
py transform.py ../docs/BR.md
py transform.py ../docs/CS.md
py transform.py ../docs/SMIME.md
```

Remove duplicates:

```sh
py duplicates.py
```

Build documents and requirement sheets:

```sh
py build.py BR
py build.py CS
py build.py SMIME
```

Build documents and requirement sheets including only the following Level of Assurance (LoA):

```sh
py build.py BR --loa OV
py build.py BR --loa DV OV EV
```

Build documents and exclude a layer or range of layers from the build:

```sh
py build.py BR --exclude-layers 800
py build.py BR --exclude-layers 800 801 802
py build.py BR --exclude-layers 800-999
py build.py BR --exclude-layers 800-810 820-830
```

Create a HTML view:

```sh
py tohtml.py -out ../public/
```

## Requirements

In each document you can specify a requirement, this would work following:

```md
    [001] This is an example requirement
```

This requirement will be extracted an included in the matrix as:

```csv
"ID","Section","LoA","Type","Requirement"
BR-1.3.1-001, 1.3.1, EV, BR, This is an example requirement
```

## Frontmatter

When building the target document, frontmatter information is considered, the frontmatter itself is not included in the output except for the main 000_XXX.md files.

Currently the following options can be configured.

### Level of Assurance (LoA)

The system is currently recognizing the following levels of assurance:

1. DV
2. OV
3. EV

The LoA of a specific section can be indicated within the frontmatter of the document:

```md
---
loa: DV
---

Content here
```

It's assumed that OV requirements build on top of the DV requirements, and EV of DV and OV, etc. This is however currently not enforced by the build system. Meaning that you will need to specify DV, OV, EV if you want to include requirements for all three.

### Including and excluding specific targets

With the following frontmatter the file will be ignored when building the SMIME documents.

```md
---
targets:
    excluded:
        - SMIME
---

Content here
```

To only include this file in the SMIME documents, the following frontmatter can be used to only include this file in the SMIME documents.

```md
---
targets:
    included:
        - SMIME
---

Content here
```

## Duplicate sections

The tool duplicates.py compares sections from different documents and automatically deletes duplicates to ensure that modifications in the baseline requirements wil automatically be adopted in the relying document.

The following sections have been identified as equal, the corresponding CS and SMIME files have been deleted.

| Section | Type  | Similarity (%) | Differences |
| :------ | :---: | -------------: | :---------: |
| 1       |  CS   |          100.0 |             |
| 1       |  EVG  |           1.34 |             |
| 1       | SMIME |          100.0 |             |
| 1.1     |  CS   |           2.02 |             |
| 1.1     |  EVG  |            3.2 |             |
| 1.1     | SMIME |          11.06 |             |
| 1.2     |  CS   |           23.0 |             |
| 1.2     |  EVG  |           8.95 |             |
| 1.2     | SMIME |           28.7 |             |
| 1.2.1   |  CS   |           4.43 |             |
| 1.2.1   |  EVG  |           3.49 |             |
| 1.2.1   | SMIME |           0.76 |             |
| 1.2.2   |  CS   |           2.99 |             |
| 1.3     |  CS   |          19.49 |             |
| 1.3     |  EVG  |          19.49 |             |
| 1.3     | SMIME |          67.06 |             |
| 1.3.1   |  CS   |          26.73 |             |
| 1.3.1   |  EVG  |          26.73 |             |
| 1.3.1   | SMIME |          94.79 |             |
| 1.3.2   |  CS   |           2.59 |             |
| 1.3.2   |  EVG  |           6.16 |             |
| 1.3.2   | SMIME |          58.58 |             |
| 1.3.3   |  CS   |          42.25 |             |
| 1.3.3   |  EVG  |          42.25 |             |
| 1.3.3   | SMIME |          100.0 |             |
| 1.3.4   |  CS   |          15.32 |             |
| 1.3.4   |  EVG  |          15.32 |             |
| 1.3.4   | SMIME |           82.1 |             |
| 1.3.5   |  CS   |          13.88 |             |
| 1.3.5   |  EVG  |          13.88 |             |
| 1.3.5   | SMIME |          85.54 |             |
| 1.4     |  CS   |          100.0 |             |
| 1.4     |  EVG  |          100.0 |             |
| 1.4     | SMIME |           9.32 |             |
| 1.4.1   |  CS   |          86.89 |             |
| 1.4.1   |  EVG  |          40.47 |             |
| 1.4.1   | SMIME |          24.59 |             |
| 1.4.2   |  CS   |          100.0 |             |
| 1.4.2   |  EVG  |           9.72 |             |
| 1.4.2   | SMIME |          100.0 |             |
| 1.5     |  CS   |          98.16 |             |
| 1.5     |  EVG  |           6.69 |             |
| 1.5     | SMIME |           6.84 |             |
| 1.5.1   |  CS   |          100.0 |             |
| 1.5.1   |  EVG  |          100.0 |             |
| 1.5.1   | SMIME |          100.0 |             |
| 1.5.2   |  CS   |          100.0 |             |
| 1.5.2   |  EVG  |          12.41 |             |
| 1.5.2   | SMIME |          66.26 |             |
| 1.5.3   |  CS   |          100.0 |             |
| 1.5.3   |  EVG  |          100.0 |             |
| 1.5.3   | SMIME |          100.0 |             |
| 1.5.4   |  CS   |          100.0 |             |
| 1.5.4   |  EVG  |          100.0 |             |
| 1.5.4   | SMIME |          100.0 |             |
| 1.6     |  CS   |          100.0 |             |
| 1.6     |  EVG  |          25.35 |             |
| 1.6     | SMIME |          89.64 |             |
| 1.6.1   |  CS   |          16.39 |             |
| 1.6.1   |  EVG  |           1.51 |             |
| 1.6.1   | SMIME |          38.12 |             |
| 1.6.2   |  CS   |          32.67 |             |
| 1.6.2   |  EVG  |            3.2 |             |
| 1.6.2   | SMIME |          17.56 |             |
| 1.6.3   |  CS   |           68.0 |             |
| 1.6.3   |  EVG  |           3.66 |             |
| 1.6.3   | SMIME |          27.67 |             |
| 1.6.4   |  CS   |          78.59 |             |
| 1.6.4   |  EVG  |          74.52 |             |
| 1.6.4   | SMIME |          40.39 |             |
| 2       |  CS   |          100.0 |             |
| 2       |  EVG  |          17.97 |             |
| 2       | SMIME |           30.2 |             |
| 2.1     |  CS   |          62.63 |             |
| 2.1     |  EVG  |          17.65 |             |
| 2.1     | SMIME |          99.04 |             |
| 2.2     |  CS   |          14.16 |             |
| 2.2     |  EVG  |          33.24 |             |
| 2.2     | SMIME |          28.53 |             |
| 2.3     |  CS   |          100.0 |             |
| 2.3     |  EVG  |          15.42 |             |
| 2.3     | SMIME |          61.81 |             |
| 2.4     |  CS   |          100.0 |             |
| 2.4     |  EVG  |          47.89 |             |
| 2.4     | SMIME |          100.0 |             |
| 3       |  CS   |          100.0 |             |
| 3       |  EVG  |          100.0 |             |
| 3       | SMIME |          100.0 |             |
| 3.1     |  CS   |          100.0 |             |
| 3.1     |  EVG  |          100.0 |             |
| 3.1     | SMIME |          100.0 |             |
| 3.1.1   |  CS   |          100.0 |             |
| 3.1.1   |  EVG  |          100.0 |             |
| 3.1.1   | SMIME |           5.26 |             |
| 3.1.2   |  CS   |          100.0 |             |
| 3.1.2   |  EVG  |          100.0 |             |
| 3.1.2   | SMIME |          32.56 |             |
| 3.1.3   |  CS   |          100.0 |             |
| 3.1.3   |  EVG  |          100.0 |             |
| 3.1.3   | SMIME |           5.19 |             |
| 3.1.4   |  CS   |          100.0 |             |
| 3.1.4   |  EVG  |          100.0 |             |
| 3.1.4   | SMIME |          100.0 |             |
| 3.1.5   |  CS   |          100.0 |             |
| 3.1.5   |  EVG  |          100.0 |             |
| 3.1.5   | SMIME |          100.0 |             |
| 3.1.6   |  CS   |          100.0 |             |
| 3.1.6   |  EVG  |          100.0 |             |
| 3.1.6   | SMIME |          100.0 |             |
| 3.2     |  CS   |          100.0 |             |
| 3.2     |  EVG  |          100.0 |             |
| 3.2     | SMIME |           6.75 |             |
| 3.2.1   |  CS   |          100.0 |             |
| 3.2.1   |  EVG  |          100.0 |             |
| 3.2.1   | SMIME |          100.0 |             |
| 3.2.2   |  CS   |          32.14 |             |
| 3.2.2   |  EVG  |           8.61 |             |
| 3.2.2   | SMIME |           3.07 |             |
| 3.2.2.1 |  CS   |          11.42 |             |
| 3.2.2.1 |  EVG  |           1.27 |             |
| 3.2.2.1 | SMIME |           1.85 |             |
| 3.2.2.2 |  CS   |          12.76 |             |
| 3.2.2.2 |  EVG  |           1.13 |             |
| 3.2.2.2 | SMIME |           4.53 |             |
| 3.2.2.3 |  EVG  |           2.63 |             |
| 3.2.2.3 | SMIME |           6.05 |             |
| 3.2.2.4 |  EVG  |           1.43 |             |
| 3.2.2.4 | SMIME |           2.71 |             |
| 3.2.2.5 |  EVG  |           2.31 |             |
| 3.2.2.6 |  EVG  |           0.92 |             |
| 3.2.2.7 |  EVG  |           3.19 |             |
| 3.2.2.8 |  EVG  |           1.28 |             |
| 3.2.3   |  CS   |          22.01 |             |
| 3.2.3   |  EVG  |           8.22 |             |
| 3.2.3   | SMIME |          18.92 |             |
| 3.2.4   |  CS   |          100.0 |             |
| 3.2.4   |  EVG  |          100.0 |             |
| 3.2.4   | SMIME |           1.96 |             |
| 3.2.5   |  CS   |          99.92 |             |
| 3.2.5   |  EVG  |            4.4 |             |
| 3.2.5   | SMIME |          15.58 |             |
| 3.2.6   |  CS   |          10.96 |             |
| 3.2.6   |  EVG  |          18.62 |             |
| 3.2.6   | SMIME |           2.25 |             |
| 3.3     |  CS   |          100.0 |             |
| 3.3     |  EVG  |          100.0 |             |
| 3.3     | SMIME |          100.0 |             |
| 3.3.1   |  CS   |          100.0 |             |
| 3.3.1   |  EVG  |          100.0 |             |
| 3.3.1   | SMIME |          100.0 |             |
| 3.3.2   |  CS   |          100.0 |             |
| 3.3.2   |  EVG  |          100.0 |             |
| 3.3.2   | SMIME |          100.0 |             |
| 3.4     |  CS   |          100.0 |             |
| 3.4     |  EVG  |          100.0 |             |
| 3.4     | SMIME |          100.0 |             |
| 4       |  CS   |          100.0 |             |
| 4       |  EVG  |          100.0 |             |
| 4       | SMIME |          100.0 |             |
| 4.1     |  CS   |          100.0 |             |
| 4.1     |  EVG  |          100.0 |             |
| 4.1     | SMIME |          100.0 |             |
| 4.1.1   |  CS   |          25.14 |             |
| 4.1.1   |  EVG  |          33.46 |             |
| 4.1.1   | SMIME |          100.0 |             |
| 4.1.2   |  CS   |          41.29 |             |
| 4.1.2   |  EVG  |          11.02 |             |
| 4.1.2   | SMIME |          37.71 |             |
| 4.2     |  CS   |          100.0 |             |
| 4.2     |  EVG  |          100.0 |             |
| 4.2     | SMIME |          100.0 |             |
| 4.2.1   |  CS   |          25.57 |             |
| 4.2.1   |  EVG  |           4.76 |             |
| 4.2.1   | SMIME |           7.75 |             |
| 4.2.2   |  CS   |           5.96 |             |
| 4.2.2   |  EVG  |           30.9 |             |
| 4.2.2   | SMIME |           30.9 |             |
| 4.2.3   |  CS   |          100.0 |             |
| 4.2.3   |  EVG  |          100.0 |             |
| 4.2.3   | SMIME |          100.0 |             |
| 4.3     |  CS   |          100.0 |             |
| 4.3     |  EVG  |          100.0 |             |
| 4.3     | SMIME |          100.0 |             |
| 4.3.1   |  CS   |          59.36 |             |
| 4.3.1   |  EVG  |          90.24 |             |
| 4.3.1   | SMIME |          95.61 |             |
| 4.3.2   |  CS   |          100.0 |             |
| 4.3.2   |  EVG  |          100.0 |             |
| 4.3.2   | SMIME |          100.0 |             |
| 4.4     |  CS   |          100.0 |             |
| 4.4     |  EVG  |          100.0 |             |
| 4.4     | SMIME |          100.0 |             |
| 4.4.1   |  CS   |          100.0 |             |
| 4.4.1   |  EVG  |          100.0 |             |
| 4.4.1   | SMIME |          100.0 |             |
| 4.4.2   |  CS   |          100.0 |             |
| 4.4.2   |  EVG  |          100.0 |             |
| 4.4.2   | SMIME |          100.0 |             |
| 4.4.3   |  CS   |          100.0 |             |
| 4.4.3   |  EVG  |          100.0 |             |
| 4.4.3   | SMIME |          100.0 |             |
| 4.5     |  CS   |          100.0 |             |
| 4.5     |  EVG  |          100.0 |             |
| 4.5     | SMIME |          100.0 |             |
| 4.5.1   |  CS   |          100.0 |             |
| 4.5.1   |  EVG  |          55.49 |             |
| 4.5.1   | SMIME |          100.0 |             |
| 4.5.2   |  CS   |          100.0 |             |
| 4.5.2   |  EVG  |          100.0 |             |
| 4.5.2   | SMIME |          100.0 |             |
| 4.6     |  CS   |          100.0 |             |
| 4.6     |  EVG  |          100.0 |             |
| 4.6     | SMIME |          100.0 |             |
| 4.6.1   |  CS   |          100.0 |             |
| 4.6.1   |  EVG  |          100.0 |             |
| 4.6.1   | SMIME |          100.0 |             |
| 4.6.2   |  CS   |          100.0 |             |
| 4.6.2   |  EVG  |          100.0 |             |
| 4.6.2   | SMIME |          100.0 |             |
| 4.6.3   |  CS   |          100.0 |             |
| 4.6.3   |  EVG  |          100.0 |             |
| 4.6.3   | SMIME |          100.0 |             |
| 4.6.4   |  CS   |          100.0 |             |
| 4.6.4   |  EVG  |          100.0 |             |
| 4.6.4   | SMIME |          100.0 |             |
| 4.6.5   |  CS   |          100.0 |             |
| 4.6.5   |  EVG  |          100.0 |             |
| 4.6.5   | SMIME |          100.0 |             |
| 4.6.6   |  CS   |          100.0 |             |
| 4.6.6   |  EVG  |          100.0 |             |
| 4.6.6   | SMIME |          100.0 |             |
| 4.6.7   |  CS   |          100.0 |             |
| 4.6.7   |  EVG  |          100.0 |             |
| 4.6.7   | SMIME |          100.0 |             |
| 4.7     |  CS   |          100.0 |             |
| 4.7     |  EVG  |          100.0 |             |
| 4.7     | SMIME |          100.0 |             |
| 4.7.1   |  CS   |          100.0 |             |
| 4.7.1   |  EVG  |          100.0 |             |
| 4.7.1   | SMIME |          100.0 |             |
| 4.7.2   |  CS   |          100.0 |             |
| 4.7.2   |  EVG  |          100.0 |             |
| 4.7.2   | SMIME |          100.0 |             |
| 4.7.3   |  CS   |          100.0 |             |
| 4.7.3   |  EVG  |          100.0 |             |
| 4.7.3   | SMIME |          100.0 |             |
| 4.7.4   |  CS   |          100.0 |             |
| 4.7.4   |  EVG  |          100.0 |             |
| 4.7.4   | SMIME |          100.0 |             |
| 4.7.5   |  CS   |          100.0 |             |
| 4.7.5   |  EVG  |          100.0 |             |
| 4.7.5   | SMIME |          100.0 |             |
| 4.7.6   |  CS   |          100.0 |             |
| 4.7.6   |  EVG  |          100.0 |             |
| 4.7.6   | SMIME |          100.0 |             |
| 4.7.7   |  CS   |          100.0 |             |
| 4.7.7   |  EVG  |          100.0 |             |
| 4.7.7   | SMIME |          100.0 |             |
| 4.8     |  CS   |          100.0 |             |
| 4.8     |  EVG  |          100.0 |             |
| 4.8     | SMIME |          100.0 |             |
| 4.8.1   |  CS   |          100.0 |             |
| 4.8.1   |  EVG  |          100.0 |             |
| 4.8.1   | SMIME |          100.0 |             |
| 4.8.2   |  CS   |          100.0 |             |
| 4.8.2   |  EVG  |          100.0 |             |
| 4.8.2   | SMIME |          100.0 |             |
| 4.8.3   |  CS   |          100.0 |             |
| 4.8.3   |  EVG  |          100.0 |             |
| 4.8.3   | SMIME |          100.0 |             |
| 4.8.4   |  CS   |          100.0 |             |
| 4.8.4   |  EVG  |          100.0 |             |
| 4.8.4   | SMIME |          100.0 |             |
| 4.8.5   |  CS   |          100.0 |             |
| 4.8.5   |  EVG  |          100.0 |             |
| 4.8.5   | SMIME |          100.0 |             |
| 4.8.6   |  CS   |          100.0 |             |
| 4.8.6   |  EVG  |          100.0 |             |
| 4.8.6   | SMIME |          100.0 |             |
| 4.8.7   |  CS   |          100.0 |             |
| 4.8.7   |  EVG  |          100.0 |             |
| 4.8.7   | SMIME |          100.0 |             |
| 4.9     |  CS   |           16.0 |             |
| 4.9     |  EVG  |          100.0 |             |
| 4.9     | SMIME |          100.0 |             |
| 4.9.1   |  CS   |           19.1 |             |
| 4.9.1   |  EVG  |          100.0 |             |
| 4.9.1   | SMIME |          100.0 |             |
| 4.9.1.1 |  CS   |          13.62 |             |
| 4.9.1.1 | SMIME |          22.22 |             |
| 4.9.1.2 |  CS   |          99.94 |             |
| 4.9.1.2 | SMIME |          95.62 |             |
| 4.9.2   |  CS   |          13.72 |             |
| 4.9.2   |  EVG  |          18.58 |             |
| 4.9.2   | SMIME |          95.21 |             |
| 4.9.3   |  CS   |          100.0 |             |
| 4.9.3   |  EVG  |           8.85 |             |
| 4.9.3   | SMIME |          85.07 |             |
| 4.9.4   |  CS   |          100.0 |             |
| 4.9.4   |  EVG  |          100.0 |             |
| 4.9.4   | SMIME |          100.0 |             |
| 4.9.5   |  CS   |           7.02 |             |
| 4.9.5   |  EVG  |           7.84 |             |
| 4.9.5   | SMIME |          90.75 |             |
| 4.9.6   |  CS   |           10.5 |             |
| 4.9.6   |  EVG  |          30.39 |             |
| 4.9.6   | SMIME |          100.0 |             |
| 4.9.7   |  CS   |           7.29 |             |
| 4.9.7   |  EVG  |           5.82 |             |
| 4.9.7   | SMIME |           6.08 |             |
| 4.9.8   |  CS   |           80.0 |             |
| 4.9.8   |  EVG  |          100.0 |             |
| 4.9.8   | SMIME |           80.0 |             |
| 4.9.9   |  CS   |          85.86 |             |
| 4.9.9   |  EVG  |          14.08 |             |
| 4.9.9   | SMIME |          14.57 |             |
| 4.9.10  |  CS   |          28.27 |             |
| 4.9.10  |  EVG  |           2.92 |             |
| 4.9.10  | SMIME |          47.58 |             |
| 4.9.11  |  CS   |           18.3 |             |
| 4.9.11  |  EVG  |           87.3 |             |
| 4.9.11  | SMIME |           87.3 |             |
| 4.9.12  |  CS   |          100.0 |             |
| 4.9.12  |  EVG  |          65.15 |             |
| 4.9.12  | SMIME |          100.0 |             |
| 4.9.13  |  CS   |          92.66 |             |
| 4.9.13  |  EVG  |          43.14 |             |
| 4.9.13  | SMIME |          37.25 |             |
| 4.9.14  |  CS   |          100.0 |             |
| 4.9.14  |  EVG  |          79.49 |             |
| 4.9.14  | SMIME |          79.49 |             |
| 4.9.15  |  CS   |          100.0 |             |
| 4.9.15  |  EVG  |          82.22 |             |
| 4.9.15  | SMIME |          82.22 |             |
| 4.9.16  |  CS   |          100.0 |             |
| 4.9.16  |  EVG  |           80.0 |             |
| 4.9.16  | SMIME |           80.0 |             |
| 4.10    |  CS   |          100.0 |             |
| 4.10    |  EVG  |          100.0 |             |
| 4.10    | SMIME |          100.0 |             |
| 4.10.1  |  CS   |          67.28 |             |
| 4.10.1  |  EVG  |          34.59 |             |
| 4.10.1  | SMIME |          97.72 |             |
| 4.10.2  |  CS   |          47.26 |             |
| 4.10.2  |  EVG  |           7.52 |             |
| 4.10.2  | SMIME |          99.29 |             |
| 4.10.3  |  CS   |          100.0 |             |
| 4.10.3  |  EVG  |          100.0 |             |
| 4.10.3  | SMIME |          100.0 |             |
| 4.11    |  CS   |          100.0 |             |
| 4.11    |  EVG  |          100.0 |             |
| 4.11    | SMIME |          100.0 |             |
| 4.12    |  CS   |          100.0 |             |
| 4.12    |  EVG  |          100.0 |             |
| 4.12    | SMIME |          100.0 |             |
| 4.12.1  |  CS   |          100.0 |             |
| 4.12.1  |  EVG  |          100.0 |             |
| 4.12.1  | SMIME |           19.8 |             |
| 4.12.2  |  CS   |          100.0 |             |
| 4.12.2  |  EVG  |          88.89 |             |
| 4.12.2  | SMIME |          88.89 |             |
| 5       |  CS   |          98.84 |             |
| 5       |  EVG  |           1.74 |             |
| 5       | SMIME |          50.56 |             |
| 5.1     |  CS   |          81.63 |             |
| 5.1     |  EVG  |          81.63 |             |
| 5.1     | SMIME |          81.63 |             |
| 5.1.1   |  CS   |          100.0 |             |
| 5.1.1   |  EVG  |          100.0 |             |
| 5.1.1   | SMIME |          100.0 |             |
| 5.1.2   |  CS   |          100.0 |             |
| 5.1.2   |  EVG  |          100.0 |             |
| 5.1.2   | SMIME |          100.0 |             |
| 5.1.3   |  CS   |          100.0 |             |
| 5.1.3   |  EVG  |          100.0 |             |
| 5.1.3   | SMIME |          100.0 |             |
| 5.1.4   |  CS   |          100.0 |             |
| 5.1.4   |  EVG  |          100.0 |             |
| 5.1.4   | SMIME |          100.0 |             |
| 5.1.5   |  CS   |          100.0 |             |
| 5.1.5   |  EVG  |          100.0 |             |
| 5.1.5   | SMIME |          100.0 |             |
| 5.1.6   |  CS   |          100.0 |             |
| 5.1.6   |  EVG  |          100.0 |             |
| 5.1.6   | SMIME |          100.0 |             |
| 5.1.7   |  CS   |          100.0 |             |
| 5.1.7   |  EVG  |          100.0 |             |
| 5.1.7   | SMIME |          100.0 |             |
| 5.1.8   |  CS   |          100.0 |             |
| 5.1.8   |  EVG  |          100.0 |             |
| 5.1.8   | SMIME |          100.0 |             |
| 5.2     |  CS   |          100.0 |             |
| 5.2     |  EVG  |          100.0 |             |
| 5.2     | SMIME |          100.0 |             |
| 5.2.1   |  CS   |          100.0 |             |
| 5.2.1   |  EVG  |          100.0 |             |
| 5.2.1   | SMIME |          100.0 |             |
| 5.2.2   |  CS   |           96.5 |             |
| 5.2.2   |  EVG  |          28.22 |             |
| 5.2.2   | SMIME |           96.5 |             |
| 5.2.3   |  CS   |          100.0 |             |
| 5.2.3   |  EVG  |          100.0 |             |
| 5.2.3   | SMIME |          100.0 |             |
| 5.2.4   |  CS   |          12.97 |             |
| 5.2.4   |  EVG  |          12.52 |             |
| 5.2.4   | SMIME |          100.0 |             |
| 5.3     |  CS   |          100.0 |             |
| 5.3     |  EVG  |          100.0 |             |
| 5.3     | SMIME |          100.0 |             |
| 5.3.1   |  CS   |          100.0 |             |
| 5.3.1   |  EVG  |          34.46 |             |
| 5.3.1   | SMIME |          100.0 |             |
| 5.3.2   |  CS   |           4.54 |             |
| 5.3.2   |  EVG  |           4.55 |             |
| 5.3.2   | SMIME |          100.0 |             |
| 5.3.3   |  CS   |          91.39 |             |
| 5.3.3   |  EVG  |           5.67 |             |
| 5.3.3   | SMIME |          95.67 |             |
| 5.3.4   |  CS   |          100.0 |             |
| 5.3.4   |  EVG  |           41.0 |             |
| 5.3.4   | SMIME |          100.0 |             |
| 5.3.5   |  CS   |          100.0 |             |
| 5.3.5   |  EVG  |          100.0 |             |
| 5.3.5   | SMIME |          100.0 |             |
| 5.3.6   |  CS   |          100.0 |             |
| 5.3.6   |  EVG  |          100.0 |             |
| 5.3.6   | SMIME |          100.0 |             |
| 5.3.7   |  CS   |          97.29 |             |
| 5.3.7   |  EVG  |          21.14 |             |
| 5.3.7   | SMIME |          95.24 |             |
| 5.3.8   |  CS   |          100.0 |             |
| 5.3.8   |  EVG  |          100.0 |             |
| 5.3.8   | SMIME |          100.0 |             |
| 5.4     |  CS   |          100.0 |             |
| 5.4     |  EVG  |          49.09 |             |
| 5.4     | SMIME |          100.0 |             |
| 5.4.1   |  CS   |           2.37 |             |
| 5.4.1   |  EVG  |           2.37 |             |
| 5.4.1   | SMIME |          69.38 |             |
| 5.4.2   |  CS   |          91.18 |             |
| 5.4.2   |  EVG  |          91.18 |             |
| 5.4.2   | SMIME |          100.0 |             |
| 5.4.3   |  CS   |           63.9 |             |
| 5.4.3   |  EVG  |           6.02 |             |
| 5.4.3   | SMIME |          99.13 |             |
| 5.4.4   |  CS   |          100.0 |             |
| 5.4.4   |  EVG  |          100.0 |             |
| 5.4.4   | SMIME |          100.0 |             |
| 5.4.5   |  CS   |          100.0 |             |
| 5.4.5   |  EVG  |          100.0 |             |
| 5.4.5   | SMIME |          100.0 |             |
| 5.4.6   |  CS   |          100.0 |             |
| 5.4.6   |  EVG  |          100.0 |             |
| 5.4.6   | SMIME |          100.0 |             |
| 5.4.7   |  CS   |          100.0 |             |
| 5.4.7   |  EVG  |          100.0 |             |
| 5.4.7   | SMIME |          100.0 |             |
| 5.4.8   |  CS   |          100.0 |             |
| 5.4.8   |  EVG  |           8.66 |             |
| 5.4.8   | SMIME |          95.91 |             |
| 5.5     |  CS   |          100.0 |             |
| 5.5     |  EVG  |          100.0 |             |
| 5.5     | SMIME |          100.0 |             |
| 5.5.1   |  CS   |           99.9 |             |
| 5.5.1   |  EVG  |          11.39 |             |
| 5.5.1   | SMIME |           99.9 |             |
| 5.5.2   |  CS   |          99.74 |             |
| 5.5.2   |  EVG  |           4.69 |             |
| 5.5.2   | SMIME |          99.96 |             |
| 5.5.3   |  CS   |          100.0 |             |
| 5.5.3   |  EVG  |          100.0 |             |
| 5.5.3   | SMIME |          100.0 |             |
| 5.5.4   |  CS   |          100.0 |             |
| 5.5.4   |  EVG  |          100.0 |             |
| 5.5.4   | SMIME |          100.0 |             |
| 5.5.5   |  CS   |          100.0 |             |
| 5.5.5   |  EVG  |          100.0 |             |
| 5.5.5   | SMIME |          100.0 |             |
| 5.5.6   |  CS   |          100.0 |             |
| 5.5.6   |  EVG  |          100.0 |             |
| 5.5.6   | SMIME |          100.0 |             |
| 5.5.7   |  CS   |          100.0 |             |
| 5.5.7   |  EVG  |          100.0 |             |
| 5.5.7   | SMIME |          100.0 |             |
| 5.6     |  CS   |          100.0 |             |
| 5.6     |  EVG  |          100.0 |             |
| 5.6     | SMIME |          100.0 |             |
| 5.7     |  CS   |          100.0 |             |
| 5.7     |  EVG  |          100.0 |             |
| 5.7     | SMIME |          100.0 |             |
| 5.7.1   |  CS   |          100.0 |             |
| 5.7.1   |  EVG  |           5.47 |             |
| 5.7.1   | SMIME |          64.23 |             |
| 5.7.2   |  CS   |          83.21 |             |
| 5.7.2   |  EVG  |          83.21 |             |
| 5.7.2   | SMIME |          83.21 |             |
| 5.7.3   |  CS   |          61.36 |             |
| 5.7.3   |  EVG  |          61.36 |             |
| 5.7.3   | SMIME |          61.36 |             |
| 5.7.4   |  CS   |          100.0 |             |
| 5.7.4   |  EVG  |          100.0 |             |
| 5.7.4   | SMIME |          100.0 |             |
| 5.8     |  CS   |           9.56 |             |
| 5.8     |  EVG  |          100.0 |             |
| 5.8     | SMIME |          100.0 |             |
| 6       |  CS   |          100.0 |             |
| 6       |  EVG  |          100.0 |             |
| 6       | SMIME |          100.0 |             |
| 6.1     |  CS   |          100.0 |             |
| 6.1     |  EVG  |          100.0 |             |
| 6.1     | SMIME |          100.0 |             |
| 6.1.1   |  CS   |          100.0 |             |
| 6.1.1   |  EVG  |           4.19 |             |
| 6.1.1   | SMIME |          100.0 |             |
| 6.1.1.1 |  CS   |          97.14 |             |
| 6.1.1.1 | SMIME |          57.18 |             |
| 6.1.1.2 |  CS   |          100.0 |             |
| 6.1.1.2 | SMIME |          100.0 |             |
| 6.1.1.3 |  CS   |          84.79 |             |
| 6.1.1.3 | SMIME |          81.46 |             |
| 6.1.2   |  CS   |          56.41 |             |
| 6.1.2   |  EVG  |          15.26 |             |
| 6.1.2   | SMIME |          30.22 |             |
| 6.1.3   |  CS   |          100.0 |             |
| 6.1.3   |  EVG  |          100.0 |             |
| 6.1.3   | SMIME |          100.0 |             |
| 6.1.4   |  CS   |          100.0 |             |
| 6.1.4   |  EVG  |          100.0 |             |
| 6.1.4   | SMIME |          100.0 |             |
| 6.1.5   |  CS   |           6.93 |             |
| 6.1.5   |  EVG  |           6.93 |             |
| 6.1.5   | SMIME |          84.88 |             |
| 6.1.6   |  CS   |          100.0 |             |
| 6.1.6   |  EVG  |          16.33 |             |
| 6.1.6   | SMIME |           63.6 |             |
| 6.1.7   |  CS   |           5.15 |             |
| 6.1.7   |  EVG  |          19.85 |             |
| 6.1.7   | SMIME |          45.65 |             |
| 6.2     |  CS   |          100.0 |             |
| 6.2     |  EVG  |          20.82 |             |
| 6.2     | SMIME |          99.26 |             |
| 6.2.1   |  CS   |          100.0 |             |
| 6.2.1   |  EVG  |          100.0 |             |
| 6.2.1   | SMIME |          100.0 |             |
| 6.2.2   |  CS   |          100.0 |             |
| 6.2.2   |  EVG  |          100.0 |             |
| 6.2.2   | SMIME |          100.0 |             |
| 6.2.3   |  CS   |          100.0 |             |
| 6.2.3   |  EVG  |          100.0 |             |
| 6.2.3   | SMIME |          100.0 |             |
| 6.2.4   |  CS   |          90.54 |             |
| 6.2.4   |  EVG  |           44.9 |             |
| 6.2.4   | SMIME |          90.54 |             |
| 6.2.5   |  CS   |          100.0 |             |
| 6.2.5   |  EVG  |          26.52 |             |
| 6.2.5   | SMIME |          100.0 |             |
| 6.2.6   |  CS   |          78.08 |             |
| 6.2.6   |  EVG  |          20.69 |             |
| 6.2.6   | SMIME |          100.0 |             |
| 6.2.7   |  CS   |           22.6 |             |
| 6.2.7   |  EVG  |           22.6 |             |
| 6.2.7   | SMIME |          100.0 |             |
| 6.2.8   |  CS   |          82.54 |             |
| 6.2.8   |  EVG  |          82.54 |             |
| 6.2.8   | SMIME |          82.54 |             |
| 6.2.9   |  CS   |          83.58 |             |
| 6.2.9   |  EVG  |          83.58 |             |
| 6.2.9   | SMIME |          83.58 |             |
| 6.2.10  |  CS   |          83.08 |             |
| 6.2.10  |  EVG  |          83.08 |             |
| 6.2.10  | SMIME |          83.08 |             |
| 6.2.11  |  CS   |          100.0 |             |
| 6.2.11  |  EVG  |          100.0 |             |
| 6.2.11  | SMIME |          100.0 |             |
| 6.3     |  CS   |          100.0 |             |
| 6.3     |  EVG  |          100.0 |             |
| 6.3     | SMIME |          100.0 |             |
| 6.3.1   |  CS   |          100.0 |             |
| 6.3.1   |  EVG  |          100.0 |             |
| 6.3.1   | SMIME |          100.0 |             |
| 6.3.2   |  CS   |           10.9 |             |
| 6.3.2   |  EVG  |           25.0 |             |
| 6.3.2   | SMIME |          76.03 |             |
| 6.4     |  CS   |          100.0 |             |
| 6.4     |  EVG  |          100.0 |             |
| 6.4     | SMIME |          100.0 |             |
| 6.4.1   |  CS   |          100.0 |             |
| 6.4.1   |  EVG  |          100.0 |             |
| 6.4.1   | SMIME |          100.0 |             |
| 6.4.2   |  CS   |          100.0 |             |
| 6.4.2   |  EVG  |          100.0 |             |
| 6.4.2   | SMIME |          100.0 |             |
| 6.4.3   |  CS   |          100.0 |             |
| 6.4.3   |  EVG  |          100.0 |             |
| 6.4.3   | SMIME |          100.0 |             |
| 6.5     |  CS   |          100.0 |             |
| 6.5     |  EVG  |          100.0 |             |
| 6.5     | SMIME |          100.0 |             |
| 6.5.1   |  CS   |          100.0 |             |
| 6.5.1   |  EVG  |          47.96 |             |
| 6.5.1   | SMIME |          100.0 |             |
| 6.5.2   |  CS   |          100.0 |             |
| 6.5.2   |  EVG  |          100.0 |             |
| 6.5.2   | SMIME |          100.0 |             |
| 6.6     |  CS   |          100.0 |             |
| 6.6     |  EVG  |          100.0 |             |
| 6.6     | SMIME |          100.0 |             |
| 6.6.1   |  CS   |          100.0 |             |
| 6.6.1   |  EVG  |          100.0 |             |
| 6.6.1   | SMIME |          100.0 |             |
| 6.6.2   |  CS   |          100.0 |             |
| 6.6.2   |  EVG  |          100.0 |             |
| 6.6.2   | SMIME |          100.0 |             |
| 6.6.3   |  CS   |          100.0 |             |
| 6.6.3   |  EVG  |          100.0 |             |
| 6.6.3   | SMIME |          100.0 |             |
| 6.7     |  CS   |          100.0 |             |
| 6.7     |  EVG  |          100.0 |             |
| 6.7     | SMIME |          29.47 |             |
| 6.8     |  CS   |           3.61 |             |
| 6.8     |  EVG  |          100.0 |             |
| 6.8     | SMIME |          100.0 |             |
| 7       |  CS   |          100.0 |             |
| 7       |  EVG  |          100.0 |             |
| 7       | SMIME |          100.0 |             |
| 7.1     |  CS   |          54.14 |             |
| 7.1     |  EVG  |          28.84 |             |
| 7.1     | SMIME |          40.43 |             |
| 7.1.1   |  CS   |          100.0 |             |
| 7.1.1   |  EVG  |           50.0 |             |
| 7.1.1   | SMIME |          93.91 |             |
| 7.1.2   |  CS   |           6.04 |             |
| 7.1.2   |  EVG  |           4.68 |             |
| 7.1.2   | SMIME |          10.96 |             |
| 7.1.2.1 |  CS   |           1.16 |             |
| 7.1.2.1 |  EVG  |           3.39 |             |
| 7.1.2.1 | SMIME |           1.64 |             |
| 7.1.2.2 |  CS   |           2.91 |             |
| 7.1.2.2 |  EVG  |           2.27 |             |
| 7.1.2.2 | SMIME |           3.23 |             |
| 7.1.2.3 |  CS   |           4.25 |             |
| 7.1.2.3 | SMIME |           1.62 |             |
| 7.1.2.4 |  CS   |           3.77 |             |
| 7.1.2.4 | SMIME |           3.81 |             |
| 7.1.3   |  CS   |          100.0 |             |
| 7.1.3   |  EVG  |          100.0 |             |
| 7.1.3   | SMIME |          100.0 |             |
| 7.1.3.1 |  CS   |          10.13 |             |
| 7.1.3.1 | SMIME |           4.37 |             |
| 7.1.3.2 |  CS   |           2.43 |             |
| 7.1.3.2 | SMIME |          23.18 |             |
| 7.1.4   |  CS   |          10.73 |             |
| 7.1.4   |  EVG  |          10.73 |             |
| 7.1.4   | SMIME |          27.04 |             |
| 7.1.4.1 |  CS   |           5.24 |             |
| 7.1.4.1 |  EVG  |           6.13 |             |
| 7.1.4.1 | SMIME |          49.16 |             |
| 7.1.4.2 |  CS   |           3.28 |             |
| 7.1.4.2 |  EVG  |           5.44 |             |
| 7.1.4.2 | SMIME |           2.41 |             |
| 7.1.4.3 |  EVG  |           2.56 |             |
| 7.1.4.3 | SMIME |           1.44 |             |
| 7.1.6   |  CS   |          30.89 |             |
| 7.1.6   |  EVG  |          35.87 |             |
| 7.1.6   | SMIME |          32.39 |             |
| 7.1.6.1 |  CS   |          54.07 |             |
| 7.1.6.1 |  EVG  |          17.25 |             |
| 7.1.6.1 | SMIME |          21.72 |             |
| 7.1.7   |  CS   |          100.0 |             |
| 7.1.7   |  EVG  |          100.0 |             |
| 7.1.7   | SMIME |          100.0 |             |
| 7.1.8   |  CS   |          100.0 |             |
| 7.1.8   |  EVG  |          100.0 |             |
| 7.1.8   | SMIME |          100.0 |             |
| 7.1.9   |  CS   |          100.0 |             |
| 7.1.9   |  EVG  |          100.0 |             |
| 7.1.9   | SMIME |          100.0 |             |
| 7.2     |  CS   |           1.71 |             |
| 7.2     |  EVG  |           0.84 |             |
| 7.2     | SMIME |           0.84 |             |
| 7.2.1   |  CS   |           41.3 |             |
| 7.2.1   |  EVG  |           41.3 |             |
| 7.2.1   | SMIME |           41.3 |             |
| 7.2.2   |  CS   |           1.26 |             |
| 7.2.2   |  EVG  |           1.15 |             |
| 7.2.2   | SMIME |           2.64 |             |
| 7.3     |  CS   |           7.94 |             |
| 7.3     |  EVG  |           7.54 |             |
| 7.3     | SMIME |          51.34 |             |
| 7.3.1   |  CS   |          100.0 |             |
| 7.3.1   |  EVG  |          100.0 |             |
| 7.3.1   | SMIME |          100.0 |             |
| 7.3.2   |  CS   |          26.57 |             |
| 7.3.2   |  EVG  |          26.57 |             |
| 7.3.2   | SMIME |          97.19 |             |
| 8       |  CS   |          28.38 |             |
| 8       |  EVG  |           6.26 |             |
| 8       | SMIME |          26.72 |             |
| 8.1     |  CS   |          69.37 |             |
| 8.1     |  EVG  |          13.15 |             |
| 8.1     | SMIME |          88.49 |             |
| 8.2     |  CS   |          100.0 |             |
| 8.2     |  EVG  |          19.08 |             |
| 8.2     | SMIME |          76.55 |             |
| 8.3     |  CS   |          100.0 |             |
| 8.3     |  EVG  |          100.0 |             |
| 8.3     | SMIME |          100.0 |             |
| 8.4     |  CS   |          49.61 |             |
| 8.4     |  EVG  |           2.85 |             |
| 8.4     | SMIME |          61.79 |             |
| 8.5     |  CS   |          100.0 |             |
| 8.5     |  EVG  |          100.0 |             |
| 8.5     | SMIME |          100.0 |             |
| 8.6     |  CS   |          99.49 |             |
| 8.6     |  EVG  |           2.55 |             |
| 8.6     | SMIME |          68.42 |             |
| 8.7     |  CS   |           5.44 |             |
| 8.7     |  EVG  |           1.54 |             |
| 8.7     | SMIME |          30.93 |             |
| 9       |  CS   |          100.0 |             |
| 9       |  EVG  |          100.0 |             |
| 9       | SMIME |          100.0 |             |
| 9.1     |  CS   |          100.0 |             |
| 9.1     |  EVG  |          100.0 |             |
| 9.1     | SMIME |          100.0 |             |
| 9.1.1   |  CS   |          100.0 |             |
| 9.1.1   |  EVG  |          100.0 |             |
| 9.1.1   | SMIME |          100.0 |             |
| 9.1.2   |  CS   |          100.0 |             |
| 9.1.2   |  EVG  |          100.0 |             |
| 9.1.2   | SMIME |          100.0 |             |
| 9.1.3   |  CS   |          100.0 |             |
| 9.1.3   |  EVG  |          100.0 |             |
| 9.1.3   | SMIME |          100.0 |             |
| 9.1.4   |  CS   |          100.0 |             |
| 9.1.4   |  EVG  |          100.0 |             |
| 9.1.4   | SMIME |          100.0 |             |
| 9.1.5   |  CS   |          100.0 |             |
| 9.1.5   |  EVG  |          100.0 |             |
| 9.1.5   | SMIME |          100.0 |             |
| 9.2     |  CS   |          100.0 |             |
| 9.2     |  EVG  |          100.0 |             |
| 9.2     | SMIME |          100.0 |             |
| 9.2.1   |  CS   |          25.14 |             |
| 9.2.1   |  EVG  |           3.25 |             |
| 9.2.1   | SMIME |          100.0 |             |
| 9.2.2   |  CS   |          100.0 |             |
| 9.2.2   |  EVG  |          100.0 |             |
| 9.2.2   | SMIME |          100.0 |             |
| 9.2.3   |  CS   |          100.0 |             |
| 9.2.3   |  EVG  |          100.0 |             |
| 9.2.3   | SMIME |          100.0 |             |
| 9.3     |  CS   |          100.0 |             |
| 9.3     |  EVG  |          100.0 |             |
| 9.3     | SMIME |          100.0 |             |
| 9.3.1   |  CS   |          100.0 |             |
| 9.3.1   |  EVG  |          100.0 |             |
| 9.3.1   | SMIME |          100.0 |             |
| 9.3.2   |  CS   |          100.0 |             |
| 9.3.2   |  EVG  |          100.0 |             |
| 9.3.2   | SMIME |          100.0 |             |
| 9.3.3   |  CS   |          100.0 |             |
| 9.3.3   |  EVG  |          100.0 |             |
| 9.3.3   | SMIME |          100.0 |             |
| 9.4     |  CS   |          100.0 |             |
| 9.4     |  EVG  |          100.0 |             |
| 9.4     | SMIME |          100.0 |             |
| 9.4.1   |  CS   |          100.0 |             |
| 9.4.1   |  EVG  |          100.0 |             |
| 9.4.1   | SMIME |           7.73 |             |
| 9.4.2   |  CS   |          100.0 |             |
| 9.4.2   |  EVG  |          100.0 |             |
| 9.4.2   | SMIME |          21.12 |             |
| 9.4.3   |  CS   |          100.0 |             |
| 9.4.3   |  EVG  |          100.0 |             |
| 9.4.3   | SMIME |          100.0 |             |
| 9.4.4   |  CS   |          100.0 |             |
| 9.4.4   |  EVG  |          100.0 |             |
| 9.4.4   | SMIME |          29.97 |             |
| 9.4.5   |  CS   |          100.0 |             |
| 9.4.5   |  EVG  |          100.0 |             |
| 9.4.5   | SMIME |          21.21 |             |
| 9.4.6   |  CS   |          100.0 |             |
| 9.4.6   |  EVG  |          100.0 |             |
| 9.4.6   | SMIME |          100.0 |             |
| 9.4.7   |  CS   |          100.0 |             |
| 9.4.7   |  EVG  |          100.0 |             |
| 9.4.7   | SMIME |          100.0 |             |
| 9.5     |  CS   |          100.0 |             |
| 9.5     |  EVG  |          100.0 |             |
| 9.5     | SMIME |          100.0 |             |
| 9.6     |  CS   |          100.0 |             |
| 9.6     |  EVG  |          100.0 |             |
| 9.6     | SMIME |          100.0 |             |
| 9.6.1   |  CS   |           5.73 |             |
| 9.6.1   |  EVG  |           3.52 |             |
| 9.6.1   | SMIME |           54.8 |             |
| 9.6.2   |  CS   |          100.0 |             |
| 9.6.2   |  EVG  |          100.0 |             |
| 9.6.2   | SMIME |          100.0 |             |
| 9.6.3   |  CS   |          31.35 |             |
| 9.6.3   |  EVG  |           4.73 |             |
| 9.6.3   | SMIME |          61.61 |             |
| 9.6.4   |  CS   |          100.0 |             |
| 9.6.4   |  EVG  |          100.0 |             |
| 9.6.4   | SMIME |          100.0 |             |
| 9.6.5   |  CS   |            9.4 |             |
| 9.6.5   |  EVG  |          100.0 |             |
| 9.6.5   | SMIME |          100.0 |             |
| 9.7     |  CS   |          100.0 |             |
| 9.7     |  EVG  |          100.0 |             |
| 9.7     | SMIME |          100.0 |             |
| 9.8     |  CS   |          30.93 |             |
| 9.8     |  EVG  |           4.16 |             |
| 9.8     | SMIME |           68.2 |             |
| 9.9     |  CS   |          100.0 |             |
| 9.9     |  EVG  |           9.76 |             |
| 9.9     | SMIME |          96.11 |             |
| 9.10    |  CS   |          100.0 |             |
| 9.10    |  EVG  |          100.0 |             |
| 9.10    | SMIME |          100.0 |             |
| 9.10.1  |  CS   |          100.0 |             |
| 9.10.1  |  EVG  |          100.0 |             |
| 9.10.1  | SMIME |          100.0 |             |
| 9.10.2  |  CS   |          100.0 |             |
| 9.10.2  |  EVG  |          100.0 |             |
| 9.10.2  | SMIME |          100.0 |             |
| 9.10.3  |  CS   |          100.0 |             |
| 9.10.3  |  EVG  |          100.0 |             |
| 9.10.3  | SMIME |          100.0 |             |
| 9.11    |  CS   |          100.0 |             |
| 9.11    |  EVG  |          100.0 |             |
| 9.11    | SMIME |          100.0 |             |
| 9.12    |  CS   |          100.0 |             |
| 9.12    |  EVG  |          100.0 |             |
| 9.12    | SMIME |          100.0 |             |
| 9.12.1  |  CS   |          100.0 |             |
| 9.12.1  |  EVG  |          100.0 |             |
| 9.12.1  | SMIME |          100.0 |             |
| 9.12.2  |  CS   |          100.0 |             |
| 9.12.2  |  EVG  |          100.0 |             |
| 9.12.2  | SMIME |          100.0 |             |
| 9.12.3  |  CS   |          100.0 |             |
| 9.12.3  |  EVG  |          100.0 |             |
| 9.12.3  | SMIME |          100.0 |             |
| 9.13    |  CS   |          100.0 |             |
| 9.13    |  EVG  |          100.0 |             |
| 9.13    | SMIME |          100.0 |             |
| 9.14    |  CS   |          100.0 |             |
| 9.14    |  EVG  |          100.0 |             |
| 9.14    | SMIME |          100.0 |             |
| 9.15    |  CS   |          27.31 |             |
| 9.15    |  EVG  |          27.31 |             |
| 9.15    | SMIME |          27.31 |             |
| 9.16    |  CS   |          100.0 |             |
| 9.16    |  EVG  |          100.0 |             |
| 9.16    | SMIME |          100.0 |             |
| 9.16.1  |  CS   |          100.0 |             |
| 9.16.1  |  EVG  |          100.0 |             |
| 9.16.1  | SMIME |          100.0 |             |
| 9.16.2  |  CS   |          100.0 |             |
| 9.16.2  |  EVG  |          100.0 |             |
| 9.16.2  | SMIME |          100.0 |             |
| 9.16.3  |  CS   |          12.69 |             |
| 9.16.3  |  EVG  |          10.69 |             |
| 9.16.3  | SMIME |          56.83 |             |
| 9.16.4  |  CS   |          100.0 |             |
| 9.16.4  |  EVG  |          100.0 |             |
| 9.16.4  | SMIME |          100.0 |             |
| 9.16.5  |  CS   |          100.0 |             |
| 9.16.5  |  EVG  |          100.0 |             |
| 9.16.5  | SMIME |          100.0 |             |
| 9.17    |  CS   |          100.0 |             |
| 9.17    |  EVG  |          100.0 |             |
| 9.17    | SMIME |          100.0 |             |
| A       |  CS   |          12.57 |             |
| A       |  EVG  |          11.76 |             |
| A       | SMIME |          48.22 |             |
| A.1     | SMIME |           6.29 |             |
| A.2     | SMIME |          11.03 |             |
| B       |  EVG  |            2.1 |             |
| B       | SMIME |            2.7 |             |


## TODO
- Handle "No stipulation", this is now less predictable, when do we want this?
- Review the requirement matrix, do we need to add more information.
- Move TLS requirements from BR to TLS to ensure that they are not included in CS or SMIME requirements.
- Define a LoA (OV/EV or something new) for in addition to the document type.
- Create an option to create a CSV file with all requirements for all document types.
