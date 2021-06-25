# Meeting Minutes

## 10/4/2020 - Students Only

- Find patterns for unrelated text in each article providers by looking at common patterns in first few words of paragraph and header tags. (Matt to work more on this)
- Find patterns of noisy text by new source. Focus sources that contribute 25% of the data

## 10/6/2020 - Biweekly Team

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

## 10/28/2020 - Weekly Team

- Presented sampling procedure
  - Sampled ~1.5 million articles from ~17 million
  - Uploaded sample data to ~6GB, shared on google drive
- Need to check distribution of peaceful/neutral/in-confilct countries for sampled data.
- Next Steps:
  - Clean text thoroughly
  - Word Freq analysis
  - Topic Modeling
  - Utilize word vectors for contextual modeling
- Next Goal from team:
  - After validating current lexicon, begin extending the lexicon
- What was the standard for choosing lexicon?
  - Started by looking at glossaries, manually sorted them into positive/negative peace
  - Peace linguist offered more terms
  - Small version of text analysis from anthropological and academic articles, manual sorting
- When people talk about peace, often about the _lack of conflict_
  - Apply all 3 lexicons in WF analayis
- Worried that the words in lexicon may not show up in articles
  - Determine % of articles that contain lexicon words?
- Interested in domestic articles, not international
- **Priority**: WF analysis

## 11/3/2020 - Saurav + Philippe

- **Elaborate on README** - add details with what folder does what, etc...
- Evaluation of cleaning:
  - Doc2Vec - would need to train, probably don't have time for this
  - N-gram does a good enough job
- Identifing foreign articles
  - Supervised learning - need annotated set
  - Unsupervised
    - Topic modeling
    - Clustering
  - Frequency analysis - does the article metion domestic country or cities?
- Data Management
  - Use a database
    - NoSQL: DynamoDB, MongoDB
    - SQL: MySQL
    - Saurav will provide recommendations for database creation and security
    - Maybe we use GCP to host since we have \$100
- Write models in a class structure for reusability

## 11/4/2020 - Biweekly Meeting

- Weekly Summary: subsampled, lematization, stopwords done. Began WF analysis.
- Peace is harder to measure than violence. Measuring casualties and arrests is easier then mundane peace.
  - The less interesting words in peace lexicon showing up are still valuable
- Need more analysis and conclusions from WF analysis.
  - Bucket words by lexicon
  - Score countries as %positve - %negative lexicons
  - Investigate with/without filtering articles that talk about foreign nations
- Look at the data and see what shows up, find new lexicon words
- Zipf's Law, investigate ways to compare distributions of words
- Classifier - what type of a country does a new article come from.

  - Use full article text and embeddings to find boundries between peaceful/non...
    - We are interested in things like, "canadian journalists write about confilct fundementally differently"
  - Maybe use other article characteristics as well

    1. Classifier on whether an article is from the source or not
       - method: Use Named-Entity-Recognition (NER) to retrieve the location names, check the ratio of the source nation, and determine whether it is from the source or not
    2. Classifier on whether an article is from peaceful, non-peaceful, neutral (or on which country it is from)
       - method discussed: Given the labels (Use country peaceful labels as labels for articles), use transfer learning and transformer models to build one.
       - objective: to find out whether there is a boundary that classify the peaceful, non-peaceful, neutral nation

- Calculate the distance between lexicons from peace, conflict, resilence
  - Train word vector (word2vec: either CBOW, Skip-gram), embed each lexicons and perform clustering

## 11/10/2020 - Saurav

- Word embedding techniques to find new key lexicon words
  - find nearest words in vector space to our current lexicon words
- Ivestigate variants of Word2Vec models
- Mess with parameter spaces of Word2Vec
  - do we sacrifice performance for speed?
    - visually inspect clusters
    - find a clustering metric
- May improve embeddings if we include sentence segmentation

## 11/11/2020 - Weekly Team

- Possible reinbursement for Colab Pro
- "Peace Metric" not giving the kind of results we want.
  - i.e., GB score too low, TZ score too high
- Don't use "Neutral" use something like "Medium"
- Resilliance Lexicon - factors used to control violence, descrimination...
- Possible Issues
  - Country classification might be off
    - We are testing to see if the lexicosns are working or not.
    - Confident in categorization, grouped using 5 different indices.
  - The lexicons might not be working
    - Censorship could be leading to non-peaceful countries appearing more peaceful in media
- Thoughts on new goals
  - Expanding the lexicons
    - Same as what Saurav said, use current lexicon words and find closest word vectors to those and find new words.
  - Domestic v International News
    - Does the article mention the publishing country?
    - Don't do this yet!
- **End Goals**
  - We want to see if highly peaceful/nonpeaceful will differ in the kinds of language present in their society. (Print journalism right now)
    - Media allows for dynamic monitoring, where other indices do not
  - Revise lexicons so they become better predictors
  - Create a metric, and build a dashboard to see realtime assessment of how people are talking to eachother in different places.
  - **Where we currently are: "Does language help us differentiate these countries, and what are the lexicons"**

## Biweekly Meeting - 11/18/2020

- Investigate feature importances from Doc2Vec model
- Compare RNN words to top frequency words.
- Continue with next steps...
- Send report before due on Tuesday for feed back
- No meeting next week, back on 12/2
- Compare top words by country/year

## Biweekly Meeting - 12/2/2020

- Getting good press!
- **Last meeting 12/9** for final findings... Send report to team for offline review.
- Extract words from attention layer, compare with words from FA. 
- Is list of words enough or do individual words have predictive power alone?
  - Classification model just using vocab words?
- There is a conference in July, Allegra will send details if we wish to apply. 