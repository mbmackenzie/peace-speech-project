# The Power of Peace Speech
Columbia University - Data Science Institute - FALL 2020 Capstone Project

**Team Members**<br>
Jinwoo Jung (jj2762@columbia.edu)<br>
Hojin Lee (hl3328@columbia.edu)<br>
Hyuk Joon Kwon (hk3084@columbia.edu)<br> 
Matt Mackenzie (mbm2228@columbia.edu)<br>
Tae Yoon Lim (tl2968@columbia.edu)

**Advisors**<br>
Peter Coleman, Professor, Psychology and Education<br>
Allegra Chen-carrel, Program Manager, The Sustaining Peace Project

**Final Presentation**<br>
Video: https://www.youtube.com/watch?v=hTtMzFsc-9A&feature=youtu.be<br>
Deck: [The Power of Peace Speech.pdf](The%20Power%20of%20Peace%20Speech.pdf)


## Project Overview

As the world gets more polarized, one of the biggest challenges we face hate speech. The harm of hate speech is an active area of research, and the general consensus in the recent literature is that hate speech tends to cause harm to societies. However, there was not much attention to the other side of the story: peace speech.

We were interested in whether peace speech could play a role in measuring and promoting more peaceful societies as some research suggests that peace speech is the DNA of peaceful societies. If the hypothesis is supported, we could develop techniques to understand, measure, and track the power of peace speech, which will guide us toward building and maintaining more robust and peaceful communities.

We will look into news articles from many different countries, analyze them using natural language processing (NLP) techniques, and study the relationship between the language used in the articles and the peacefulness of the country.

### Data

The data that our group is working on is the News on the Web (NOW) dataset from corpusdata.org. According to the source, the data is “composed of 11.2 billion words from web-based newspapers and magazines from 2010 to present times” from 20 countries.

The 20 countries are classifies into 3 groups for the purposes of this analysis.


| Peaceful            | Non-Peaceful    | Neutral            |
|---------------------|-----------------|--------------------|
| Australia (AU)      | Bangladesh (BD) | Ghana (GH)         |
| Canada (CA)         | Kenya (KE)      | Hong Kong (HK)     |
| Ireland (IE)        | Nigeria (NG)    | India (IN)         |
| New Zealand (NZ)    | Pakistan (PK)   | Jamaica (JM)       |
| Singapore (SG)      | Tanzania (TZ)   | Malaysia (MY)      |
| United Kingdom (GB) |                 | South Africa (ZA)  |
|                     |                 | Philippines (PH)   |
|                     |                 | Sri Lanka (LK)     |
|                     |                 | United States (US) |

## Files and Folder

### Reports

The *Reports* folder contains our progress reports of the projects.
We will be adding our final reports and poster as well towards the end of the semester.

### Data Files

The [data](data) folder contains multiple folders that housed the different forms of our data at different times.

- `original` contains the full, non-processed data set separating into source files and text folders
- `raw` contains the full, non-processed data set, orgainzed in a `COUNTRY/PUBLUSHER/YEAR` folder format.
- `sample_raw` contains the non-processed files that we sampled from the full data, orgainzed in a `COUNTRY/PUBLUSHER/YEAR` folder format.
- `clean` contains the cleaned data in the `COUNTRY/PUBLUSHER/YEAR` folder format.

For size and privacy reasons, the data is not stored on GitHub, but the folder act as a template for how our scripts and notebooks work.

### Lexicons

The *Lexicons* folder contains 3 excel files with the original lexicons we had to work with.

### Data Processing

- "Clean Text Files - SAMPLE.ipynb" - This file acts as our way to reorganize the the 'original' data into the 'raw' format.
- "Export Sampled Data.ipynb" - This file creates a representative sample of our data for eaiser use

### Analysis

### Lexicon Validation

#### Classification Models

#### Lexicon Generation

### Miscellaneous Folder

This folder contains smaller tasks that we needed to accomplish. Things like validating our sampling procedure, experimenting, and other random tasks.

### Visualizations

The *Visualizations* folder contains python and R notebooks for generating visualizations.

### Utility Functions and Tests

The *utils* folder contains a python module of useful functions to be reused. The *tests* folder contains unit tests (using python's unittest library) for the utility functions.
