# VOJ

- Directory statement/ contains generated latex for problems in [VOJ](https://vn.spoj.com/)

# TODO

- Can we parse tex files into legend, input, output and sample test data?

# EXTRACTOR INSTRUCTION
1. Place your statements into `statement` folder
2. Run `python subsectionsExtractor.py` to extract information about statements based on subsections
3. Run `python statementExtractor.py` to extract statements into parts
Extracted statements are saved in `extracted` folder. Each statement would be broken into 4 parts: `statement.tex`, `input.tex`, `output.tex`, `notes.tex`, the same format as Codeforces Polygon
