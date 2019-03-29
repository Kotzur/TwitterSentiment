# Papers #
## Papers to read ##
- Book ["Social media mining"](http://dmml.asu.edu/smm/SMM.pdf) Zafarani, R. Abbasi M. A. Liu H. Cambridge University Press April 2014 Maybe Chapter III Applications, 9 Recommandation in Social Media?

- Filter bubbles:
    1. [Curation Algorithms and Filter Bubbles in Social Networks](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2848526) Berman, R. Katona, Z. June 2018 NET Institute Working Paper No. 16-08
    2. ["Collaborative personalized Twitter recommendation"]() Chen, K. Chen, T. Zheng, G. Jin, O. Yao, E. Yu, Y. 2012 Shanghai Jiao Tong University
    3. ["Designing interfaces for presentation of opinion diversity"](https://www.researchgate.net/publication/221515349_Designing_interfaces_for_presentation_of_opinion_diversity) Munson, S. A. Conference Preceedings for CHI 2009
    4. ["Filter Bubbles, echo chambers, and online news consumption"](https://5harad.com/papers/bubbles.pdf) Flaxman, S. Goel, S. Rao, J. M. Public Opinion Quarterly, Vol 80, Special Issue, 2016, 298-320
    6. ["Beyond the filter bubble: concepts, myths, evidence and issues for future debates"](https://www.ivir.nl/publicaties/download/Beyond_the_filter_bubble__concepts_myths_evidence_and_issues_for_future_debates.pdf) Moeller, J. Helberger N. University of Amsterdam

- Sentiment analysis:
    1. ["Twitter Sentiment Classification using Distant Supervision"](https://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf) Go, A. Bhayani R. Huang, L. Stanford University
    2. ["Twitter Sentiment Analysis: a review"](https://www.ijser.org/paper/Twitter-Sentiment-Analysis-A-Review.html)

## Papers read ##
## Fake news and ideological polarization ##
["Fake news and ideological polarization: Filter bubbles and selective exposure on social media"](http://journals.sagepub.com/doi/pdf/10.1177/0266382117722446) Spohr, D. Business Information Review, 2017, Vol 34, 150-160
- perceived role of fake enws and selective news filtering in recent US presidential election and British eu referendum
- Pew research cener: 62% adults in US get news on social media, 66% of all fb users use it for news
- social networks displayed symptoms of ideological polarization and formation of filter bubbles (see for references)
- trend of western world to become polarized
- people cluster into like-minded, semi-isolated groups which in some cases become extreme
- polarization -> loss of diversity of opinion and arguments -> benefits from having variety of opinions is lost
- individual opinion gives way to group thinking
- less constructive public discussion, too negative view of people from across the political spectrum
- like-minded groups grow extreme
- ignore facts that prove their arguments wrong
- political difference is necessary to facilitate progressive public discussions
- most users are not aware of the algorithm behind the new feed
- no empirical evidence that warrants any strong worries about filter bubbles (Bogrsius)
- range of studies produced contradicting results, identifying filter bubbles on Twitter and facebook
- psychological theory: people have confirmation bias, reject anything that's inconsistent with their consistent view of the world
- news finds me perception: living in the news feed world, people believe they can stay sufficiently informed about the world without explicitly seeking out news. People gather their info from social media -> are misinformed, no fact checking. this perception creates a mislead feeling of staying informed that the big news will always reach me, when in fact the possible benefits of active political knowledge are being lost
- people with this attitude give the responsibility of staying informed citizens to algorithms guiding their news feeds
- social media platforms effectively eliminated entry barriers to media production and distribution (Alcott and Gentzkow)
- Facebook-funded study from 2015 agreed that the current newsfeed algorithm favours posts that support the user's ideological viewpoints (Bakshy et al, 2015)

## Social Media and Fake News in the 2016 Election ##
["Social Media and Fake News in the 2016 Election"](https://web.stanford.edu/~gentzkow/research/fakenews.pdf) Allcott, H. Gentzkow, M. Journal of Economic Perspectives - Vol. 31, No 2, Spring 2017, 211-236
This paper studied the creation and spread of fake news in the year leading up to 2016 US election. Social media has played a major role in the popularization of fake news. In early 2000s the move of news online created concerns including "excess diversity of viewpoints would make it easier for like-minded citizens to form "echo chambers" or "filter bubbles" where they would be insulated from contrary perspectives". Content online is relayed with no significant third party filtering, fact checking or editorial judgement and this is especially true on social media where people give credibility to stories because they were shared by someone they follow. An individual with no track record can reach as many readers as Fox News, CNN or the NYT.

From previous studies it was found that 62% of US adults get news on social media and for 14% of US adults social media was the most important source of election news. Most popular fake news stories were more widely shared on Facebook than the most popular mainstream news stories. The consequence of this is, as the paper suggests and proves, that Donald Trump would not have been elected president were it not for the influence of fake news.

To study fake news the authors sketch a model of supply and demand for news based on a previously formally defined model where "Consumers may derive psychological utility from seeing reports that are consistent with their priors. Consumers choose the firms from which they will consume news in order to maximise their own expected utility. They then use the content of the news reports they have consumed to form a posterior about the state of the world. Consumers receive psychological utility from confirmatory news. When feedback about the true state is limited, rational consumers will judge a firm to be higher quality when its reports are closer to the consumers' priors. Consumers may prefer reports that confirm their priors due to psychological utility."

The paper proves that social media platforms are especially conductive to fake news. Facebook friend networks are ideologically separated. People are more likely to read and share news articles that are aligned with their ideological positions. This suggests that people who get their news from social media are less likely to receive evidence about the true state of the world that would counter an ideologically alligned but false story.

People who report that social media were their most important sources of election news were more likely both to correctly believe true headline and to incorrectly believe false headlines.

## WTF: The Who to Follow Service at Twitter ##
["WTF: The Who to Follow Service at Twitter"](http://stanford.edu/~rezab/papers/wtf_overview.pdf) Gupta, P. Goel, A. Lin, J. Sharma, A. Wang, D. Zadeh, R. Twitter, Inc. May 2013
WTF is the user recommendation service at Twitter. It suggests accounts the user might be interested in following based on shared interests, common connections and "a number of other factors". The two categories suggested profiles fall under are "similar to" and "interested in". The "similar to" category is used based on the homophily principle which is the tendency for individuals to bond with similar others. Converting new users into active users is a priority for social media services since user retention is strongly connected with the ability of the user to find communities to engage with. That's why the suggestion methods are prioritiezed towards new users. Making high-quality recommendations for new users is extremely challenging as they present a "cold start" problem - the network doesn't have much information about their interests they could dig into. If users are unable to find value in a service they are unlikely to return and that value is created by showing them content they'd most likely engage with. The algorithms for recommendations mentioned are Circle of Trust, SALSA and Real Graph.

- The circle of trust is a "primitive" in user recommendation and is just a personalized PageRank. This provides a basis for SALSA.
- SALSA uses a bipartite graph where on one side it puts ca 500 top-ranked nodes from a user's circle of trust and on the other it puts authorities which are profiles these 500 nodes follow creating a relationship between the two sides. The SALSA algorithm then assigns scores to both sides by a random walk and both sides are ranked by this score. Right hand side is then the standard "interested in" category whereas the left hand side ranking creates a group of "similar to you" profiles which are also suggested to the user.  
I.e. the profiles a user is shown are either profiles followed by many of user's current friends or profiles that are similar to the user. "A user u is likely to follow those who are followed by users that are similar to u."
- The Real Graph is a new approach possible because of distributing the graph with Hadoop. The Real Graph integrates user and behaviour features. Vertices represent users with metadata (#tweetss, #followers, #followings etc.) Edges represent relationships (follows, retweets, favourites, mentions etc or can add arbitrary weights). From this recommendations are computed in two phases:
    1. Candidate generation: produce a list of recommendations with many different algorithms, simple and complex (2-hop neighborhoods, personalized PageRanak, SALSA etc)
    2. Rescoring: apply an ML model to the candidate list. It's just a binary classification problem. The models are learned using the Pig-based framework. Logistic regression classifiers are trained using stochastic gradient descent in a single pass.

Recommendation information is used in search, content discovery, static priors in ranking etc.

## Thumbs up? Sentiment Classification using Machine Learning Techniques ##
["Thumbs up? Sentiment Classification using Machine Learning Techniques"](https://www.cs.cornell.edu/home/llee/papers/sentiment.pdf) Pang, B. Lee, L. Vaithyanathan, S. Proceedings of EMNLP 2002 79-86

- Prev research focused on __topical categorisation__
- Growth in on-line discussion groups and review sites -> sentiment categorisation.
- __Sentiment definition__: overall opinion towards the subject matter
- Paper focus: machine learning techniques to the sentiment classification problem.
- Challenges: more subtle than topic, require more understanding.
- Related research areas: source style, genre classification, sent. classification at least partially knowledge-based using linguistic heuristics or seed words. Closest prev research: unsupervised learning based on words "excellent" and "poor"
- Data: movie reviews. Good because have rating indicator
- Results applicable to other domains as long as __sufficient training data exists__
- Expert hypothesis: relatively low performance for automatic sentiment classification (relative to other text categorisation).
- Human-based classifiers: 58% and 64%, human-based + data analysis: 69%. So __baseline__ is 69%.
- Test NB, MaxEntr and SVM because they were successful in prev classifciers.
- Count vector to represent documents.
- Removing the negation tag had negligable, slightly harmful effect
- Features used: unigrams (occuring at least 4 times), top bigrams.
- Surpass random choice and human-based results
- Topic-based classifiers achiver 90% and above for particular categories with more than two classes -> sentiment anal more difficult than topic classification
- Tried improvements:
  - __feature frequence vs presence__: binarise the document vector. Much better performance. Opposite result to topic classification - difference.
  - __bigrams__: using uni + bi violates independence assumption of NB but doesn't imply NB will have poorer performance. For NB, uni+bi had negl. effect. If context is important, bigrams are not good at capturing it.
  - __POS tagging:__ word sense disambiguation. Improves perf slightly for NB but declines for SVM. Focus on adjectives - poor. But using fewer unigrams = acc when using all of them -> applying explicit feature-selection on unigrams could improve performance.
  - __Position__: position of sentiment in the text -> different meaning. But actually doesn't amke a difference, maybe need more refinement in text position.
- Relative performance: NB worst, SVM best.
- Not as good as topic categorisation.
- Unigram presence most effective, consistently better performance
- thwarted expectations narrative: thought it'll be great but wasn't.
- many words indicative of the opposite sentiemnt - discourse analysis necessary to decide when the author is talking about the film itself -> next step is whether sentences are on topic or not.

## Sentiment Analysis on Twitter Data ##
["Sentiment Analysis on Twitter Data"](http://www.cs.columbia.edu/~julia/papers/Agarwaletal11.pdf) Agarwal, A. Xie, B. Columbia University

- Introduce Twitter like the reader never heard about it: social networking and microblog, tweets 140/280 characters, acronyms, spelling mistakes, emoticons.
- Define: emoticons, target (reference), hashtag (topic)
- Three models all running on SVMs: unigram model (baseline), feature based model and tree kernel based model
- Design their own features called senti-features
- Feature based model with 100 features acc == acc of unigram with 10k features.
- Combinations of uni + features or uni + tree kernels outperform baseline.
- Twitter specific features marginally add value.
- Most important __combine prior polarity of words with their parts-of-speech tags__.
- Twitter API: gives actual tweets in terms of language and content
- Can get from them hand annotated dict of emojis and 5000 frequently used acronyms
- Data collection based on search queries is biased (they provide part of their data which is not)
- Preprocess:
  - emoticons -> polarity
  - urls -> url tag
  - targets -> target tags
  - negations -> negation tag
  - repeated characters -> three characters
  - Stanford tokenizer -> tokens
  - stop words -> mark as stop word
  - found in WordNet -> mark as english word
- Use prior polarity dictionary DAL and if word not found, use WordNet to find synonyms.
- Partial tree kernels: calculate similarity between trees by comparing all possible subtrees -> captures all possible correlations between features and categories. Takes a subtree and finds every possible combination of all or some of its elements.
- Kernel attempts to use full information, abstracts away from specific information
- Combining unigrams with senti-features best 2-class classification (4.04% gain over hard unigram baseline)
- All features other than prior polarity of part of speech have marginal role.
- URLs tend to be possitive (also in Go et al 2009), emoticons appear important
- Less data -> unigrams are a critical disadvantage
- Best performing system: combination of tree kernel with senti-features (4.25% gain over unigram baseline - same as 2-way class)
- Conclusion: Twitter not that diff from other genres
- Future work: parsing, semantic analysis, topic modelling

## Sentiment Analysis on Twitter ##
["Sentiment Analysis on Twitter"](https://www.ijcsi.org/papers/IJCSI-9-4-3-372-378.pdf) Kumar, A. Sebastian, T. M. Delhi Technological University, IJCSI, 2012, Vol. 9

- Hybrid approach: corpus based + dictionary based methods
- Twitter:
  - Microblogging valuable source of people's opinons: different people
  - Corpus can be arbitrarily large
  - Differnt social and interests groups
  - Many countries
- NB works much better than MaxEntr (Parikh and Movassate)
- Emoticons as fuzzy lables (Go et al and Read): NB, MaxEnt, SVM with unigrams, bigrams and POS = SVM + unigrams
- Objective positive and negative tweet class (Pak and Paroubek)
- 60 mil tweet dataset trained showed stochastic gradient descent is best (Batra and Rao)
- Features that combine prior polarity of words with their pos are most important (Agarwal et al)
- Hybrid: dicrionary + corpus based approach NLP + ML algorithms
- twitter unique characteristics:
  - message length
  - writing technique: cyber slang, spelling, acronyms, emoticons
  - availability
  - topics
  - real time
- terminology:
  - emoticons: facial expression representation
  - target: refer
  - hash tags: topic
  - special symbols: rt - repeat
- architecture: extract opinon words, find their orientation. Adjectives and verbs+adverbs. Corpus based method - find the semantic orientation of adjectives. Dictionary based method to find semantic orientation of verbs and adverbs. Calculate overall tweet sentiment through linear equation with emotion intensifiers (punctuation, repetition)
- describe preprocessing
- adjective: domain specific, use corpus, verbs: not domain specific, use seedlist + synonyms from wordnet)
- no results reported in the paper???
