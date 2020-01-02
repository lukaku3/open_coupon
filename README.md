## setup python on windows
  download python 3.7.x  
  https://www.python.org/downloads/

## install virtualenv
    pip install --upgrade pip  
    pip install virtualenv  
## move in your working space.
   (meaning Documents or something Directory)
   
    cd your_working_space  
## create your virtual enviroment directory
    virtualenv open_coupon  
    cd open_coupon  
 
## activate virtual enviroment
    source Scripts/activate
    pip install --upgrade pip  
    pip install -r freeze.txt  
    git clone https://github.com/lukaku3/open_coupon.git  get_coupon  
    cd get_coupon  
  
## download chromedriver for Windows
- check your google chrome version.
- https://chromedriver.chromium.org/downloads
- move chromedriver to current directory  

└ open_coupon  
>├ Include  
├ Lib  
├ Scripts  
└ get_coupon  
>>├  chromedriver.exe  
├ freeze.txt    
├ MyCase.py    
  
## Update MyCase.py (Write your Account and you Password)

OK Pattern

    login_account = 'yourLoginId'  
    login_password = 'yourLoginPassword'
    
NG Pattern

    login_account = yourLoginId  
    login_password = yourLoginPassword
    
## execute python

    python MyCase.py MyTestCase.test_something

