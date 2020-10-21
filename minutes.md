# Meeting Minutes

## 10/4/2020 - Students Only

- Find patterns for unrelated text in each article providers by looking at common patterns in first few words of paragraph and header tags. (Matt to work more on this)
- Find patterns of noisy text by new source. Focus sources that contribute 25% of the data

## 10/6/2020 - Bi-Weekly Team

- We got the data - two types of files:
  1. sources and
  2. folders of by year/month containing the text
- "xx" country - possibly when no country in the sources.
- Pre-process in batches
- We are looking to understand the data we have -- descriptive analysis, we can do that in sections, not necessarily all at once.
- Don't over-delete when removing sentences
- Sanity check that sentence removal is not overdoing it
- Mentors will bin countries into 3 groups and let us know

## 10/13/2020 - Students Only

- First progress report due next friday... let's get it done thursday
- File export mostly done.. there are a few edge cases we need to get at.

- Things to do:
  - create a summary table of #articles/words by publisher
  - create a lookup of aritcle ids to publisher
  - determine how and when to remove noise and stop words from data
  - create a notebook to make an abridged dataset to start working on a pipeline
  - determine if we can drop publishers that do not contribute a minimum number of articles.

## 10/14/2020 - Weekly Team

- In the future, coordinate who will be presenting the work.
- Possible other dataset - Lexus Nexus - might be much larger.
- Reflection/Challenges:
  - Space requirements with duplicate dataset, raw/clean
    - Possible solution: get external hardrives? Move to cloud?
  - What are the next steps?
    - Word Frequencies
  - Inconsistencies between source/text files... Need to capture as many edge cases as possible
- **New Team Captain: JJ**
- **Next Week Presenter: Tae Yoon**

## 10/21/2020 - Biweekly Team

- First draft submitted
- Big question: data size
  - what is the expectation for the volumne of data we use?
  - There are 20 million files, it will take weeks to preproccess it all.
  - Phillipe: subsample later years to match volume from earlier year.
- Sensitivity analysis around noise removal?
  - don't need rigorous statistics, but maybe an analysis of one publisher. Include top ngrams removed in report. Sanity check that we are not overkilling words.