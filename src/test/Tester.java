package test;

import classifiers.BagOfWords;
import javafx.util.Pair;
import utils.DataPreparation;
import utils.Sentiment;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class Tester {
    public static void main(String [] args){
        Path dataDir = Paths.get("/home/aga/work/ii/dissertation/code/data/");

        Path anonymizedTrainingDataFile = Paths.get(dataDir.toString(), "stanford_training_anonymized.csv");
        Path anonymizedTestingDataFile = Paths.get(dataDir.toString(), "stanford_testing_anonymized.csv");
        Path tweetsMapFile = Paths.get(dataDir.toString(), "TweetMap.ser");
        Path sentimentMapFile = Paths.get(dataDir.toString(), "SentimentMap.ser");
        Path smallTweetsMapFile = Paths.get(dataDir.toString(), "SmallTweetMap.ser");
        Path smallSentimentMapFile = Paths.get(dataDir.toString(), "SmallSentimentMap.ser");
        Path lexiconFile = Paths.get(dataDir.toString(), "Lexicon.ser");


        Pair<HashMap<Integer, String>, HashMap<Integer, Sentiment>> maps = DataPreparation.loadTweetsWithSentiments(anonymizedTestingDataFile);
        HashMap<Integer, String> testingTweets = maps.getKey();
        HashMap<Integer, Sentiment> testingSentiments = maps.getValue();
        HashMap<Integer, Sentiment> predictionSentiments;

        BagOfWords bow = new BagOfWords(lexiconFile);
        predictionSentiments = bow.runClassifier(testingTweets);
        Evaluator eval = new Evaluator();
        double acc = eval.accuracy(testingSentiments, predictionSentiments);
        double posRecall = eval.recall(testingSentiments, predictionSentiments, Sentiment.POSITIVE);
        double negRecall = eval.recall(testingSentiments, predictionSentiments, Sentiment.NEGATIVE);

        System.out.printf("Accuracy: %.3f\nPositive Recall: %.3f\nNegative Recall: %.3f", acc, posRecall, negRecall);
    }

    private static <T, D> void printMap(HashMap<T, D> map, int numberOfPrints){
        System.out.println(String.format("Map print for %d elements", numberOfPrints));
        int count = 0;
        for(Map.Entry<T, D> entry : map.entrySet()){
            if(count >= numberOfPrints){
                break;
            }

            System.out.printf("%s: %s\n", entry.getKey().toString(), entry.getValue().toString());
            System.out.println();

            count++;
        }
        System.out.println("---");
    }
}
