# Synopsys Detect Wizard (detect-wizard)

Black Duck scanning wizard to pre-scan folders, determine and output optimal scan configuration in YML files and optionally call Synopsys Detect to perform scan

# INTRODUCTION

This script is provided under an OSS license (specified in the LICENSE file) to assist users when scanning projects in Black Duck for OSS analysis.

It does not represent any extension of licensed functionality of Synopsys software itself and is provided as-is, without warranty or liability.

# OVERVIEW

The Detect Wizard is intended to provide a simple, comprehensive method for scanning new projects with Black Duck, checking prerequisites,
pre-scanning the specified folder to identify the contents and using supplied preferences (license, security analysis or both) and a 
sensitivity value to determine the optimal Synopsys Detect options to use, to create a yml project file (for running Synopsys Detect later) 
and optionally invoking Synopsys Detect to perform the scan.

# DETAILED DESCRIPTION

The Detect Wizard uses several inputs by default including:
- Folder to scan (REQUIRED)
- Black Duck server URL (REQUIRED)
- Black Duck API token (REQUIRED)
- Scan sensitivity value (determines how detailed the scan will be - default 3)
- Scan focus (license, security or both - default both)
- Black Duck Project name (default none)
- Black Duck Project version (default none)

These values can be specified as arguments, or will be requested in an interactive mode if not supplied. Server URL and API key will also be picked up 
from standard Detect environment variables (BLACKDUCK_URL and BLACKDUCK_API_TOKEN) if set in the environment.

The scan sensitivity value specifies the analysis scope ranging from 1 (most accurate Bill of Materials with minimal false positives – but with the potential 
to miss some OSS components) to 5 (most comprehensive analysis to identify as many OSS components as possible but with the potential for many false positives). See the section `Scan Sensitivity` below.

Detect Wizard allows predefined Detect scan parameters to be defined as environment variables which will be passed straight to Synopsys Detect. An existing .yml project configuration file will be backed up and will not be used by Detect Wizard or in creating the new .yml file. Detect Wizard will check the prerequisites to run Synopsys Detect (including the correct version of Java) and then scan the project location for files and archives, calculate the total scan size, check for project (package manager) files and package managers themselves and will also detect large duplicate files and folders.

It will expand .zip, .jar and .tar files automatically, processing recursive files (zips within zips etc.). Other archive types (.gz, .Z etc.) are not 
currently expanded by Detect Wizard (although they will be expanded by Synopsys Detect).

Based on the specified sensitivity and scan type, it will identify Detect options which are relevant to the scanned project and determine suitable settings 
to support the level of scan required.

It will export a .yml file for use in Detect scans, and will optionally call Detect directly to run the scan.

# CONTROLLING THE LEVEL OF SCAN USING THE WIZARD

Detect Wizard uses 2 input factors to control the types of scan and the scan features used:

1. Scan sensitivity value (1-5)
1. Scan focus (l, s or b for License, Security or Both)

## Scan Sensitivity

Scan sensitivity can be specified as a command line argument (-s or --sensitivity) or in interactive mode, and accepts a value between 1 and 5.

Sensitivity of 1 will configure/run a minimal scope scan focussed on package manager direct dependencies only and without a Signature (folder) scan; this is intended to ensure that identified OSS components are highly likely to be included and used in the running application with the minimal number of OSS components which may be in the project but not used in the project.

Sensitivity of 3 (the default) is intended to be a general purpose scan which will try to perform a comprehensive analysis including OSS components most likely to be used the application, but could potentially include some which are in the project but not used by the application.

Sensitivity of 5 will configure/run a maximal scope scan using all relevant scanning types including package manager dependency analysis (including dev and test dependencies), signature scan (incuding individual file matching where appropriate to include singleton JS files, and not trying to include ), and optionally snippet scanning etc. intended to identify all possible OSS components whether they are used in the application or not.

The full list of scan types/options by sensivity is shown below:

| Sensitivity   | Dependency Scan | Dev/Test Deps | Signature Scan | Dep Search | Duplicates | Snippets | Split >4.5G |
| :------------ | :-------------- | :------- | :------------- | :--------- | :--------- | :------- | :---------- |
| 1             | Buildless | Excluded | No | Min depth, Std exclusions | Ignored | No | Yes |
| 2             | Full | Excluded | Yes | Half max depth, Std exclusions | Ignored | No | Yes |
| 3             | Full | Included | Yes | Half max depth, Std exclusions | Not Ignored | No | Yes |
| 4             | Full | Included | Yes + Ind Files | Half max depth, No exclusions | Not Ignored | No | Yes |
| 5             | Full | Included | Yes + Ind Files | Max depth, No exclusions | Not Ignored | Yes if Scan Focus = l or b | Yes |

## Notes
1. 'Dev/Test Deps' is where dev dependencies in npm, packigist and ruby will be ignored or not, Test dependency exclusion is implemented for Gradle. 
1. Dep Search 'depth' refers to the range of depths where package manager files were found in the prescan.
1. Dep search 'exclusions' refers to whether the default folder exclusions will be applied or not (build, node_modules etc.)
1. Duplicates 'ignored/not ignored' refers to whether large duplicate folders will be excluded from the signature scan or not.
1. Split >4.5G will cause a large signature scan greater than 4.5G to be scanned offline, the json files split and then uploaded (only works when scan is performed online).

## Scan Focus
Scan focus can be selected between `s` (for security only), `l` (for license compiance only) or `b` (for both).

Selecting 'l' or 'b' will add the local copyright and license search options (`detect.blackduck.signature.scanner.copyright.search` and `detect.blackduck.signature.scanner.license.search`) to scans, in addition to using snippet scanning if the sensitivity level is set to 5.

# PREREQUISITES
Detect Wizard requires Python 3 to be installed.

# INSTALLATION
    pip3 install libmagic
    pip3 install python-magic==0.4.15
    (Windows only: pip install python-magic-bin==0.4.14)
    pip3 install -i https://test.pypi.org/simple/ detect-wizard

# DETECT WIZARD USAGE
The Detect Wizard can be invoked with or without parameters.

If the scan folder or other required options are not specified, or `-i`/`--interactive` is used, then required options will be requested in interactive mode.

The detect_wizard script arguments are shown below:

    usage: detect_wizard [-h] [-b] [-i] [-s SENSITIVITY] [-f FOCUS] [-u URL]
                          [-a API_TOKEN] [-n] [—no_write]
                          [--aux_write_dir AUX_WRITE_DIR] [-hp HUB_PROJECT]
                          [-hv HUB_VERSION] [-t TRUST_CERT] [-bdba] [scanfolder]

    Check prerequisites for Detect, scan folders, configure and run Synopsys Detect

    positional arguments:
      scanfolder            Project folder to analyse

    optional arguments:
      -h, --help            show this help message and exit
      -b, --bdignore        Create .bdignore files in sub-folders to exclude folders from scan
      -i, --interactive     Use interactive mode to review/set options
      -s SENSITIVITY, --sensitivity SENSITIVITY
                            Coverage/sensitivity - 1 = dependency scan only & limited FPs, 5 = all
                            scan types including all potential matches
      -f FOCUS, --focus FOCUS
                            Scan focus of License Compliance (l) / Security (s) / Both (b)
      -u URL, --url URL     Black Duck Server URL
      -a API_TOKEN, --api_token API_TOKEN
                            Black Duck Server API Token
      -n, --no_scan         Do not run Detect scan - only create .yml project config file
      --no_write            Do not write to scan directory (log files and binary zip archive for example).
      --aux_write_dir AUX_WRITE_DIR
                            Directory to write intermediate files (default is the project top-level folder)
      -hp HUB_PROJECT, --hub_project HUB_PROJECT
                            Hub Project Name
      -hv HUB_VERSION, --hub_version HUB_VERSION
                            Hub Project Version
      -t TRUST_CERT, --trust_cert TRUST_CERT
                            Automatically trust Black Duck cert
      -bdba, --binary       Upload binary files for binary scan is sensitivity>=4

If scanfolder is not specified then all required options will be requested interactively (alternatively use -i or --interactive option to run interactive 
mode). Enter q or use CTRL-C to terminate interactive entry and the program. Special characters such as ~ or environment variables such as $HOME are not 
supported in interactive mode. Default values will be identified from the environment variables BLACKDUCK_URL or BLACKDUCK_API_TOKEN if set in the environment.

The scanfolder can be a relative or absolute path.

The -bdba or --binary options with Sensitivity>=4 will cause Detect Wizard to zip binary files (.dll .obj .o .a .lib .iso .qcow2 .vmdk .vdi .ova .nbi .vib .exe .img .bin .apk .aac .ipa .msi) within the project hierarchy into a new archive and upload for binary scanning.

# EXAMPLE USAGE

The following command will request arguments interactively:

    detect-wizard

The interactive questions are shown below (set the environment variables BLACKDUCK_URL and BLACKDUCK_API_TOKEN to pre-populate these values):

    Enter project folder to scan (default current folder ‘/Users/myuser/Desktop'):
    Black Duck Server URL [None]: 
    Black Duck API Token [None]: 
    Scan sensitivity/coverage (1-5) where 1 = dependency scan only, 5 = all scan types including all potential matches [3]: 
    Scan Focus (License Compliance (l) / Security (s) / Both (b)) [b]: 
    Hub Project Name [None]:
    Hub Project Version [None]:
    Run Detect scan (y/n) [y]:
    Disable SSL verification and automatically trust the certificate (required for self-signed certs) (y/n) [n]:

The following example command specifies the folder to scan and uses default values for other arguments (sensitivity = 3, scan focus = both, run Detect scan = y).
If not specified, then the Black Duck project and version names will be determined by Synopsys Detect. For this command 

    detect-wizard /Users/myuser/myproject

# SUMMARY INFO OUTPUT
This section includes counts and size analysis for the files and folders beneath the project location.

The Size Outside Archives value in the ALL FILES (Scan Size) row represents the total scan size as calculated by Detect (used for capacity license).

Note that the Archives(exc. Jars) row covers all archive file types but that only .zip files are extracted by detect_advisor (whereas Synopsys Detect 
extracts other types of archives automatically). The final 3 Inside Archives columns indicate items found within .zip archives for the different types 
(except for the Jar row which references .jar/.ear/.war files). The Inside Archives columns for the Archives row itself reports archive files within .zips 
(or nested deeper - zips within zips within zips etc.).

    SUMMARY INFO:
    Total Scan Size = 5,856 MB

                             Num Outside     Size Outside      Num Inside     Size Inside     Size Inside
                                Archives         Archives        Archives        Archives        Archives
                                                            (UNcompressed)    (compressed)
    ====================  ==============   ==============   =============   =============   =============
    Files (exc. Archives)        297,415         4,905 MB         130,126          653 MB          160 MB
    Archives (exc. Jars)              39           951 MB               9            0 MB            0 MB
    ====================  ==============   ==============   =============   =============   =============
    ALL FILES (Scan size)        297,454         5,856 MB         130,135          654 MB          160 MB
    ====================  ==============   ==============   =============   =============   =============
    Folders                       30,435              N/A          10,309             N/A             N/A   
    Ignored Folders                4,169         2,319 MB               0            0 MB            0 MB
    Source Files                 164,240         1,024 MB          53,740          171 MB           34 MB
    JAR Archives                       6             6 MB               0            0 MB            0 MB
    Binary Files                      33            99 MB              10            0 MB            0 MB
    Other Files                  129,476         2,988 MB          75,282          478 MB          124 MB
    Package Mgr Files              3,633            25 MB           1,094            2 MB            0 MB
    OS Package Files                   0             0 MB               0            0 MB            0 MB
    --------------------  --------------   --------------   -------------   -------------   -------------
    Large Files (>5MB)                38           336 MB               1            9 MB            4 MB
    Huge Files (>20MB)                27         1,875 MB               1           35 MB            6 MB
    --------------------  --------------   --------------   -------------   -------------   -------------

    PACKAGE MANAGER CONFIG FILES:
    - In invocation folder:   0
    - In sub-folders:         3633
    - In archives:            0
    - Minimum folder depth:   2
    - Maximum folder depth:   14
    ---------------------------------
    - Total discovered:       3633

    Config files for the following Package Managers found: gradlew, gradle, clang, dotnet, npm, yarn, pod, python, python3, pip

# RECOMMENDATIONS
This section includes a list of critical findings which will cause Detect to fail.

    RECOMMENDATIONS:
    - CRITICAL: Overall scan size (6,520 MB) is too large
        Impact:  Scan will fail
        Action:  Ignore folders or remove large files

# OUTPUT OPERATIONAL TABLE

Detect Wizard will produce 2 output tables explaining which scan features and options have been applied and the reason for selection.

The first table shows the options which will be applied (or the default option overridden) and the cause of this selection, whereas the second table shows options which will not be applied (NO-OP).

    ----------------------------------------------- Sensitivity(5) Manifest -----------------------------------------------
    Scan options applied:
    +----------------------------+-----------------------------+-----------------------------+-----------------------------+
    |         Actionable         |       Cause/Condition       |           Outcome           |         Description         |
    +============================+=============================+=============================+=============================+
    |   Individual File Match    |      sensitivity >= 4       | detect.blackduck.signature. |  Individual File Matching   |
    |                            |                             | scanner.individual.file.mat |     (SOURCE) is ENABLED     |
    |                            |                             |        ching=SOURCE         |                             |
    +----------------------------+-----------------------------+-----------------------------+-----------------------------+
    |   File Snippet Matching    |      sensitivity == 5,      | detect.blackduck.signature. |  File Snippet Matching set  |
    |                            |      scan_focus != "s"      | scanner.snippet.matching=   |         to ENABLED          |
    |                            |                             |      SNIPPET_MATCHING       |                             |
    +----------------------------+-----------------------------+-----------------------------+-----------------------------+
    | Detector Search Exclusions |      sensitivity >= 4       | detect.detector.search.excl |  Search exclusion defaults  |
    |                            |                             |    usion.defaults=false    |        DEACTIVATED.         |
    +----------------------------+-----------------------------+-----------------------------+-----------------------------+
    |       License Search       |      scan_focus != "s"      | ('detect.blackduck.signatur |   License search WILL be    |
    |                            |                             |  e.scanner.license.search=  |            used.            |
    |                            |                             | true', 'detect.blackduck.si |                             |
    |                            |                             | gnature.scanner.copyright.s |                             |
    |                            |                             |        earch=true')         |                             |
    +----------------------------+-----------------------------+-----------------------------+-----------------------------+
    |   Detector Search Depth    |      sensitivity == 5       |              1              |  Detector search depth set  |
    |                            |                             |                             |            to 1             |
    +----------------------------+-----------------------------+-----------------------------+-----------------------------+
    -----------------------------------------------------------------------------------------------------------------------
    Scan options not applied:
    +----------------------------+--------------------------------------+---------+----------------------------------------+
    |         Actionable         |           Cause/Condition            | Outcome |              Description               |
    +============================+======================================+=========+========================================+
    |       Buildless Mode       |           sensitivity > 1            |  NO-OP  |    Buildless mode will NOT be used.    |
    +----------------------------+--------------------------------------+---------+----------------------------------------+
    |       Signature Scan       |           sensitivity != 1           |  NO-OP  |       Signature Scan is ENABLED        |
    +----------------------------+--------------------------------------+---------+----------------------------------------+
    |     Scanfile Splitter      |           scan_size < 4.5            |  NO-OP  |  Scan (0.0002GB) is within size limit  |
    |                            |                                      |         |      (5GB) and will NOT be split.      |
    +----------------------------+--------------------------------------+---------+----------------------------------------+
    |      BDBA Binary Scan      | num_binaries <= 1, num_binaries != 1 |  NO-OP  |       BDBA will NOT be invoked.        |
    +----------------------------+--------------------------------------+---------+----------------------------------------+
    | Directory Duplicate Ignore |           sensitivity > 2            |  NO-OP  |   Duplicated directories WILL NOT be   |
    |                            |                                      |         |                ignored.                |
    +----------------------------+--------------------------------------+---------+----------------------------------------+
    -----------------------------------------------------------------------------------------------------------------------

# DETECT SCAN PROCESS

If the `Run Detect Scan` option is specified (or the `-n` or `--no_scan` option is specified), then Detect Wizard will call the standard Synopsys Detect to run the scan using the options generated by the Wizard.

# OUTPUT FILES

The file `application-project.yml` will be created in the project folder if it does not already exist. If the file already exists it will be renamed first. 
The application-project.yml config file can be used to configure Synopsys Detect using the single `--spring.profiles.active=project` option.

The file `detect_wizard_input.log` will be created containing the input values supplied to Detect Wizard and a tree view of all files in the project; useful for debugging. 

The file `latest_detect_run.txt will` contain the console output of Detect Wizard including the Synopsys Detect log.

The `-b` or `--bdignore` option will create multiple .bdignore files in sub-folders beneath the project folder if they do not already exist. The .bdignore files 
will be created in parent folders of duplicate folders or those containing only binary files for exclusion. USE WITH CAUTION as it will cause specified folders 
to be permanently ignored by the Signature scan until the .bdignore files are removed.
