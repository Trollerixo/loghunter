LogHunter — Advanced Log Analysis Tool for Cybersecurity

LogHunter is a modular Python-based CLI tool designed to parse, search,
and analyze system and application logs. Built with cybersecurity in
mind, it helps detect suspicious activity, identify Indicators of
Compromise (IOCs), and generate structured reports.

------------------------------------------------------------------------

FEATURES

-   Log Parsing: Supports syslog, Apache/Nginx, JSON logs, and raw text

-   Search Engine: Keyword search, regex matching, severity filtering

-   IOC Detection: Malicious IPs, hashes (SHA256), suspicious
    user-agents

-   Output & Reporting: Terminal output and export to JSON, CSV, HTML

-   Modular Architecture: Plugin-based and extensible design

------------------------------------------------------------------------

EXAMPLE USAGE

Detect failed logins: py -3.13 main.py test.log -k “Failed password”

Filter errors: py -3.13 main.py test.log -s error

Detect IOCs: py -3.13 main.py test.log –ioc

Export report: py -3.13 main.py test.log –export html –output report

------------------------------------------------------------------------

INSTALLATION

git clone https://github.com/Trollerixo/loghunter.git cd loghunter py
-3.13 -m pip install -r requirements.txt

------------------------------------------------------------------------

IOC CONFIGURATION

Edit: data/ip_blacklist.txt data/hashes.txt data/bad_useragents.txt

One entry per line.

------------------------------------------------------------------------

SKILLS DEMONSTRATED

-   Log analysis
-   Threat detection
-   Python scripting
-   Regex and pattern matching
-   SOC fundamentals

------------------------------------------------------------------------

AUTHOR

Fabricio Daniel Pacheco Calderón
