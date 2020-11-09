# Job Collector
Job Collector is a project I made, to help me while I hunt for a job.
Built using the scrapy framework, Job Collector scrapes all the job postings it finds based on the config file that's inclued with the code.
Right now it is specific for Indeed, but the ground work is laid so we can collect jobs from a whole bunch of diffrent job sites.

\*\*Posibillity of IP being blocked, exspecially if used not as it was intended. I accept no responsibility if that were to happen.\*\*

## Usage
1. Clone the repository onto your local machine.
2. Run throught the config.yaml file and make any necessary changes to the settings.
3. Run the main.py file and wait for the program to finish running.
4. You should now see a folder labeled "output". You will find the completed files in that folder.

## Configureing Job Collector
### Search Parameters
#### Log Level
Used to change the output when the job collector is running.  
ACCEPTED VALUES: CRITICAL, ERROR, WARNING, INFO, DEBUG
#### Search Keywords
A list of main keywords that the job collector uses to search by.  
If null, the job collector will grab all jobs it can find in the specified location.   
ACCEPTED VALUES: LIST OF KEYWORDS, NULL
#### Locations
A list of locations that the job collector uses to search by.  
ACCEPTED VALUES: LIST OF LOCATIONS
#### Sub Keywords
A list of sub keywords that the job collector uses to help determine whether the job is a good match or not.  
ACCEPTED VALUES: LIST OF SUB KEYWORDS, NULL
#### Radius
A positive integer that determines the radius which the job collector will match jobs with.  
ACCEPTED VALUES: POSITIVE INTEGER
### File Configuration
#### File Name
Name for the output file.  
ACCEPTED VALUES: STRING
#### File Type
Desired file type for your output file.  
ACCEPTED VALUES: JSON, CSV
#### Item Limit
Used to limit the amount of items collected with the job collector.  
If item limit is set to 0, the job collector will collect as many jobs as it can.  
ACCEPTED VALUES: POSITIVE INTEGER
#### Compact
The compact flag allows you to decide whether you would like a compact version of locations, salary, ect. or if you would like all the data separated for easier data analysis.  
It will also hide columns such as match and keywords.  
ACCEPTED VALUES: BOOL

## Notes
Speed can be ajusted inside of the main.py file. By lowering the delay rate you will have faster speeds, but you also risk getting your IP adress blocked as well.
