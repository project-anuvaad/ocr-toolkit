# Error Profiling

Error profililing is done using the csv generated by the ocr_benchmark flow.
```
https://github.com/project-anuvaad/ocr-toolkit/tree/ocr_toolkit/ocr_benchmark
```
```

path = input csv  (path+csv)
crops_path = line image crops path
report_file = curated csv file
```
csv contains :-
```
gt_text: Google-vision text
tess_text: Tesseract Text
crop_name : line crop name (line image crop stored in the error crops path)
exp : Experiment name
Score : score is given based on the quality of gt_text and tess_text
missmatch_count : difference of text from gt_text and tess_text
coords : Bounding boc coordinates of the crop image
image_name : name of image where the crop image belongs to
ocr_conf : OCR confidence text
```

Output csv contains :- 
```
key : crop image name
error_type : error types are classified into classes of error :
              '''
              Class -2 : Manual intervention required 
              class -1 : tesseract correct
              class 0 : charater mismatch ಕೆ as ಕ
              Class 1 : ೧೧ . as NAN, ೧೧ . as 1, 2 as 2.0, 1.40 as 1.0, 14 as 1, etc.  ( digit error)
              Class 2 : ಚಿಹ್ನೆಗಳು as ಚಿಹೆಗಳು,  ಬಾಗಲಕೋಟ as ಬದಾಗಲಕೋಟ, ಎಲ್ಎಕೂ as ಎಲ್‌ಎಕ್ಯೂ etc.  (Auxiliaries)
              Class 3 : / as |, " as ' ', etc        (Special characters)
              Class 4 : கிடங்கு as யபI, கடனாக as -IபI, etc. (contradiction)
              Class 5 : ಅರ್ಜೆಂಟಿನಾ as             (Missing text and crop issue)
              Class 6 : Text repeatation
              '''
              

Ground_truth : Corrected text from either tesseract or googlevision or manual intervention
```

### Each text has to evaluated manually by running the jupyter notebook

```
'''
Line data curation:

1. Hit enter when google vision is true.

2. Type -1 when tesseract is correct.

3. Hit enter when both tesseract and google vision is true.

4. Type “w” to correct text manually give the one of the class where which error_type does the text belong and correct the ground truth using tesseract and google vision text.

5. Type -2 when we can’t correct the ground truth.

6. TYpe “s” when the image is not properly cropped(check matras,first word,last word),empty , too noisy,more than 2 lines and contain any diagram.
'''
```
