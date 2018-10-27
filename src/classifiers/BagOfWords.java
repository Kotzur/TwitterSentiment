package classifiers;

import javafx.util.Pair;
import utils.DataPreparation;
import utils.Sentiment;

import javax.xml.crypto.Data;
import java.io.IOException;
import java.nio.file.Path;
import java.util.*;

public class BagOfWords {
    private HashSet<String> allWords;

    private HashMap<String, Integer> negativeCount;
    private HashMap<String, Integer> positiveCount;
    private HashMap<String, Sentiment> lexicon;

    private HashMap<Integer, String> tweets;
    private HashMap<Integer, Sentiment> tweetSentiments;

    private int neutralThreshold = 0;

    public BagOfWords(Path tweetMapFile, Path sentimentMapFile){
        allWords = new HashSet<>();
        negativeCount = new HashMap<>();
        positiveCount = new HashMap<>();
        lexicon = new HashMap<>();

        tweets = DataPreparation.loadSerializedMap(tweetMapFile);
        tweetSentiments = DataPreparation.loadSerializedMap(sentimentMapFile);
    }

    public BagOfWords(Path lexiconFile){
        allWords = new HashSet<>();
        negativeCount = new HashMap<>();
        positiveCount = new HashMap<>();
        lexicon = DataPreparation.loadSerializedMap(lexiconFile);
    }

    /**
     * Run prediction on the given tweets.
     * If the lexicon hasn't been created, run the necessary steps to do so. Then for every tweet, find its sentiment.
     * @param tweets messages to be classified
     * @return map of tweet id to its predicted sentiment.
     * */
    public HashMap<Integer, Sentiment> runClassifier(HashMap<Integer, String> tweets){
        if(lexicon.size() == 0){
            countSentiments();
            createLexicon();
        }

        HashMap<Integer, Sentiment> predictedSentiments = new HashMap<>();
        for(Map.Entry<Integer, String> entry : tweets.entrySet()){
            predictedSentiments.put(entry.getKey(), predictTweetSentiment(entry.getValue()));
        }
        return predictedSentiments;
    }

    /**
     * Predict sentiment of the given string based on the lexicon.
     * Calculate the score of a message by calculating the numbers of positive and negative words it contains.
     * @param tweet string examined.
     * @return prediction of sentiment for the passed tweet
     * */
    public Sentiment predictTweetSentiment(String tweet){
        ArrayList<String> tokens = DataPreparation.splitText(tweet);
        int score = 0;
        for(String token : tokens){
            if(lexicon.containsKey(token)) {
                score += (lexicon.get(token) == Sentiment.POSITIVE) ? 1 : -1;
            }
        }

        if(score >= neutralThreshold){
            return Sentiment.POSITIVE;
        }else{
            return (score <= neutralThreshold - Math.abs(neutralThreshold)) ? Sentiment.NEGATIVE : Sentiment.NEUTRAL;
        }
    }

    /**
     * Counts occurances of words in negative and positive texts.
     * This needs to be run before lexicon building.
     */
    public void countSentiments(){
        int id;
        String tweet;
        Sentiment sent;
        HashMap<String, Integer> sentimentCountMap = null;
        for(Map.Entry<Integer, String> entry : tweets.entrySet()){
            id = entry.getKey();
            tweet = entry.getValue();
            sent = tweetSentiments.get(id);

            switch(sent){
                case POSITIVE:
                    sentimentCountMap = positiveCount;
                    break;
                case NEGATIVE:
                    sentimentCountMap = negativeCount;
                    break;
            }

            ArrayList<String> tokens = DataPreparation.splitText(tweet);
            for(String token : tokens){
                addTokenToMap(token, sentimentCountMap);
                allWords.add(token);
            }
        }
    }

    /**
     * Create the lexicon map after the sentiment counting maps are complete.
     * Based on the maps, the lexicon calculates a score for each word present in the training set and assigns
     * it a sentiment based on it.
     */
    public void createLexicon(){
        int posCount;
        int negCount;
        int score;
        for(String word : allWords){
            posCount = positiveCount.getOrDefault(word, 0);
            negCount = negativeCount.getOrDefault(word, 0);
            score = posCount - negCount;

            // System.out.printf("For %s we have %d positive %d negative so the score is %d\n", word, posCount, negCount, score);

            if(score >= 0){
                lexicon.put(word, Sentiment.POSITIVE);
            }else{
                lexicon.put(word, Sentiment.NEGATIVE);
            }
        }
        // System.out.println("-----");
    }

    /**
     * Helper function grouping the actions needed whenever a token is added to a map.
     * Checks whether the item is present in the map and increments its count or initializes it.
     * @param token item added
     * @param map data structure added to
     */
    private void addTokenToMap(String token, HashMap<String, Integer> map){
        if(map.containsKey(token)){
            map.replace(token, map.get(token) + 1);
        }else{
            map.put(token, 1);
        }
    }

    public HashSet<String> getAllWords() {
        return allWords;
    }

    public HashMap<String, Integer> getNegativeCount() {
        return negativeCount;
    }

    public HashMap<String, Integer> getPositiveCount() {
        return positiveCount;
    }

    public HashMap<String, Sentiment> getLexicon() {
        return lexicon;
    }

    public void setLexicon(HashMap<String, Sentiment> lexicon) {
        this.lexicon = lexicon;
    }
}
