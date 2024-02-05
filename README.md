PRE SCREENING CHATBOT
====================

This is a chatbot that performs a screening interview to a candidate. 

Installation
------------------------

To use this project you need to have python installed. It has been tested to work 
with version [3.10](https://www.python.org/downloads/release/python-31011/), 
you can follow the installation procedure at the link, or you can try any other 
python version. We do not guarantee for it to work though.

It is deeply suggested to set up a virtual environment to use this project. 
Have a look at [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

The package dependencies can be solved by installing the following packages with pip:
 - rasa

All the other dependencies should be installed as dependencies of these packages. 
To do it, execute the following instructions in a command prompt inside your virtual env:
```
pip install -r requirements.txt
```

Create a folder at the same level of app.py named 'models' and place the downloaded model in there.

Download the italian language model from the 
[spacy repository](https://github.com/explosion/spacy-models/releases/tag/it_core_news_lg-3.7.0).
Install it by executing the following instruction inside your virtual environment:

```
pip install [path\to\it_core_news_lg-3.*.tar.gz]
```

or you could download it by using spacy itself with:

```
python -m spacy download it_core_news_lg
```

Once you have installed these packages, we suggest you to train your model since there might have been
modifications to rules and stories. To train your model execute the command below:

```
rasa train
```

Custom Action Server
--------------------

All the functions needed to enable the integration with the database are implemented through 
Custom Actions. To enable these operations it is necessary to launch a separate Custom Action Server.
Execute the following instructions to enable Custom Actions in your localhost:

1. Check that the file ```endpoints.yml``` has the following lines uncommented.
    ```
    action_endpoint: 
        url: "http://localhost:5055/webhook"
    ```

2. Check that you project has the folder actions containing the files ```__init__.py``` and ```actions.py```. 
The file __init__.py can be empty, it is needed to identify the folder as a python module containing your custom actions.

3. Open a new prompt/terminal window and activate the virtual environment if you have one.
    ```
    C:\path\to\your\project\folder>your_virtual_env\Scripts\activate.bat  
    ```

4. Launch the Custom Action Server:
    ```
    (your_virtual_env) C:\path\to\your\project\folder>rasa run actions
    ```

The server will be responding to REST APIs at the default url: 0.0.0.0:5055.

Now you can launch your chatbot with the ```rasa shell``` command.