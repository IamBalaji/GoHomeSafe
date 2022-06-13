# GoHomeSafe
Django based webapp for Fatigue Detection: For Driver Safety


# Intructions to run the web application
1. `clone` the repository
   ```shell 
   git clone https://github.com/IamBalaji/GoHomeSafe.git
   ```
2. `cd` to repositories to root path
3. create `conda` environment
   ``` shell 
   conda env create -f=environment.yml
   ```
4. activate the virtual/conda environment
   ``` shell
   source activate GoHomeSafe
   ```
   OR 
   ```shell
   conda activate GoHomeSafe
   ````
5. run the django server
    ```shell
    python manage.py runserver 
    ```
6. open the url `http://127.0.0.1:8000/`

7. web optons:
   a. `Start`: to start the capturing the video
   b. `GoHomeSafe`: to start sending the data to backed and getting the predictions
   c. `Stop`: to stop the video capture
