package test;

import utils.Sentiment;

import java.util.HashMap;
import java.util.Map;

public class Evaluator {
    /**
     * Accuracy*/
    public double accuracy(HashMap<Integer, Sentiment> trueSentiments, HashMap<Integer, Sentiment> predictedSentiments){
        double correct = 0, incorrect = 0;
        for(Map.Entry<Integer, Sentiment> trueSentiment : trueSentiments.entrySet()){
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
     * Positive and negative recall.
     * (Well predicted sentiment) / (True count of that sentiment)
     * @param trueSentiments real sentiments
     * @param predictedSentiments sentiments the model predicted
     * @param recallSentiment sentiment for which recall is calculated
     * */
    public double recall(HashMap<Integer, Sentiment> trueSentiments, HashMap<Integer, Sentiment> predictedSentiments, Sentiment recallSentiment){
        double truePosCount = 0, predictedCorrectPosCount = 0;
        for(Map.Entry<Integer, Sentiment> trueSentiment : trueSentiments.entrySet()){
            if(trueSentiment.getValue().compareTo(recallSentiment) == 0){
                truePosCount++;
                if(predictedSentiments.get(trueSentiment.getKey()).compareTo(recallSentiment) == 0){
                    predictedCorrectPosCount++;
                }
            }
        }

        return predictedCorrectPosCount/truePosCount;
    }


}
