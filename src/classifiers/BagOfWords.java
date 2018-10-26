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

    public HashMap<Integer, Sentiment> runClassifier(HashMap<Integer, String> tweets){
        HashMap<Integer, Sentiment> predictedSentiments = new HashMap<>();
        for(Map.Entry<Integer, String> entry : tweets.entrySet()){
            predictedSentiments.put(entry.getKey(), predictTweetSentiment(entry.getValue()));
        }
        return predictedSentiments;
    }

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
