# AI Certification Quiz App

## Table of Contents
- [About](#about)
- [Project Objectives](#project_objectives)
- [Features](#features)
- [How to Run](#how_to_run)
- [How the Quiz Works](#how_the_quiz_works)
- [Future Improvements](#future_improvements)
- [Disclaimer](#disclaimer)

## About
This desktop application was developed as a structured study tool for the certification: «Εφαρμογές Τεχνητής Νοημοσύνης»
The certification is delivered by goLearn, a licensed Κέντρο Διά Βίου Μάθησης (ΚΔΒΜ) in Greece, with assessment support from UCERT.
As part of the preparation process, a set of 28 indicative questions was provided. Instead of simply reviewing them passively, I transformed them into a fully interactive graphical quiz application using Python.

## Project Objectives
- Develop a structured desktop application using Python
- Implement multiple question types dynamically
- Handle scoring logic and answer validation
- Design a clean and user-friendly graphical interface
- Apply object-oriented programming principles
- Simulate an exam-like experience

## Features
- Single-choice questions (Radio Buttons)
- Multiple-selection questions (Checkboxes with strict validation)
- Fill-in-the-blanks questions (Dropdown menus)
- Randomized question order on each run
- Automatic scoring system
- Percentage calculation
- Detailed review of incorrect answers
- Restart functionality with reshuffling

## How to Run
1. Run with Python:
     Make sure Python 3 is installed.
   `python quiz.py`
2. Run the .exe:
   1. Double-click quiz.exe
   2. The quiz launches immediately
   3. No Python installation required

## How the Quiz Works
Questions are shuffled randomly at startup. The user must answer each question before proceeding. Multi-selection questions require selecting the exact number of correct answers. Fill-in-the-blanks questions require all blanks to be completed.
At completion:
- Total score is displayed
- Percentage is calculated
- Incorrect answers are listed with correct solutions

## Future Improvements
- Make the quiz in other languages
- Load questions from an external JSON file
- Add countdown timer per question
- Store user performance history
- Add difficulty levels
- Add dark mode
- Convert to a web-based version (Flask / FastAPI)
- Deploy as a web app

## Disclaimer
This is a personal educational project created for certification preparation.
It is not officially affiliated with, endorsed by, or connected to goLearn, UCERT, or any related organization.
The questions are used strictly for personal study and exam simulation purposes.
