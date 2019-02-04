import 'dart:html';
import 'dart:convert';

InputElement topicInput;
ParagraphElement loading;
List<Argument> positiveArguments;
List<Argument> negativeArguments;
List<Argument> chosenArguments = [];
List<Argument> unchosenArguments = [];
Map<String, Argument> arguments;

TableElement argumentTable;
TableElement resultTable;

int rowCount = 0;
int posScore = 0;

String topic;

class Argument{
  String tweet;
  bool isNeg;
  List<String> support;
  var class_prob;
  var word_probs;
}

void main() {
  // Run an interactive debate on a topic based on tweets.
  loading = querySelector("#loading");
  topicInput = querySelector('#topic');
  topicInput.onChange.listen(changeTopic);
  argumentTable = querySelector("#argTable");
  resultTable = querySelector("#resultTable");
}

// Interface methods

void changeTopic(Event e){
  // Responds to new topic choice.
  topic = topicInput.value;
  print("New topic: ${topic}");
  restartTables();
  requestArguments();
  rowCount = 0;
  posScore = 0;
}

void addArgumentRow(){
  // Displays next row of arguments in the debate.
  if(rowCount != 0){
    argumentTable.deleteRow(-1);
  }
  if(negativeArguments.isNotEmpty && positiveArguments.isNotEmpty) {
    TableRowElement opinionRow = argumentTable.insertRow(-1);
    var negArg = negativeArguments.removeLast();
    var posArg = positiveArguments.removeLast();
    opinionRow.insertCell(0)
      ..colSpan = 3
      ..children.add(new ButtonElement()
        ..text = negArg.tweet
        ..onClick.listen(makeSelection)
        ..onMouseOver.listen(displaySupport)
        ..onMouseOut.listen(hideSupport)
        ..id = "neg");
    opinionRow.insertCell(1)
      ..colSpan = 3
      ..children.add(new ButtonElement()
        ..text = posArg.tweet
        ..onClick.listen(makeSelection)
        ..onMouseOver.listen(displaySupport)
        ..onMouseOut.listen(hideSupport)
        ..id = "pos");

    TableRowElement supportRow = argumentTable.insertRow(-1);
    supportRow.id = "support";
    int i = 0;
    for (var arg in [negArg, posArg]) {
      for (var sup in arg.support) {
        supportRow.insertCell(i)
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
      restartTables();
    }
    addArgumentRow();
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

void restartTables(){
  // Clears the interface from previous arguments.
  argumentTable.children.clear();
  resultTable.children.clear();
}

void displayResultScreen(){
  // Presents final interface with debate results.
  restartTables();
  loading.text = "You are ${(posScore / rowCount * 100).round()}% pro ${topic}\nPositive choices: ${posScore}\nNegative choices: ${rowCount-posScore}";
  resultTable.addRow()
    ..addCell().text = "Chosen tweet"
    ..addCell().text = "Sentiment"
    ..addCell().text = "Confidence"
    ..addCell().text = "Feature log probabilities"
    ..addCell().text = "Not chosen tweet"
    ..addCell().text = "Sentiment"
    ..addCell().text = "Confidence"
    ..addCell().text = "Feature log probabilities";

  print("Chosen arg length ${chosenArguments.length}");
  print("Row count ${rowCount}");
  print("Unchosen agr length ${unchosenArguments.length}");

  for(var i = 0; i < chosenArguments.length; i++){
    var row = resultTable.addRow();
    for(var arg in [chosenArguments[i], unchosenArguments[i]]) {
      row.addCell().text = arg.tweet;
      row.addCell().text = arg.isNeg ? "Negative" : "Positive";
      row.addCell().text = arg.class_prob.toString();
      var sortedKeys = arg.word_probs.keys.toList();
      sortedKeys.sort((String a, String b) => compareWordProbs(arg.word_probs[a], arg.word_probs[b]));
      String out = "";
      for(var key in sortedKeys){
        out += "${key}: ${arg.word_probs[key]}\n";
      }
      row.addCell().text = out;
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

void loadingScreen(bool on){
  if(on){
    loading.text = "Loading...";
  }
  else{
    loading.text = "";
  }
}

//  Argument methods
void requestArguments() {
  // Requests arguments from a local server running the Python spectrum scripts.
  HttpRequest
      .getString("http://127.0.0.1:5000/spectrum/${topic}")
      .then((String jsonContents){
        createArgumentLists(jsonDecode(jsonContents));
        addArgumentRow();
  })
      .catchError((Error error){
    print(error.toString());
  });
  loadingScreen(true);
}

void createArgumentLists(var jsonArguments) {
  loadingScreen(false);
  // Decodes arguments from server response and places them in their lists.
  positiveArguments = new List<Argument>();
  negativeArguments = new List<Argument>();
  arguments = new Map();
  // First element in the list is the number of arguments each side has.
  for(var jsonArgument in jsonArguments){
    var argument = new Argument();
    argument.tweet = jsonArgument["tweet"];
    var support = jsonArgument["support"];
    List<String> supportArgs = new List<String>();
    for(var s in support){
      supportArgs.add(s);
    }
    argument.support = supportArgs;
    argument.class_prob = jsonArgument["class_prob"];
    var word_probs_dict = jsonArgument["word_probs"];
    var keys = word_probs_dict.keys.toList();
    Map<String, double> word_probs = new Map();
    for(var key in keys){
      word_probs.putIfAbsent(key, () => word_probs_dict[key]);
    }
    argument.word_probs = word_probs;

    arguments.putIfAbsent(argument.tweet, () => argument);
    if(jsonArgument["negative"]){
      argument.isNeg = true;
      negativeArguments.add(argument);
    }else{
      argument.isNeg = false;
      positiveArguments.add(argument);
    }
  }
}
