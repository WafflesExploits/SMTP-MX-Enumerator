# SMTP-MX-Enumerator
 ### -> Enumerates SMTP (mail) servers from domains using MX/A records.
## Table of Contents
* [Installation](#installation)
* [Example Usage](#Example-Usage)
* [Usage](#Usage)
* [Contact](#contact)

## Installation
 ```
 $ git clone https://github.com/WafflesExploit/SMTP-MX-Enumerator
 ```

## Example Usage
```
$ ./smtp-records-enum.py -d naturitas.pt
* Starting SMTP Records Enum at 2023-03-15 13:46:14.
| 
| Settings:
| Number of Scans: 10 | Delay time between scans: 0
|
| Credits:
| By (https://github.com/WafflesExploits)
| 
| Results:
| Domain: naturitas.pt 
| Finished scan in 1.398s.
| [1] MX Record - aspmx.l.google.com
| A Records: 108.177.15.27, 66.102.1.26, 108.177.15.26
| [2] MX Record - aspmx2.googlemail.com
| A Records: 142.250.153.27
| [3] MX Record - aspmx3.googlemail.com
| A Records: 142.251.9.26
| [4] MX Record - alt1.aspmx.l.google.com
| A Records: 142.250.153.27, 142.250.153.26
| [5] MX Record - alt2.aspmx.l.google.com
| A Records: 142.251.9.26, 142.251.9.27
*
```

## Usage
```
./smtp-records-enum.py -h                    
usage: smtp-records-enum.py [-h] [-d DOMAIN] [-sn [SCANNUM]] [-st [SLEEPTIME]] [-dm] [-v]

-> Enumerates mail servers from domains using MX/A records.

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domains to enumerate.
  -sn [SCANNUM], --scannum [SCANNUM]
                        Number of times to search for multiple A records from found mail servers.
  -st [SLEEPTIME], --sleeptime [SLEEPTIME]
                        Time before each search of A records. Useful to prevent timeout and avoid being detected.
  -dm, --debugmode      Shows Errors
  -v, --verbose         VerboseMode
```

## Contact
Created by [@WafflesExploit](https://github.com/WafflesExploit) - feel free to contact me!
