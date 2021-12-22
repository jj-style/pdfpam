# pdfpam
CLI utility for picking and choosing pages from certain PDF files and combining them together.

## Requirements
- `pdftk`
- [click](https://github.com/pallets/click/)

## Installation
You can install from source like so:
```
git clone github.com/jj-style/pdfpam
cd pdfpam
pip install -e .
```

## Usage
`pdfpam config.txt /path/to/dir/of/pdfs output.pdf`

## Configuration
The input file must have the following format:  
```
1:1 3 5
2:10 20
3:5-7 10
```  
This would extract pages:
- 1, 3, 5 from the file starting `1-*` in the directory given
- 10 and 20 from the file starting `2-*` in the directory given
- 5,6,7 and 10 from the file starting `3-*` in the directory given
and combine them all into one file.

**Note the files must all be in the same directory and be identifiable by something followed by a hyphen, e.g. `[1,2,3]-file.pdf`, `[a,b,c]-file.pdf`.**
