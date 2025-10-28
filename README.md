# easy-ics

输入：文字/图片/csv文件

图片->ocr->文字pipeline

文字->1. dateparser re parse 2. crf fasttest jieba+规则 3. spaCy+transformer bert-bsae-chinese roberta-base 