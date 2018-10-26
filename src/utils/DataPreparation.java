package utils;

import javafx.util.Pair;

import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class DataPreparation {
    /**
     * Tokenizes tweets into valid strings.
     * @param tweet message to be tokenized
     * @return tokens
     * */
    public static ArrayList<String> splitText(String tweet){
        ArrayList<String> words = new ArrayList<>();
        tweet = spaceCharacters(tweet);
        tweet = tweet.replaceAll("(.)\\1{2,}","$1$1");
        String [] tokens = tweet.split("\\s+");
        Arrays.stream(tokens).forEach(token ->{

            // Only accepting tokens which are longer than one character and don't contain slashes (most prob urls).
            if((token.length() > 1 && !token.contains("/"))){
                words.add(token.toLowerCase());
            }
        });

        return words;
    }

    /**
     * Helper function adding white space around punctuation characters.
     * @param tweet word to be spaced out
     * @return spaced out word
     * */
    private static String spaceCharacters(String tweet){
        String [] expandedChars = {"\\.", ",", "\\(", "\\)", "\\[", "\\]", "&", "\"", ":", ";", "!", "\\?", "-", "#", "\\+", "'"};
        for(String search : expandedChars){
            tweet = tweet.replaceAll(search, String.format(" %s ", search));
        }
        return tweet;
    }


    /**
     * Prepares a small dataset of specified size which can be used during development.
     * @param dataFile csv file from which the data is taken
     * @param numberOfEntries number of entries in the small set
     * @param outputDir where the small sets will be saved to when serialized
     * */
    public static void prepareSmallDataset(Path dataFile, int numberOfEntries, Path outputDir){
        Pair<HashMap<Integer, String>, HashMap<Integer, Sentiment>> maps = loadTweetsWithSentiments(dataFile);
        Path tweetsOutputPath = Paths.get(outputDir.toString(), "SmallTweetMap.ser");
        Path sentimentsOutputPath = Paths.get(outputDir.toString(), "SmallSentimentMap.ser");

        HashMap<Integer, String> smallTweetMap = new HashMap<>();
        HashMap<Integer, Sentiment> smallSentimentMap = new HashMap<>();

        for(int i = 0; i < numberOfEntries; i++){
            smallTweetMap.put(i, maps.getKey().get(i));
            smallSentimentMap.put(i, maps.getValue().get(i));
        }

        serializeMap(smallTweetMap, tweetsOutputPath);
        serializeMap(smallSentimentMap, sentimentsOutputPath);
    }


    /**
     * Loads a serialized hashmap.
     * The hashmap has to be indexed with an integer but can point to any serializable value.
     * @param mapFile serialized file the map is constructed from
     * @return reconstructed hashmap
     * */
    public static <T, D> HashMap<T, D> loadSerializedMap(Path mapFile){
        HashMap<T, D> map = null;
        try
        {
            FileInputStream fis = new FileInputStream(mapFile.toFile());
            ObjectInputStream ois = new ObjectInputStream(fis);
            map = (HashMap) ois.readObject();
            ois.close();
            fis.close();

        }catch(IOException ioe)
        {
            System.err.println("Error loading the tweets hashmap.");
            ioe.printStackTrace();
            System.exit(-1);
        }catch(ClassNotFoundException c)
        {
            System.err.println("Class not found when reading the tweets hashmap.");
            c.printStackTrace();
            System.exit(-1);
        }
        return map;
    }

    /**
     * Serializes HashMaps created based on the dataFile for quicker loading and less file IO when rerunning.
     * @param dataFile anonymized file where data is taken from for the hashmaps.
     * @param outputDir directory in which the serialized map files are stored.
     */
    public static void serializeAllData(Path dataFile, Path outputDir){
        Pair<HashMap<Integer, String>, HashMap<Integer, Sentiment>> maps = loadTweetsWithSentiments(dataFile);
        HashMap<Integer, String> tweets = maps.getKey();
        HashMap<Integer, Sentiment> sentiments = maps.getValue();

        Path outputTweetsFile = Paths.get(outputDir.toString(), "TweetMap.ser");
        Path outputSentimentFile = Paths.get(outputDir.toString(), "SentimentMap.ser");

        serializeMap(tweets, outputTweetsFile);
        serializeMap(sentiments, outputSentimentFile);
    }

    /**
     * Serializes a given (generic) map.
     * @param map hashmap to be serialized
     * @param outputPath path to file where the serialization stream is saved
     */
    public static <T, D> void serializeMap(HashMap<T, D> map, Path outputPath){
        try
        {
            // Serialize tweet map.
            FileOutputStream fos = new FileOutputStream(outputPath.toFile());
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            oos.writeObject(map);
            oos.close();
            fos.close();
        }catch(IOException ioe)
        {
            System.err.println("Couldn't serialize the maps.");
            System.exit(-1);
        }
    }

    /**
     * Creates a new csv file based on the passed csv file whose data is stripped of personal information.
     * The method removes the author username, timestamp, gives the tweet a new id and
     * replaces all @-mentions with "@USERNAME".
     * @param dataFile Original dataset to be anonymized.
     * */
    public static void anonymizeData(Path dataFile){
        try{
            // Make sure the anonymized file exists.
            File anonymizedDataFile = new File(dataFile.toString().replace(".csv", "_anonymized.csv"));
            anonymizedDataFile.createNewFile(); // Does nothing if exists.

            PrintWriter writer = new PrintWriter(anonymizedDataFile, "UTF-8");
            // For each line remove date, user and replace all usernames with @USERNAME. Store in new file.
            BufferedReader reader = new BufferedReader(
                                        new InputStreamReader(
                                            new FileInputStream(dataFile.toFile()),"utf-8"));

            AtomicInteger newID = new AtomicInteger(0);
            reader.lines().forEach(line -> {
                if(line.startsWith("\"")){
                    // Need to deal with escape chars inside tweets.
                    String [] tokens = line.split(",");
                    String tweetMessage = putMessageTogether(tokens, false);

                    if(tweetMessage.contains("@")){
                        tweetMessage = tweetMessage.replaceAll("@(\\w|\\d|_)+", "@USERNAME");
                    }
                    String newLine = String.format("%s,%s,%s,%s\n",
                                                    tokens[0], newID.getAndIncrement(), tokens[3], tweetMessage);
                    writer.write(newLine);
                    writer.flush();
                }
            });
            writer.flush();

        } catch(IOException e){
            System.err.println("Problem opening files.");
            System.exit(-1);
        }

    }

    /**
     * Loads data from the anonymized csv and parses it to internal representation.
     * @param dataFile The file to load data from. The method assumes the file is anonymized.
     * @return a Pair of two hashmaps. The first hashmap has Tweet IDs as keys and the Tweet content as values.
     * The second hashmap has Tweet IDs as keys and sentiment enums as values.*/
    public static Pair<HashMap<Integer, String>, HashMap<Integer, Sentiment>>
                                                            loadTweetsWithSentiments(Path dataFile){
        HashMap<Integer, String> tweets = new HashMap<>();
        HashMap<Integer, Sentiment> sentiments = new HashMap<>();

        try(BufferedReader reader = new BufferedReader(
                                        new InputStreamReader(
                                            new FileInputStream(dataFile.toFile()),"utf-8"))){

            reader.lines().forEach(line -> {
                if(line.startsWith("\"")){
                    String [] tokens = line.split(",");
                    String message = putMessageTogether(tokens, true);

                    int id = Integer.parseInt(tokens[1].replaceAll("\"", ""));
                    tweets.put(id, message);

                    int sentiment = Integer.parseInt(tokens[0].replaceAll("\"", ""));
                    if(sentiment == 0){
                        sentiments.put(id, Sentiment.NEGATIVE);
                    }else{
                        sentiments.put(id, sentiment == 2 ? Sentiment.NEUTRAL : Sentiment.POSITIVE);
                    }
                }
            });

        }catch(IOException e){
            System.err.println("Problem loading tweets.");
            System.exit(-1);
        }

        return new Pair<>(tweets, sentiments);
    }

    /**
     * Helper function to stitch back the message which contains "," after it's been split by reading the csv.
     * @param tokens Tokens read from the csv line we're reconstructing the message from
     * @return message of this tweet
     * */
    private static String putMessageTogether(String [] tokens, boolean isAnonymized){
        String message = "";
        int msgInd = isAnonymized ? 3 : 5;
        for(int i = msgInd; i < tokens.length; i++){
            message = message.concat(tokens[i]);
        }
        return message;
    }
}
