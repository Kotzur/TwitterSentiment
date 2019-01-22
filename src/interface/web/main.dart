import 'dart:html';
import 'dart:convert';

InputElement topicInput;
Element output;
List<Argument> positiveArguments;
List<Argument> negativeArguments;

var arguments;

TableElement argumentTable;

int rowCount = 0;
int posScore = 0;

String topic;

void main() {
  // Run an interactive debate on a topic based on tweets.
  topicInput = querySelector('#topic');
  topicInput.onChange.listen(changeTopic);
  argumentTable = querySelector("#argTable");
}

// Interface methods

void changeTopic(Event e){
  // Responds to new topic choice.
  topic = topicInput.value;
  print("New topic: ${topic}");
  restartTable();
  requestArguments();
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
        ..id = "neg");
    opinionRow.insertCell(1)
      ..colSpan = 3
      ..children.add(new ButtonElement()
        ..text = posArg.tweet
        ..onClick.listen(makeSelection)
        ..id = "pos");

    TableRowElement supportRow = argumentTable.insertRow(-1);
    int i = 0;
    for (var arg in [negArg, posArg]) {
      for (var sup in arg.support) {
        supportRow.insertCell(i)
          ..text = sup;
        i++;
      }
    }
  }
  else{
    displayResultScreen();
  }
}

void displayResultScreen(){
  // Presents final interface with debate results.
  restartTable();
  TableRowElement resultRow = argumentTable.insertRow(-1);
  resultRow.insertCell(0)
    ..children.add(new ParagraphElement()
      ..text = "You find arguments pro ${topic} ${posScore / rowCount * 100}% convincing");
}

void makeSelection(Event e){
  // Responds to user's debate choice.
  rowCount++;
  ButtonElement selectedArgument = e.target;
  print(selectedArgument.parent.className);
  if(selectedArgument.id == "pos"){
    posScore++;
  }
  if(rowCount % 3 == 0) {
    restartTable();
  }
  addArgumentRow();
}

void restartTable(){
  // Clears the interface from previous arguments.
  argumentTable.children.clear();
}

//  Argument methods

class Argument{
  String tweet;
  List<String> support;
}

void requestArguments() {
  // Requests arguments from a local server running the Python spectrum scripts.
  HttpRequest.getString("http://127.0.0.1:5000/spectrum/${topic}").then((String jsonContents){
    print(jsonContents);
    arguments = jsonDecode(jsonContents);
    createArgumentLists();
    addArgumentRow();
  })
      .catchError((Error error){
    print(error.toString());
  });
}

void createArgumentLists() {
  // Decodes arguments from server response and places them in their lists.
  positiveArguments = new List<Argument>();
  negativeArguments = new List<Argument>();
  // First element in the list is the number of arguments each side has.
  for(int i = 0; i < arguments.length; i++){
    var jsonArgument = arguments[i];
    var argument = new Argument();
    argument.tweet = jsonArgument["tweet"];
    var support = jsonArgument["support"];
    List<String> supportArgs = new List<String>();
    for(var s in support){
      print(s);
      supportArgs.add(s);
    }
    argument.support = supportArgs;
    if(jsonArgument["negative"]){
      negativeArguments.add(argument);
    }else{
      positiveArguments.add(argument);
    }
  }
}