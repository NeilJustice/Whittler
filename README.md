# Whittler

Whittler is a Python command line program which facilitates the figurative "whittling away" (deletion) of "inessential" standard output text, especially Linux `program_name --help` standard output text, resulting in a file containing only "essential" standard output text which can be repeatedly reopened with Whittler for continued whittling.

For example, when learning a new Linux program such as `ansible`, `whittler ansible --help` can be repeatedly invoked to iteratively "whittle away" command line argument descriptions so as to be left with a text file containing only `ansible` command line arguments not yet experimented with.

|Build Type|Build Status|
|----------|------------|
|GitHub Actions build for ubuntu-latest and windows-latest|[![Whittler](https://github.com/NeilJustice/Whittler/actions/workflows/build.yml/badge.svg)](https://github.com/NeilJustice/Whittler/actions/workflows/build.yml)|
|Codecov.io Python code coverage|[![codecov](https://codecov.io/gh/NeilJustice/Whittler/branch/main/graph/badge.svg?token=g9qpHBaepU)](https://codecov.io/gh/NeilJustice/Whittler)|
|SonarCloud Python static analysis|[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=NeilJustice_Whittler&metric=alert_status)](https://sonarcloud.io/dashboard?id=NeilJustice_Whittler)|

* [Whittler command line usage](#whittler-command-line-usage)
* [Whittler program behavior](#whittler-program-behavior)
* [Whittler Python code structure as it appears in Visual Studio Code on Linux](#whittler-python-code-structure-as-it-appears-in-visual-studio-code-on-linux)
* [Whittler Python code structure as it appears in Visual Studio 2019 on Windows](#whittler-python-code-structure-as-it-appears-in-visual-studio-2019-on-windows)
* [Linux Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then pyinstaller creates Linux binary whittler](#linux-jenkins-job-which-unit-tests-mypys-flake8s-pylints-sonarqube-scans-then-pyinstaller-creates-linux-binary-whittler)
* [Windows Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then pyinstaller creates Windows executable Whittler.exe](#windows-jenkins-job-which-unit-tests-mypys-flake8s-pylints-sonarqube-scans-then-pyinstaller-creates-windows-executable-whittlerexe)
* [4 steps to build binary whittler from source on Linux with PyInstaller](#4-steps-to-build-binary-whittler-from-source-on-linux-with-pyinstaller)
* [4 steps to build executable Whittler.exe from source on Windows with PyInstaller](#4-steps-to-build-executable-whittlerexe-from-source-on-windows-with-pyinstaller)

## Whittler command line usage

```html
Whittler v0.7.0 - Facilitates the figurative whittling away of program standard output text.

Usage: whittler <ProgramName> [ProgramArguments...]

Whittler writes standard output text from a given command line
to file ~/.config/Whittler/<CommandLine>.txt for editing with the EDITOR-defined text editor.

If Whittler has been run previously with the exact same command line arguments,
file ~/.config/Whittler/<CommandLine>.txt is opened with EDITOR for continued whittling.

Example sequence of Whittler invocations:
whittler ag --help
whittler ag --help
whittler ag --help
```

(`ag` is the excellent command line program Silver Searcher for quickly finding file text and file names.)

## Whittler program behavior

The main use case for Whittler is to "whittle away" command line argument descriptions for Linux programs in the process of being learned, resulting in a text file containing only not-yet-experimented-with command line arguments.

For example, when `whittler ansible --help` is run, standard output for `ansible --help` is written to file `~/.config/Whittler/ansible --help.txt` and is then opened with the `$EDITOR` text editor.

In this screenshot, `$EDITOR` is defined as `nvim`, and contents of directory `~/.config/Whittler` is listed having having run `whittler ansible --help`:

![Whittler command line](Screenshots/Linux/WhittlerCommandLine.png)

Here is the starting, not-yet-whittled standard output text for `ansible --help`:

![ansible --help](Screenshots/Linux/AnsibleHelp.png)

Here is the initial view in `nvim` of `whittler ansible --help` with leading spaces removed by Whittler so as to prepare the text for further whittling:

![ansible Whittler phase 1](Screenshots/Linux/AnsibleWhittlerPhase1.png)

After an initial bout of text whittling, here is one possible instance of whittled-down text for `ansible --help` as opened in `nvim` with `whittler ansible --help`:

![ansible Whittler phase 2](Screenshots/Linux/AnsibleWhittlerPhase2.png)

Thereafter, whenever `whittler ansible --help` is run, existing file `~/.config/Whittler/ansible --help.txt` is reopened with `$EDITOR` for continued editing / whittling.

## Whittler Python code structure as it appears in Visual Studio Code on Linux

Shown in this screenshot is the `run` function in `Process.py` for running the specified command line and returning its standard output and standard error text:

![Whittler code in Visual Studio Code](Screenshots/Linux/WhittlerCodeInVisualStudioCode.png)

## Whittler Python code structure as it appears in Visual Studio 2019 on Windows

Shown in this screenshot is the code that writes either `stdout` or `stderr` to Whittler file `~/.config/Whittler/<Command>.txt`:

![Whittler code in Visual Studio 2019](Screenshots/Windows/WhittlerCodeInVisualStudio2019.png)

## Linux Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then pyinstaller creates Linux binary whittler

![Linux Whittler Jenkins job](Screenshots/Linux/LinuxJenkinsJob.png)

## Windows Jenkins job which unit tests, mypys, flake8s, pylints, SonarQube scans, then Pyinstaller creates Windows executable Whittler.exe

![Windows Whittler Jenkins job](Screenshots/Windows/WindowsJenkinsJob.png)

## 4 steps to build binary whittler from source on Linux with PyInstaller

```bash
git clone https://github.com/NeilJustice/Whittler
cd Whittler
./JenkinsJobs/Linux/Whittler.ps1
sudo ./JenkinsJobs/Linux/Whittler-Install.ps1
```

Resulting binary `/usr/local/bin/whittler`:

![whittler on Linux](Screenshots/Linux/WhittlerBinary.png)

## 4 steps to build executable Whittler.exe from source on Windows with PyInstaller

```powershell
git clone https://github.com/NeilJustice/Whittler
cd Whittler
.\JenkinsJobs\Windows\Whittler.ps1
.\JenkinsJobs\Windows\Whittler-Install.ps1
```

Resulting executable `C:\bin\Whittler.exe`:

![Whittler.exe on Windows](Screenshots/Windows/WhittlerDotExe.png)
