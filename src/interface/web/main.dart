import 'dart:convert';
import 'dart:html';
import 'dart:math';

SelectElement topicInput;
DivElement loading;
ParagraphElement progress;
DivElement instructions;
ParagraphElement studyDescription;
ParagraphElement result;

List<Argument> positiveArguments;
List<Argument> negativeArguments;
List<Argument> chosenArguments = [];
List<Argument> unchosenArguments = [];
Map<String, Argument> arguments;

Argument randomArgument;

TableElement argumentTable;
TableElement resultTable;

int rowCount = 0;
int posScore = 0;

String topic;

class Argument{
  String tweet;
  bool isNeg;
  bool isRand;
  List<String> support;
  var class_prob;
  var word_probs;

  Map toJsonMap(){
    return {
      "tweet": tweet,
      "negative": isNeg.toString(),
      "random": isRand.toString(),
      "support": support.toString(),
      "class_prob": class_prob.toString(),
      "word_probs" : word_probs.toString()
    };
  }
}

void main() {
  // Run an interactive debate on a topic based on tweets.
  loading = querySelector("#loading");
  result = querySelector("#result");
  topicInput = querySelector('#topic');
  topicInput.onChange.listen(changeTopic);
  argumentTable = querySelector("#argTable");
  resultTable = querySelector("#resultTable");
  progress = querySelector("#progress");
  instructions = querySelector("#instructions");
  studyDescription = querySelector("#study-description");
}

// Interface methods

void changeTopic(Event e){
  // Responds to new topic choice.
  topic = topicInput.value;
  print("New topic: ${topic}");

  resultTable.children.clear();
  result.children.clear();
  argumentTable.children.clear();
  instructions.children.clear();
  progress.text = "";

  chosenArguments = [];
  unchosenArguments = [];
  rowCount = 0;
  posScore = 0;
  requestRandomArgument();
}

void makeSelection(Event e){
  // Responds to user's debate choice.
  rowCount++;
  ButtonElement selectedArgument = e.target;
  if((selectedArgument.id == "pos") || (selectedArgument.id == "neg")) {
    if (selectedArgument.id == "pos") {
      posScore++;
    }

    List<TableRowElement> rows = argumentTable.rows;
    TableRowElement lastArgRow = rows.elementAt(rows.length - 2);
    for (var cell in lastArgRow.cells) {
      if(cell.children[0].id == selectedArgument.id){
        cell.children[0].id = "chosen-clicked";
        chosenArguments.add(arguments[selectedArgument.text]);
      }
      else {
        unchosenArguments.add(arguments[cell.children[0].text]);
        cell.children[0].id = "clicked";
      }
    }

    if (rowCount % 3 == 0) {
      moveToNextPage();
    }
    addArgumentRow();
  }
}

void addArgumentRow(){
  progress.text = "Page ${((rowCount + 1)/3).ceil()} / ${(arguments.length/6).ceil()}";
  // Displays next row of arguments in the debate.
  if(rowCount != 0 && rowCount %  3 != 0){
    argumentTable.deleteRow(-1);
  }
  if(negativeArguments.isNotEmpty && positiveArguments.isNotEmpty) {
    TableRowElement opinionRow = argumentTable.addRow();
    var negArg = negativeArguments.removeLast();
    var posArg = positiveArguments.removeLast();
    opinionRow.addCell()
      ..colSpan = 3
      ..children.add(new ButtonElement()
        ..text = negArg.tweet
        ..onClick.listen(makeSelection)
        ..onMouseOver.listen(displaySupport)
        ..onMouseOut.listen(hideSupport)
        ..id = "neg");
    opinionRow.addCell()
      ..colSpan = 3
      ..children.add(new ButtonElement()
        ..text = posArg.tweet
        ..onClick.listen(makeSelection)
        ..onMouseOver.listen(displaySupport)
        ..onMouseOut.listen(hideSupport)
        ..id = "pos");

    TableRowElement supportRow = argumentTable.addRow();
    supportRow.id = "support";
    int i = 0;
    for (var arg in [negArg, posArg]) {
      for (var sup in arg.support) {
        supportRow.addCell()
          ..text = sup
          ..id = i < 3 ? "neg-sup" : "pos-sup";
        i++;
      }
    }
  }
  else{
    displayResultScreen();
  }
}

void displaySupport(Event e){
  // Display the supporting argument on hover.
  ButtonElement hoveredArgument = e.target;
    TableRowElement lastRow = argumentTable.rows.elementAt(argumentTable.rows.length - 1);
    for(var cell in lastRow.cells){
      if(cell.id == "${hoveredArgument.id}-sup"){
        cell.id = "${hoveredArgument.id}-sup-visible";
      }
  }
}

void hideSupport(Event e){
  // Display the supporting argument on hover.
  ButtonElement hoveredArgument = e.target;
  TableRowElement lastRow = argumentTable.rows.elementAt(argumentTable.rows.length - 1);
  for(var cell in lastRow.cells){
    if(cell.id == "${hoveredArgument.id}-sup-visible"){
      cell.id = "${hoveredArgument.id}-sup";
    }
  }
}

void moveToNextPage(){
  // Clears the interface from previous arguments and adds a bar on top meaning
  // to give the pages a connected structure.
  argumentTable.children.clear();
  for(var i = 0; i < rowCount / 3; i++) {
    var row = argumentTable.addRow();
    row.addCell()
      ..id="prev-page"
      ..colSpan=6
      ..children.add(new ParagraphElement()..text =
          "${i+1} / ${(arguments.length/6).ceil()} completed");
    print("Added row");
  }
}

void displayResultScreen(){
  // Presents final interface with debate results.
  progress.text = "";
  writeResultsToFile();
  argumentTable.children.clear();
  result.children.add(new ParagraphElement()
                        ..text = "Topic: ${topic}");
  result.children.add(new ParagraphElement()
                        ..text = "Positive choices: ${posScore}");
  result.children.add(new ParagraphElement()
                        ..text = "Negative choices: ${rowCount-posScore}");
  resultTable.addRow()
    ..addCell().text = "Chosen tweet"
    ..addCell().text = "Not chosen tweet";

  for(var i = 0; i < chosenArguments.length; i++){
    var row = resultTable.addRow();
    for(var arg in [chosenArguments[i], unchosenArguments[i]]) {
      TableCellElement cell = row.addCell()
          ..text = arg.tweet;
      if(arg.isRand){
        cell.id = "random-argument";
      }
      else {
        if (chosenArguments.contains(arg)) {
          if (arg.isNeg) {
            cell.id = "negative-result";
          } else {
            cell.id = "positive-result";
          }
        }
      }
    }
  }
}

int compareWordProbs(double probA, double probB){
  if(probA > probB){
    return -1;
  }else{
    if(probA == probB){
      return 0;
    }else{
      return 1;
    }}
}

void addLoadingText(String displayText){
  loading.children.add(new ParagraphElement()
                        ..text = displayText);
}

void clearLoadingText(){
  loading.children.clear();
}

void setInstructions(){
  studyDescription.id = "hidden";
  instructions.children.add(new ParagraphElement()..text="1. Select a topic from the drop down menu.");
  instructions.children.add(new ParagraphElement()..text="2. At each step, select the tweet you agree with most.");
  instructions.children.add(new ParagraphElement()..text="3. Hover over arguments to display their context tweets.");
}

void writeResultsToFile(){
  var now = new DateTime.now();
  var date = "${now.hour}-${now.minute}-${now.day}-${now.month}-${now.year}";
  String filename = "${topic}-${date}.json";

  var jsonData = {"chosen_args":[],
                  "unchosen_args":[]};

  print("Unchosen: ${unchosenArguments}, Chosen:${chosenArguments}");
  for(var argument in chosenArguments){
    jsonData["chosen_args"].add(argument.toJsonMap());
  }
  for(var argument in unchosenArguments){
    jsonData["unchosen_args"].add(argument.toJsonMap());
  }

  Map<String, String> encodedJson = {"chosen_args": "", "unchosen_args": ""};
  encodedJson["chosen_args"] = jsonEncode(jsonData["chosen_args"]);
  encodedJson["unchosen_args"] = jsonEncode(jsonData["unchosen_args"]);

  HttpRequest
      .postFormData(
        "http://127.0.0.1:5000/results/${filename}", encodedJson);
}


//  Argument methods
void requestArguments() {
  // Requests arguments from a local server running the Python spectrum scripts.
  addLoadingText("Sending response to server...");
  HttpRequest
    .getString("http://127.0.0.1:5000/spectrum/${topic}")
    .then((String jsonContents){
      addLoadingText("Received responses.");
      addLoadingText("Creating argument list...");
      createArgumentLists(jsonDecode(jsonContents));
      addLoadingText("Done.");
      clearLoadingText();
      setInstructions();
      addArgumentRow();
  })
    .catchError((Error error){
      print(error.toString());
  });
  addLoadingText("Conntacting Twitter API...");
}

void requestRandomArgument(){
  HttpRequest
    .getString("http://127.0.0.1:5000/random/${topic}")
    .then((String jsonContents){
      print(jsonContents);
      randomArgument = jsonToArgument(jsonDecode(jsonContents));
      randomArgument.isRand = true;
      print(randomArgument.toJsonMap());
      requestArguments();
  })
    .catchError((Error error){
      print(error.toString());
  });
}

void createArgumentLists(var jsonArguments) {
  // Decodes arguments from server response and places them in their lists.
  positiveArguments = new List<Argument>();
  negativeArguments = new List<Argument>();
  arguments = new Map();
  // First element in the list is the number of arguments each side has.
  for(var jsonArgument in jsonArguments){
    var argument = jsonToArgument(jsonArgument);

    if(argument.isNeg){
      negativeArguments.add(argument);
    }else{
      positiveArguments.add(argument);
    }

    argument.isRand = false;
    arguments.putIfAbsent(argument.tweet, () => argument);
  }
  var random = new Random();
  int randomIndex = random.nextInt(arguments.length);
  var removedTweet = arguments.keys.elementAt(randomIndex);
  var removedArg = arguments[removedTweet];
  arguments.remove(removedTweet);

  arguments.putIfAbsent(randomArgument.tweet, () => randomArgument);

  var listRemoved;
  if(removedArg.isNeg){
    listRemoved = negativeArguments;
  }
  else{
    listRemoved = positiveArguments;
  }
  var removedIndex = listRemoved.indexOf(removedArg);
  listRemoved.removeAt(removedIndex);
  listRemoved.insert(removedIndex, randomArgument);
}

Argument jsonToArgument(var jsonArgument){
  var argument = new Argument();

  // Text
  argument.tweet = jsonArgument["tweet"];

  // Is tweet negative.
  if(jsonArgument["negative"]){
      argument.isNeg = true;
    }else{
      argument.isNeg = false;
  }

  // Supporting arguments
  var support = jsonArgument["support"];
  List<String> supportArgs = new List<String>();
  for(var s in support){
    supportArgs.add(s);
  }
  argument.support = supportArgs;

  // Class probability.
  argument.class_prob = jsonArgument["class_prob"];

  // Word probabilities.
  var word_probs_dict = jsonArgument["word_probs"];
  var keys = word_probs_dict.keys.toList();
  Map<String, double> word_probs = new Map();
  for(var key in keys){
    word_probs.putIfAbsent(key, () => word_probs_dict[key]);
  }
  argument.word_probs = word_probs;

  return argument;
}