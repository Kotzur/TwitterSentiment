package test;

import utils.Sentiment;

import java.util.HashMap;
import java.util.Map;

public class Evaluator {
    /**
     * Accuracy
     * (Correctly labelled things) / (Everything)
     * @param realSentiments actual sentiments of the tweets
     * @param predictedSentiments sentiments the model predicted
     * @return accuracy
     * */
    public double accuracy(HashMap<Integer, Sentiment> realSentiments, HashMap<Integer, Sentiment> predictedSentiments){
        double correct = 0, incorrect = 0;
        for(Map.Entry<Integer, Sentiment> trueSentiment : realSentiments.entrySet()){
            if(trueSentiment.getValue().compareTo(predictedSentiments.get(trueSentiment.getKey())) == 0){
                correct++;
            }
            else{
                incorrect++;
            }
        }
        return correct / (correct + incorrect);
    }

    /**
     * Number of correct target results divided by the number of all
     * relevant samples (all samples that should have been identified as target sentiment).
     * @param realSentiments actual sentiments
     * @param predictedSentiments sentiments the model predicted
     * @param targetSentiment sentiment for which recall is calculated
     * @return recall for chosen sentiment
     * */
    public double recall(HashMap<Integer, Sentiment> realSentiments, HashMap<Integer, Sentiment> predictedSentiments, Sentiment targetSentiment){
        return recallAndPrecisionCalculator(realSentiments, predictedSentiments, targetSentiment, false);
    }

    /**
     * Number of correct target results divided by the number of all target results returned by the classifier.
     * @param realSentiments actual sentiments
     * @param predictedSentiments sentiment given by a model
     * @param targetSentiment sentiment in question
     * @return precision of target sentiment.
     * */
    public double precision(HashMap<Integer, Sentiment> realSentiments, HashMap<Integer, Sentiment> predictedSentiments, Sentiment targetSentiment){
        return recallAndPrecisionCalculator(realSentiments, predictedSentiments, targetSentiment, true);
    }

    /**
     * Function for precision and recall.
     * Precision and recall are very similarly calculated measures. The only difference is what the ratio of well
     * assigned class is taken with respect to: number of actual items of that class (recall) or number of items that
     * have been assigned that class (precision). To make the distinction, the function takes in a boolean value whether
     * this calculation is of precision or recall which determines in what relation the maps are used.
     * @param realSentiments actual sentiments
     * @param predictedSentiments sentiments given by the model
     * @param targetSentiment sentiment examined
     * @param precision is this the precision calculation. If not, it's recall.
     * @return precision or recall depending on the arguments passed.
     * */
    private double recallAndPrecisionCalculator(HashMap<Integer, Sentiment> realSentiments, HashMap<Integer, Sentiment> predictedSentiments, Sentiment targetSentiment, boolean precision){
        HashMap<Integer, Sentiment> totalSentiment = realSentiments, matchingSentiment = predictedSentiments;
        if(precision){
            totalSentiment = predictedSentiments;
            matchingSentiment = realSentiments;
        }

        double totalCount = 0, predictedCorrectSentCount = 0;
        for(Map.Entry<Integer, Sentiment> total : totalSentiment.entrySet()){
            if(total.getValue().compareTo(targetSentiment) == 0){
                totalCount++;
                if(matchingSentiment.get(total.getKey()).compareTo(targetSentiment) == 0){
                    predictedCorrectSentCount++;
                }
            }
        }

        return predictedCorrectSentCount / totalCount;
    }

    /**
     * Harmonic average of the precision and recall. Reaches its best at 1 and worst at 0.
     * @param realSentiments actual sentiments
     * @param predictedSentiments sentiment given by a model
     * @param targetSentiment sentiment in question
     * @return F-Score
     */
    private double fscore(HashMap<Integer, Sentiment> realSentiments, HashMap<Integer, Sentiment> predictedSentiments, Sentiment targetSentiment){
        double precision = precision(realSentiments, predictedSentiments, targetSentiment);
        double recall = recall(realSentiments, predictedSentiments, targetSentiment);
        return 2 * (precision * recall) / (precision + recall);
    }

}
