The objective of this software is to classify each word as a theme. The classes / themes are learned from input texts.
By classifying each word in a text as belonging to a theme, an author can develop an intuition about the thematic dynamic range of their text. For example, if an author has a tendency to use too many depressing, gloomy words, it will come across as boring. This tool allows an author to identify when they get stuck in a thematic rut.

Running train.py will create a class for each folder in /data
Each folder in /data should be filled with .pdf files, which will automatically be converted to .txt, or .txt files. The intersection of the words in each .txt are the initial class words
Since classes cannot contain the same words, a word with multiple classes goes to the class in which it occurs the most times
Training produces a word list in the format of .txt for every class. These go in /result

Running label.py will produce a highlighted markdown file from the .txt file passed in the arg. Each class is highlighted with a different color, and a legend is built at the top of the result .md file.

The sample classes are included in /result
