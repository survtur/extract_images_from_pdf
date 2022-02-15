Scans PDF document, looks for image xObjects and saves them all.

# Requirements #
  - Python3.6+
  - PyPDF
  - PIL

# Example #

    DIR_WITH_PDFS = "/home/user/Downloads/Untitled Folder"
    SAVE_IMAGES_HERE =  "/home/user/Downloads/Untitled Folder/test"
    ie = ImagesExtractor()
    ie.extract_dir(DIR_WITH_PDFS, SAVE_IMAGES_HERE)

# Credit #
Based on [this answer](https://stackoverflow.com/a/34116472/2039471) found at stackoverflow 
