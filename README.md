# NasdaqDataLink

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) ![GitHub last commit](https://img.shields.io/github/last-commit/NeilJustice/NasdaqDataLink)

NasdaqDataLink is a Python command line program which facilitates the figurative "whittling away" (deletion) of "inessential" standard output text, especially Linux `program_name --help` standard output text, resulting in a file containing only "essential" standard output text which can be repeatedly reopened with NasdaqDataLink for continued whittling.

For example, when learning a new Linux program such as `ansible`, `nasdaqDataLink ansible --help` can be repeatedly invoked to iteratively "whittle away" command line argument descriptions so as to be left with a text file containing only `ansible` command line arguments not yet experimented with.

|Build Type|Build Status|
|----------|------------|
|GitHub Actions build for ubuntu-latest and windows-latest|[![NasdaqDataLink](https://github.com/NeilJustice/NasdaqDataLink/actions/workflows/build.yml/badge.svg)](https://github.com/NeilJustice/NasdaqDataLink/actions/workflows/build.yml)|
|Codecov.io Python code coverage|[![codecov](https://codecov.io/gh/NeilJustice/NasdaqDataLink/branch/main/graph/badge.svg?token=g9qpHBaepU)](https://codecov.io/gh/NeilJustice/NasdaqDataLink)|
|SonarCloud Python static analysis|[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=NeilJustice_NasdaqDataLink&metric=alert_status)](https://sonarcloud.io/dashboard?id=NeilJustice_NasdaqDataLink)|

* [NasdaqDataLink command line usage](#nasdaqDataLink-command-line-usage)
* [NasdaqDataLink program behavior](#nasdaqDataLink-program-behavior)
* [NasdaqDataLink Python code structure as it appears in Visual Studio Code on Linux](#nasdaqDataLink-python-code-structure-as-it-appears-in-visual-studio-code-on-linux)
* [NasdaqDataLink Python code structure as it appears in Visual Studio 2019 on Windows](#nasdaqDataLink-python-code-structure-as-it-appears-in-visual-studio-2019-on-windows)
* [Linux Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then pyinstaller creates Linux binary nasdaqDataLink](#linux-jenkins-job-which-unit-tests-mypys-flake8s-pylints-sonarqube-scans-then-pyinstaller-creates-linux-binary-nasdaqDataLink)
* [Windows Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then pyinstaller creates Windows executable NasdaqDataLink.exe](#windows-jenkins-job-which-unit-tests-mypys-flake8s-pylints-sonarqube-scans-then-pyinstaller-creates-windows-executable-nasdaqDataLinkexe)
* [4 steps to build binary nasdaqDataLink from source on Linux with PyInstaller](#4-steps-to-build-binary-nasdaqDataLink-from-source-on-linux-with-pyinstaller)
* [4 steps to build executable NasdaqDataLink.exe from source on Windows with PyInstaller](#4-steps-to-build-executable-nasdaqDataLinkexe-from-source-on-windows-with-pyinstaller)

## NasdaqDataLink command line usage

```html
NasdaqDataLink v0.7.0 - Facilitates the figurative whittling away of program standard output text.

Usage: nasdaqDataLink <ProgramName> [ProgramArguments...]

NasdaqDataLink writes standard output text from a given command line
to file ~/.config/NasdaqDataLink/<CommandLine>.txt for editing with the EDITOR-defined text editor.

If NasdaqDataLink has been run previously with the exact same command line arguments,
file ~/.config/NasdaqDataLink/<CommandLine>.txt is opened with EDITOR for continued whittling.

Example sequence of NasdaqDataLink invocations:
nasdaqDataLink ag --help
nasdaqDataLink ag --help
nasdaqDataLink ag --help
```

(`ag` is the excellent command line program Silver Searcher for quickly finding file text and file names.)

## NasdaqDataLink program behavior

The main use case for NasdaqDataLink is to "whittle away" command line argument descriptions for Linux programs in the process of being learned, resulting in a text file containing only not-yet-experimented-with command line arguments.

For example, when `nasdaqDataLink ansible --help` is run, standard output for `ansible --help` is written to file `~/.config/NasdaqDataLink/ansible --help.txt` and is then opened with the `$EDITOR` text editor.

In this screenshot, `$EDITOR` is defined as `nvim`, and contents of directory `~/.config/NasdaqDataLink` is listed having having run `nasdaqDataLink ansible --help`:

![NasdaqDataLink command line](Screenshots/Linux/NasdaqDataLinkCommandLine.png)

Here is the starting, not-yet-whittled standard output text for `ansible --help`:

![ansible --help](Screenshots/Linux/AnsibleHelp.png)

Here is the initial view in `nvim` of `nasdaqDataLink ansible --help` with leading spaces removed by NasdaqDataLink so as to prepare the text for further whittling:

![ansible NasdaqDataLink phase 1](Screenshots/Linux/AnsibleNasdaqDataLinkPhase1.png)

After an initial bout of text whittling, here is one possible instance of whittled-down text for `ansible --help` as opened in `nvim` with `nasdaqDataLink ansible --help`:

![ansible NasdaqDataLink phase 2](Screenshots/Linux/AnsibleNasdaqDataLinkPhase2.png)

Thereafter, whenever `nasdaqDataLink ansible --help` is run, existing file `~/.config/NasdaqDataLink/ansible --help.txt` is reopened with `$EDITOR` for continued editing / whittling.

## NasdaqDataLink Python code structure as it appears in Visual Studio Code on Linux

Shown in this screenshot is the `run` function in `Process.py` for running the specified command line and returning its standard output and standard error text:

![NasdaqDataLink code in Visual Studio Code](Screenshots/Linux/NasdaqDataLinkCodeInVisualStudioCode.png)

## NasdaqDataLink Python code structure as it appears in Visual Studio 2019 on Windows

Shown in this screenshot is the code that writes either `stdout` or `stderr` to NasdaqDataLink file `~/.config/NasdaqDataLink/<Command>.txt`:

![NasdaqDataLink code in Visual Studio 2019](Screenshots/Windows/NasdaqDataLinkCodeInVisualStudio2019.png)

## Linux Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then pyinstaller creates Linux binary nasdaqDataLink

![Linux NasdaqDataLink Jenkins job](Screenshots/Linux/LinuxJenkinsJob.png)

## Windows Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then Pyinstaller creates Windows executable NasdaqDataLink.exe

![Windows NasdaqDataLink Jenkins job](Screenshots/Windows/WindowsJenkinsJob.png)

## 4 steps to build binary nasdaqDataLink from source on Linux with PyInstaller

```bash
git clone https://github.com/NeilJustice/NasdaqDataLink
cd NasdaqDataLink
./JenkinsJobs/Linux/NasdaqDataLink.ps1
sudo ./JenkinsJobs/Linux/NasdaqDataLink-Install.ps1
```

Resulting binary `/usr/local/bin/nasdaqDataLink`:

![nasdaqDataLink on Linux](Screenshots/Linux/NasdaqDataLinkBinary.png)

## 4 steps to build executable NasdaqDataLink.exe from source on Windows with PyInstaller

```powershell
git clone https://github.com/NeilJustice/NasdaqDataLink
cd NasdaqDataLink
.\JenkinsJobs\Windows\NasdaqDataLink.ps1
.\JenkinsJobs\Windows\NasdaqDataLink-Install.ps1
```

Resulting executable `C:\bin\NasdaqDataLink.exe`:

![NasdaqDataLink.exe on Windows](Screenshots/Windows/NasdaqDataLinkDotExe.png)
