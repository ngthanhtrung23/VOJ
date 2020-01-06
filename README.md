# VOJ

- Directory statement/ contains generated latex for problems in [VOJ](https://vn.spoj.com/)

# TODO

- Can we parse tex files into legend, input, output and sample test data? (Done)
- I (t-rekttt) decided to run an analyze on the statements's subsections (by counting how much of `subsubsection` inside each statement) and saw that they have this kind of distribution (in the format of `[count, frequency]`). 
![](https://cdn.discordapp.com/attachments/663039190560145409/663331329915748385/unknown.png)

By examination (`subsectionsExtractor.py`) I saw that most of the statement have a typical format of `3 subsections`, beautifully ordered by the format: statement, input, output, notes. So I wrote an extractor for that specific case (inside `statementExtractor.py`).
- Done extractor for 3+ subsections. Now we need to write the extractor for the others as well.

# EXTRACTOR INSTRUCTION
1. Place your statements into `statement` folder
2. Run `pip3 install unidecode`
3. Run `python3 subsectionsExtractor.py` to extract information about statements based on subsections
4. Run `python3 statementExtractor.py` to extract statements into parts
Extracted statements are saved in `extracted` folder. Each statement would be broken into 4 parts: `statement.tex`, `input.tex`, `output.tex`, `notes.tex`, the same format as Codeforces Polygon
