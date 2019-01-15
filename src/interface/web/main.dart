import 'dart:html';
import 'dart:io' as io;
import 'dart:convert';
import 'package:path/path.dart' as path;

InputElement topicInput;
Element output;
List<Argument> positiveArguments;
List<Argument> negativeArguments;

TableElement argumentTable;

int rowCount = 0;
int posScore = 0;

String topic;

void main() {
  // Display 3 screens, each with 3 arguments on each side and each with 3
  // supporting tweets. That makes for at least 72 arguments.
  topicInput = querySelector('#topic');
  topicInput.onChange.listen(changeTopic);
  argumentTable = querySelector("#argTable");
  getArgumentLists();
}

void changeTopic(Event e){
  topic = topicInput.value;
  // TODO: Get a new set of arguments.
  restartTable();
  addArgumentRow();
}

void addArgumentRow(){
  if(negativeArguments.isNotEmpty && positiveArguments.isNotEmpty) {
    TableRowElement opinionRow = argumentTable.insertRow(-1);
    var negArg = negativeArguments.removeLast();
    var posArg = positiveArguments.removeLast();
    opinionRow.insertCell(0)
      ..colSpan = 3
      ..children.add(new ButtonElement()
        ..text = negArg.tweet
        ..onClick.listen(makeSelection));
    opinionRow.insertCell(1)
      ..colSpan = 3
      ..children.add(new ButtonElement()
        ..text = negArg.tweet
        ..onClick.listen(makeSelection));

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
  restartTable();
  TableRowElement resultRow = argumentTable.insertRow(-1);
  resultRow.insertCell(0)
    ..children.add(new ParagraphElement()
      ..text = "According to this quiz you are ${posScore / rowCount * 100} % positive about ${topic}");
}

void makeSelection(Event e){
  rowCount++;
  ButtonElement selectedArgument = e.target;
  print(selectedArgument.parent.className);
  // TODO: Find out which sentiment was clicked and increment score.
  if(rowCount % 3 == 0) {
    restartTable();
  }
  addArgumentRow();
}

void restartTable(){
  argumentTable.children.clear();
}

void getArgumentLists(){
  List<String> spec = getStaticSpectrum(); //TODO: Get real spectrum.
  positiveArguments = new List<Argument>();
  negativeArguments = new List<Argument>();
  int startingLength = spec.length;
  while(spec.length > 3) {
    var arg = new Argument();

    arg.tweet = spec.removeLast();
    List<String> support = new List<String>();
    for (int i = 0; i < 3; i++) {
      support.add(spec.removeLast());
    }
    arg.support = support;
    // Take tweets from the end -> remove positives.
    // When less than half are left they should all be negative.
    if (spec.length > startingLength / 2) {
      positiveArguments.add(arg);
    }
    else {
      negativeArguments.add(arg);
    }
  }
}

class Argument{
  String tweet;
  List<String> support;
}

LIElement newLI(String itemText) => LIElement()..text = itemText;

List<String> getSpectrum() {
  // Platform in web is urls, how to access local file in web context?
  io.Process.run('python3', ['/home/aga/work/ii/dissertation/code/src/data_pass.py']).then((io.ProcessResult results) {
    print(results.stdout);
  });
  print("Start spectrum");
  var pathToFile = path.join('/home/aga/work/ii/dissertation/code/data/spectrum.json');
  var myFile = new io.File(pathToFile);
  print("Created file ${myFile.path}");
  String jsonString = myFile.readAsStringSync();
  print("Got the json ${jsonString.substring(0, 100)}");
  List<String> spectrum = jsonDecode(jsonString);
  print("Decoded the spectrum");
  int i = 0;
  for (var s in spectrum.getRange(0, 10)) {
    print("${i}: ${s}");
    i++;
  }
  print("Finished the spectrum");
  return spectrum;
}

List<String> getStaticSpectrum(){
  List<String> spectrum = new List.from(["A", "B", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "w", "x", "y", "z"]);
  return spectrum;
}