# 🔍 LogHunter

> Advanced Log Analysis Tool for Cybersecurity (SOC-focused)

LogHunter is a modular Python-based CLI tool designed to parse, search,
and analyze system and application logs.\
It helps detect suspicious activity and identify Indicators of
Compromise (IOCs) such as malicious IPs, hashes, and attack patterns.

------------------------------------------------------------------------

## 🚀 Features

-   🔎 **Multi-format Log Parsing**
    -   Syslog
    -   Apache / Nginx
    -   JSON logs
    -   Raw text
-   🧠 **Search Engine**
    -   Keyword search
    -   Regex-based detection
    -   Severity classification (info, warning, error, critical)
-   🚨 **IOC Detection**
    -   Malicious IP detection
    -   SHA256 hash matching
    -   Suspicious User-Agent detection
-   📊 **Reporting**
    -   Terminal output (colorized with rich)
    -   Export to JSON, CSV, HTML
-   🧩 **Modular Architecture**
    -   Plugin-based parsers
    -   Easily extensible

------------------------------------------------------------------------

## 🧪 Example Usage

``` bash
py -3.13 main.py test.log -k "Failed password"
py -3.13 main.py test.log -s error
py -3.13 main.py test.log --ioc
py -3.13 main.py test.log --export html --output report
```

------------------------------------------------------------------------

## ⚙️ Installation

``` bash
git clone https://github.com/Trollerixo/loghunter.git
cd loghunter
py -3.13 -m pip install -r requirements.txt
```

### 🔧 Development dependencies

``` bash
py -3.13 -m pip install -r requirements-dev.txt
```

------------------------------------------------------------------------

## 🧠 IOC Configuration

Edit:

    data/ip_blacklist.txt
    data/hashes.txt
    data/bad_useragents.txt

------------------------------------------------------------------------

## 🎯 Skills Demonstrated

-   Log analysis & event correlation\
-   Threat detection using IOC matching\
-   Python scripting & modular design\
-   Regex and pattern recognition\
-   SOC fundamentals

------------------------------------------------------------------------

## 👨‍💻 Author

Fabricio Daniel Pacheco Calderón
