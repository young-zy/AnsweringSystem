# AnsweringSystem

A simple online answering system using flask and Mdui

Feel free to tell me your suggestions or your questions in the issues section 



# How to use
## First 
    Change the app.secretkey in app.py, make sure that only you know it, 
    since it's used for encryption
## Then
     Change the data.json @ %project_root% 
     Keys:
        "title" for question        #Could be empty
        "imgpath" for img quesiton  #could be empty
        "items" for options         #For now you can only put exactly 4 optioons
        "type" for the answertype   #"multiple" for multiple answers "textfield" for textanswers
                                    #"" or other strings will be judged as single choice question
## Don't forget
    Create a Folder name "answers" to let the program store final results 



## Enjoy :-)       
        
# If you encounter any problem
    try cleaning your cookies(or just clear session in your cookie)
        You may lost all your selection
    and then force refresh your page(ctrl+F5)
