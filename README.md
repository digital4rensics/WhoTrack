WhoTrack
========

Tracking Daily Registrant Changes

## 1.0 Introduction

The script will track basic domain WhoIs information based upon domains entered in the database.
This is an ongoing work and is likely not suitable for production use at the moment.
Planned improvements for: 1.) Proxy support 2.) Reporting 3.) History Tracking

The structure of the project requires a parser for each potential registrar. A few parsers are included
already, and more will be added as testing continues. Community work in this area would be greatly
appreciated. Otherwise, please be patient as it will likely take a while to get good coverage.

## 2.0 Installation & Use

As long as you maintain the structure of the repository, there should be any issues with just calling
the python script directly.

Suggested use is through a daily scheduled job to run the script. Until reporting and history are
fully developed, it's recommended that the script be run with the -v option and save the output to
a local file.

### 2.2 - Requirements
The only extra requirement at this time is SocksiPy, which is included in the repo for use.

## 3.0 Known Bugs

At this point, I have not tested the proxy support on a server stable enough to determine
full functionality. Therefore, the proxy support is not considered fully implemented and
there are likely problems with this at present.

# Contact

[@digital4rensics](https://twitter.com/Digital4rensics) - www.digital4rensics.com - Keith@digital4rensics.com