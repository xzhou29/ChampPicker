# ChampPicker


### BACKEND - instructions
- Pull raw data from Riot API: ```python backend/riot/pull_raw_data.py```
- Create new tables for web APP ```python backend/riot/create_tables.py```
- ```champ_picker.py``` is used with Flask API for generating data entries for web APP

### FRONT-END - instructions
- Development mode for testing: ```npm start``` under directory ```./client```
- Deploy web application into flask: run ```npm run build``` to create ```bundle.js```
- Copy or move ```bundle.js``` to ```./backend/public/js/bundle.js```
- Run flask under main directory: ```./run_flask```

### TODO list
- Download all champ icons and images instead of fetching through external links
- Disable real-time analysis when user change champs: this will need much more computing resources, but we will keep this functionality for future development if we find better way to do this.
- Add animation effect for prediction and audio?
- This web APP can be easily extended with more functionalities.