# Whittler

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) ![GitHub last commit](https://img.shields.io/github/last-commit/NeilJustice/Whittler)

Whittler is a Python command line program which facilitates the figurative "whittling away" (deletion) of standard output text, especially Linux `program_name --help` standard output text, resulting in a file containing only the most useful standard output text.

For example, when learning a new Linux executable such as `ansible-playbook`, one can repeatedly invoke `whittler ansible-playbook --help` to iteratively "whittle away" command line arguments and command line argument descriptions so as to have a text file containing only `ansible-playbook` command line arguments not yet learned or experimented with.

|Build Type|Build Status|
|----------|------------|
|GitHub Actions build for Linux, MacOS, and Windows|[![Whittler](https://github.com/NeilJustice/Whittler/actions/workflows/build.yml/badge.svg)](https://github.com/NeilJustice/Whittler/actions/workflows/build.yml)|
|Codecov.io code coverage|[![codecov](https://codecov.io/gh/NeilJustice/Whittler/branch/main/graph/badge.svg?token=g9qpHBaepU)](https://codecov.io/gh/NeilJustice/Whittler)|
|SonarCloud static analysis|[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=NeilJustice_Whittler&metric=alert_status)](https://sonarcloud.io/dashboard?id=NeilJustice_Whittler)|

* [Whittler Command Line Usage](#whittler-command-line-usage)
* [Whittler Program Behavior](#whittler-program-behavior)
* [Whittler Python Code Structure As It Appears In Visual Studio Code On Linux](#whittler-python-code-structure-as-it-appears-in-visual-studio-code-on-linux)
* [Whittler Python Code Structure As It Appears In Visual Studio 2019 On Windows](#whittler-python-code-structure-as-it-appears-in-visual-studio-2019-on-windows)
* [Linux Jenkins Job Which Unit Tests, Mypys, Flake8s, Pylints, SonarQubes, then Pyinstaller Creates Linux Binary whittler](#linux-jenkins-job-which-unit-tests-mypys-flake8s-pylints-sonarqubes-then-pyinstaller-creates-linux-binary-whittler)
* [Windows Jenkins Job Which Unit Tests, Mypys, Flake8s, Pylints, SonarQubes, then Pyinstaller Creates Windows Executable Whittler.exe](#windows-jenkins-job-which-unit-tests-mypys-flake8s-pylints-sonarqubes-then-pyinstaller-creates-windows-executable-whittler.exe)
* [How To Build And Install Binary whittler From Source On Linux](#how-to-build-and-install-binary-whittler-from-source-on-linux)
* [How To Build And Install Executable Whittler.exe From Source On Windows](#how-to-build-and-install-executable-whittlerexe-from-source-on-windows)
* [Whittler Roadmap](#roadmap)

## Whittler Command Line Usage

```text
Whittler v0.7.0
https://github.com/NeilJustice/Whittler

Usage: whittler <ProgramName> [ProgramArguments...]

Whittler writes standard output text from a given command line
to file ~/.config/Whittler/<CommandLine>.txt for editing with the EDITOR-defined text editor.
If Whittler has been run previously with the exact same command line arguments,
file ~/.config/Whittler/<CommandLine>.txt is opened with EDITOR for continued editing.
```

## Whittler Program Behavior

The prime use case for Whittler is to "whittle away" command line arguments and command line argument descriptions of new Linux programs in the process of being learned, resulting in a file containing only not-yet-experimented-with command line arguments.

For example, when `whittler ansible --help` is run, standard output for `ansible --help` is written to file `~/.config/Whittler/ansible --help.txt` and is then opened with the `$EDITOR` text editor.

![Whittler command line](Screenshots/Linux/WhittlerCommandLine.png)

Here is the starting, not-yet-whittled standard output text for `ansible --help`:

![ansible --help](Screenshots/Linux/AnsibleHelp.png)

Here is the initial view in `nvim` of `whittler ansible --help` with leading spaces removed by Whittler so as to prepare the text for further whittling:

![ansible Whittler phase 1](Screenshots/Linux/AnsibleWhittlerPhase1.png)

After an initial bout of text whittling, here is one possible instance of whittled-down text for `ansible --help` as opened in `nvim` with `whittler ansible --help`:

![ansible Whittler phase 2](Screenshots/Linux/AnsibleWhittlerPhase2.png)

Thereafter, whenever `whittler ansible --help` is run, file `~/.config/Whittler/ansible --help.txt` will be reopened with `$EDITOR` for continued editing / whittling.

## Whittler Python Code Structure As It Appears In Visual Studio Code On Linux

Seen in this screenshot is the `run` function in `Process.py` for running the to-be-whittled command line and returning its standard output and standard error text:

![Whittler code in Visual Studio Code](Screenshots/Linux/WhittlerCodeInVisualStudioCode.png)

## Whittler Python Code Structure As It Appears In Visual Studio 2019 On Windows

Seen in this screenshot is the code that writes either `stdout` or `stderr` to Whittler file `~/.config/Whittler/<Command>.txt`:

![Whittler code in Visual Studio 2019](Screenshots/Windows/WhittlerCodeInVisualStudio2019.png)

## Linux Jenkins Job Which Unit Tests, Mypys, Flake8s, Pylints, SonarQubes, then Pyinstaller Creates Linux Binary whittler

A Jenkins Blue Ocean build pipeline builds the following Whittler Jenkins job on Fedora 33 with Python 3.9.2:

![Linux Whittler Jenkins job](Screenshots/Linux/LinuxJenkinsJob.png)

## Windows Jenkins Job Which Unit Tests, Mypys, Flake8s, Pylints, SonarQubes, then Pyinstaller Creates Windows Executable Whittler.exe

A Jenkins Blue Ocean build pipeline builds the following Whittler Jenkins job on Windows 10 with Python 3.9.4:

![Windows Whittler Jenkins job](Screenshots/Windows/WindowsJenkinsJob.png)

## How To Build And Install Binary whittler From Source On Linux

```bash
git clone https://github.com/NeilJustice/Whittler
cd Whittler
./JenkinsJobs/Linux/Whittler.ps1
sudo ./JenkinsJobs/Linux/Whittler-Install.ps1
```

Resulting binary `/usr/local/bin/whittler`:

![whittler on Linux](Screenshots/Linux/WhittlerBinary.png)

## How To Build And Install Executable Whittler.exe From Source On Windows

```powershell
git clone https://github.com/NeilJustice/Whittler
cd Whittler
.\JenkinsJobs\Windows\Whittler.ps1
.\JenkinsJobs\Windows\Whittler-Install.ps1
```

Resulting executable `C:\bin\Whittler.exe`:

![Whittler.exe on Windows](Screenshots/Windows/WhittlerDotExe.png)

## Whittler Roadmap

|Feature Feature|Implementation Status|
|---------------|---------------------|
|GitHub Actions build|Awaiting implementation|
|100% Codecov.io badge|Awaiting implementation|
|Replace unittest with pytest|Awaiting implementation|
