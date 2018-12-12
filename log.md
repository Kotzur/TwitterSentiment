# Dissertation Log #

## TODO currently on my mind ##
- Finish 3 more models
- Create a CLI interface
- Look into getting Tweets on a chosen hashtag from the API

## Stage 1: Dataset ##
__Anonymizing the dataset__:

- I'm first using data from the Stanford Twitter Sentiment Corpus. The data is in CSV format. There are two files, training and testing file. The testing file is manually tagged and has queries. The testing file is automatically tagged and has no queries.
- The data is in UTF-8 and so should be all Twitter data because Twitter API uses JSON to reply to all requests and JSON assumes UTF-8.
- I remove author username, date of post and replace all @-s with @USERNAME.
- I create a new file ...\_anonymized.csv which contains only tweet sentiment, id, querey (topic) and anonymized text
- I'm trying to use streams

__Loading the data:__

- The Tweet IDs used by the dataset are too large for integer values and I didn't want to store them as longs. Since I don't have more than 2^16 datapoints, I gave the Tweets new IDs, just incremental integers in the order they are in the file. Might need to change this approach / revise it if I will need to load tweets from multiple sources.
- Not to have to perform file IO each time I open the program, I serialized the tweets and sentiments hashmaps and just need to load their bytestream when I run the program. I do this through a method loadSerializedMap which uses a generic to accept any type of map indexed by integers.

__Parsing loaded data:__

- I first add whitespace around all punctuation characters which may be appended to a word even though it's not part of it. Do this using regex replacements (to avoid situations like: "I'm ok.How are you?" -> ["i'm", "ok.How", "are", "you?"])
- This allows me to tokenize words by whitespace. Put them all to lowercase.

### Problems ###
- File IO - loading and constructing maps took a long time so I serialized all maps I load often (lexicon, testing/training maps)
- I kept on getting java.nio.charset.MalformedInputException: Input length = 2 error. This error arises when the reader gets an input that doesn't correspond to the encoding it's using. I fixed it by instead building a BuffferedReader on an InputStreamReader rather than straight from the Files.getBufferedReader(...) because the underlying behaviour of the two when faced with this error is different. The solution is here: https://stackoverflow.com/questions/26268132/all-inclusive-charset-to-avoid-java-nio-charset-malformedinputexception-input
- The IDs were too large and I had integer overflow
- I had to ID something inside a lambda function so I used an AtomicInteger which you can access from inside a lambda and use .getAndIncrement to modify it.
- I just realized there are no neutral entries in the training set, there's only positive and negative which slightly changes my code. I'll need to check why that is and either
    - allow for a neutral sentiment, find right thresholds for classifying a post as such
    - remove all data with neutral sentiment

## Stage 2: Bag of Words ##
- need to keep track of all words that appear to then reconstruct the lexicon. Use a HashSet
- count negative and positive occurances of each word. Solutions:
  1. Use a HashMap of int (id) to int (count) one for each sentiment. 2 * hashmap overhead + 2*num of words * 2 * int
  2. One hashmap of int (id) to hashmap of sentiment to int (count). hashmap overhead + num of words * (int + hashmap overhead + 2*sentiment + 2*int)
  So solution 1 is cheaper, easier to reason about and use later
- build lexicon. Use hashmap of string (word) to sentiment. For each word in the overall count, find its positive and negative count and pick the larger one. Could do more work on this to e.g. find better thresholds of assigning a sentiment (if positive sentiment occurance is harder to come by, the threshold should be lower for positive).
- create assessing method. Given a text, produce its sentiment. Take each word in the text and find its sentiment from lexicon (if there is one). Count which sentiment is seen more often - that's the result. Again, could do more work on the thresholds.

### Problems ###
- as mentioned above, thresholds could be refined to reflect the frequency of sentiments in the data e.g. if there's more negative training data, it's harder for a post to be classified as possitive because it hasn't encountered many positive words.

## Stage 3: Evaluator ##
- record accuracy, recall, precision

### Problems ###
- recall and precision have identical strucutres of calculation. Not to duplicate code, I call the same function on both but switch the order of arguments to make the ratio work. This implementation can be confusing for someone who reads the code and even though I commented it a lot, it's not very intuitive. Might've been a better idea to use a boolean indicator / leave the code duplication in.

## Stage 4: Reimplementation ##
- Switch to Python. I didn't realise we can use script languages for the project so I started it out in Java. Because the project is data based, Python is much more suitable especially that it has all necessary packages for NLP I need.
- Create 3 classifiers: BoW, NB, SVM. NB and SVM are from sklearn but BoW was implemented by me.
- Compare all model accuracies and do permutation tests between them to make sure the comparisons are not between models from the same distribution.
- The best performing model was the NB.
- Train the NB on the whole sentiment twitter dataset and pickle the model.

## Stage 5: Spectrum ##
- Create a spectrum for tweets inputed from the most negative to the most positive ones. This is determined by the probability with which the model classifies the Tweet.
- Load the model from pickle.

### Problems ###
- I didn't want to retrain the model each time I ran the spectrum so I pickled it after one training and I unpickle it each time I wish to use it. There is a possibility of creating the spectrum with retrained model.
- The spectrum created didn't seem that good on some random test I've done. Including more information about the tweets such as PoS data, stemming, frequency cut-offs and other NLP sentiment classifcation methods could help with getting better results. These downfalls are strongly related with how refined we can make the model.

## Meeting notes ##
### First meeting: ###

- Overview of the problems faced by developing countries in Africa where access to reliable information is severly limited. Programs run by the UN are in place to help people in need. A lot of the population is young and has access to social media however their exposure is limited by filter bubbles imposed by operators. Breaking the filter bubbles could prove crucial to delivery of reliant information to deprived regions.
- Currently, social media operators want to maximise their profits from advertisements by prolonging user sessions. To do so they must present digestible, interesting content to the users. Their sites present information that the user is likely to agree with and like leading to personalized News Feeds where everything is tailored to the user. Information they get might be more relevant, but it's not necessarily as stimulating as content that could be presented if those restrictions weren't in place.
- Try to break the filter bubble by finding posts with divergent opinions and present it to the users. Check if 1) it's possible to find content which can be stimulating and still partially agree with the user's opinions 2) users are interested in reading opinions that are not "comfortable" but instead challenge the way they think or propose new ideas.

### Second proposal meetin (After first drafts): ###
- Will need to work on Ethics Approval form because:
    - My experiments will include controvertial topics
    - I will be studying opinion influencing
    - Strong language in Tweets since they use coloquial expressions
    - Data I'm using is from users who published their content online but are unaware I'm runnning this experiment.

- The evaluation will be a mixed-methods evaluation composed of:
    - interviews before and after the experiments
    - during the experiment asking the users what they see, why they make decisions
    - card sorting tweets in order of polarity to compare them with the model output
    - quantitative comparison of multiple models
    - experiments will certainly go wrong so run at least two pilots

- Classifiers that I'll be using:
    - Need to have an output score: confidence and polarity
    - SVMs are good
    - Naive Bayes
    - Bag of words as baseline
    - Passing random classification as success criteria
    - No deep learning - no time for learning how to debug such systems

- Success criteria:
    - create models which are better than random
    - evaluate an interface
    - no social objectives

- Implementation:
    - use HTML + Javascript for the interface
    - Java for the models
    - create 20 design interfaces to open your mind

- Research:
    - There was a similar dissertation in the past about diversification in news articles in 2011 by Iosif Adona.
    - Go through the Further HCI and ID notes

- Important:
    - People will tell me that my project:
        - Is ascientfic
        - Doesn't have enough data
        - Doesn't have a sensible hypothesis

        But I shouldn't worry about that and just press on.
    - Need to leave enough time for the writeup

### Third meeting ###
- share the log, code and designs
- papers:
    - send papers I have read and I want to read so we can prioritize them.
    - write a short summary of each paper to get into the habit of writing and make life easier later
- code:
    - git it and work through pull requests
    - add precision and f-score
    - find out why is there no neutral in training data
- interface:
    - bring designs in
    - write a bit about each
    - highlight main features
    - developing new UI ideas:
        - create metaphores between your use and a different existing UI
        - humanize people by giving them avatars (would that humanize them or give a target for frustration?)
        - play around with Gestallt principles
- user study:
    - card sorting (priority?) give cards to order and compare with model
    - show individual cards and ask how would they respond compared to the original message
    - don't contextualize - no marks for that
    - ask them where they'd look for diverse information like the one presented
- write up:
    - start writing at Christmas
    - write the ethics form when you have a prototype

### Corrections from Overseers ###
- add calendar dates to the schedule
- add milestones to each chunk in schedule
- add ethics acknowledgments
- anonymise Twitter datasets
- specify the models I will implement
- detail evaluation:
  - what will I do
  - how
  - how will I recruit
- reduce the workload to make the project less agressive $\rightarrow$ I moved creating an SVM and card-sorting evaluation to extensions

## Schedule ##

  | Start date  | End date  | Description| Milestones  |  Done? |
  |---|---|-----------------------  |---------|---|
  | 22/10/2018 | 02/11/2018  | Read papers on sentiment analysis, the filter bubble phonomenon and Twitter content suggestion algorithms.  | Background knowledge to start implementation.  | More or less |
  | 05/11/2018  | 09/11/2018  | Create 20 designs for the interface. Pre-process data.  | 20 design concepts. Datasets ready.  | Need to create 8 more designs |
  | 12/11/2018  | 16/11/2018  | Implement bag-of-words classifier. Chose the design.  | Bag-of-words classifier ready.  | Yes |
  | 19/11/2018  | 23/11/2018  | Implement Naive Bayes classifier. Perform cross-validation.  | Naive Bayes classifier. Results from model evaluations.  | Yes |
  | 26/11/2018  | 30/11/2018  | Extra time.  |   |   |
  | 03/12/2018  | 10/12/2018  | Learn JavaScript. Create basic interface. Finish the models in case they are not complete.  | Basic interface.  |   |
  | 10/12/2018  | 19/12/2018  | Link the interface with the model.  | Working program ready to use in user studies.  |   |
  | 26/12/2018  | 05/01/2019  | Write introduction and preparation sections.  | Introduction and Preparation.  |   |
  | 07/01/2019  | 12/01/2019  | Extra time. Make sure all notes are well organized.	  | Clear notes. 	  |   |
  | 14/01/2019  | 18/01/2019  | Design user studies. Recruit subjects for user studies. Use this as buffer time or work on extensions.  | Interview questions and user studies plan. A list of people that will participate in the user studies.  |   |
  | 21/01/2019  | 25/01/2019  | Run two user study pilots. Work on the progress report and presentation.  | Corrected plan for user studies based on the pilots. Draft report and presentation.  |   |
  | 28/01/2019  | 01/02/2019  | Prepare the progress report and the presentation.  | Submitted progress report (01/02/2019)  |   |
  | 04/02/2019  | 15/02/2019  | Run user studies.  | Recordings and notes from the user studies.  |   |
  | 18/02/2019  | 22/02/2019  | Extra time.  |   |   |
  | 25/02/2019  | 01/03/2019  | Gather results from the user studies, perform interview coding, create graphs evaluating the data.  | Statistically analysed interview data, evaluation data ready.  |   |
  | 04/03/2019  | 08/03/2019  | Write implementation section.  | Implementation  |   |
  | 11/03/2019  | 15/03/2019  | Write evaluation section.  | Evaluation  |   |
  | 18/03/2019  | 30/03/2019  | Finish writing dissertation.  | First draft ready.  |   |
  | 01/03/2019  | 19/04/2019  | Extra time  |   |   |
  | 22/04/2019  | 17/05/2019  | Proofreading, corrections and early submission if possible.  | Submitted dissertation.  | No  |
