# Rules of Inference Auto Generator/Grader

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![image](https://github.com/jorofino3/roi-gen/assets/97992795/1b49a671-e39a-494e-a93b-1945165380d7)
![image](https://github.com/jorofino3/roi-gen/assets/97992795/7cf21245-4872-48c1-af4e-d7b052c75c57)
![image](https://github.com/jorofino3/roi-gen/assets/97992795/ec71990b-bb5b-4bb1-9a32-e89a127205cb)
![image](https://github.com/jorofino3/roi-gen/assets/97992795/8fd4974b-34d9-470c-85cc-90c6d7708c15)
![image](https://github.com/jorofino3/roi-gen/assets/97992795/197138c4-4f1b-4b90-9aff-a4262039f27f)

Welcome to the Rules of Inference Problem Generator! This project, developed over the past two semesters (Spring 2023 and Fall 2023), is designed to automatically generate problems related to rules of inference for logic enthusiasts and students alike.

# Table of Contents

- [Installation-Guide](#Installation-Guide)
- [Deployment-Instructions](#Deployment-Instructions)
- [Release-Notes](#Release-Notes)

# Installation-Guide

## Pre-requisites

* [Python 3](https://www.python.org/downloads/)
* [Java](https://www.java.com/download/ie_manual.jsp)
* [MongoDB](https://www.mongodb.com/try/download/community)
* [Node / npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* [make (optional)](https://gnuwin32.sourceforge.net/packages/make.htm)

## Dependent libraries that must be installed

* pymongo 
* flask 
* flask-cors

## Download instructions

* Beyond downloading pre-requisite software and libraries, cloning this repo is all you should need

## Build instructions

* The only binaries that need to be built are the Java binaries
* Steps:
1. `cd` into `algo`
2. `cd` into `solver`
3. invoke `make` or manually run command listed in troubleshooting
4. verify that `.class` files are present in a newly created `bin` folder in `solver`

## Run instructions

### Backend
* Place your MongoDB cluster `db = database.cluster_connect(YOUR_LINK_HERE)`, replacing `YOUR_LINK_HERE`
* Run index.py -- `python index.py`found in the `server` directory.

### Algorithm
* To start the `flask` server which serves the algo run `python problem.py`

- If you want to just see the algorithm work (another way to check to see if the java binaries compiled correctly), `cd` into `algo` and run `python executor.py`
- This should output a json representation of the problem
- You can change the difficulty by modifying the string in the `executor.py` file


#### Frontend
* `cd` to the `client` directory.
* Run `npm install`
* Then run `npm run dev` to start the frontend
* The website should open on 



## Troubleshooting

Some systems (base windows) do not have make installed. You can manually run a compile command instead: `javac -d bin src/engine/AtomicStatement.java src/engine/Inference.java src/engine/LogicalConnective.java src/engine/ProofSpace.java src/engine/Statement.java src/Solver.java`

If `javac` is not a valid command, ensure that your PATH variables are set correctly and that you have the Java Compiler (install the JDK)


# Deployment-Instructions

## Backend
Please visit https://hosting.gatech.edu/about/dedicated-server for detailed instructions on how to obtain a private VM on GT servers to run the backend.
## Frontend

The following instructions are for deploying the frontend to a Vercel Application. The full documentation for these steps can be found [here](https://docs.astro.build/en/guides/deploy/vercel/) 3. **Update Astro Project:**

- Update your Astro project code as required by the backend deployment. This includes setting the enviorment variables for the MongoDB Clust, following the instructions [here](https://docs.astro.build/en/guides/configuring-astro/#environment-variables).

2. **Finish Configuring the Project:**

   - cd into the `client` directory.
   - Follow these steps [here](https://docs.astro.build/en/guides/deploy/vercel/#adapter-for-ssr) to finish configuring the project.

3. **Create a Vercel Account:**

   - Create an account with your GATECH Github Account (here)[https://vercel.com/signup]
   - Click 'Import' on the GitHub Reposity
   - Give the Project a Name
   - Click 'Deploy'

   --- IM NOTE SURE IF THIS WILL WORK WITH HIS CONFIG

4. **Connect to Vercel:**

   - Install the Vercel CLI by running `npm install -g vercel`.
   - Deploy your Astro project with `vercel` as described [here](https://docs.astro.build/en/guides/deploy/vercel/#deploy-to-vercel).
   - ...

Remember to consult the [official Astro documentation](https://docs.astro.build/) and [Vercel documentation](https://vercel.com/docs) for additional details and troubleshooting.


# Release-Notes

### Version 0.5.0

#### New Features
Backend
* Algo - Refined random generation algorithm, included setup details in setup below
* Database - Functionalities relating to statistics of students have been created

Frontend
* Exporting statistics now requires an admin passkey
* Routing issues between pages have been fixed

#### Known Issues
* N/A

#### Bug Fixes
* Algo - per the client's feedback, we have fixed an issue in which contradicting statements could be generated
* Frontend - multiple routing issues have been fixed

### Version 0.4.0

#### New Features
Backend
* Algo - Random Problem has been fully implemented alongside the web server API - this algorithm can be tweaked without any change to front end resources
* Database - More features relating to stat tracking for instructors and students have been implemented

Frontend
* Frontend now integrated with backend algorithm via web server API
* Users can now generate problems of varying difficulty to practice
* Users can generate random, unique problems
* Statistics page - We have implemented the ability for instructors to export global statistics

#### Known Issues
* Algo - Conclusion is included as part of the list of premises; we instead put this into its own json key value pair (conclusion: "example")
* Front End - No way of directly generating a new problem; need to swap between difficulties / refresh page; this will be fixed with a button in Sprint 5

#### Bug Fixes
* Algo - We are committing to keeping the JVM based Solver; it currently works and we are too deep to change this.

### Version 0.3.0

#### New Features
Backend
* Algo - Created base class structure for our generator alongside random generation for "easy" level problems
* Database - add guest login functions and additional user statistics

Frontend
* Implemented blank pages for problems, sign in, and routing

#### Known Issues
* Algo - Generator is still JVM based - we want to fully be on Python eventually

#### Bug Fixes
None

### Version 0.2.0

#### New Features
Jira / Project Tracking
* We have retro-actively re-created sprint 2 after its mysterious deletion
* We will not "complete" the sprint; it's just there to show our progress
* Github should have pull requests from the sprint 2 period, which is a better reflection of our work completed 
* Sprint 3 should be working properly - We will document this in our meeting minutes and will likely be mentioned during our sprint 2 retrospective

Backend
* Solver has been created with a python script to invoke Java
* Command line tool which takes in a file of premises which invokes a java subprocess to solve the rules of inference
* Database: User accounts - login capability, global user metrics, per-problem set metrics (problems that have/have not been completed yet)
* Database: Problem sets - Can create custom problem sets with varying length, accessible to users

Frontend
* Fully functional and visually stunning frontend landing page
* Navbar with logo, internal links, and call to action buttons
* Banner with Call to action and short descirption template
* About page, which links to more details about our features (documents in progress)
* Practice badges with beginner, intermediate, and advanced filtering
* Community tab (communities not yet added)
* Footer with moore detailed and legal info
* Light and Dark mode depending on user system settings
* responsive to larger, medium, and smaller screens

#### Known Issues
* Solver currently solves things naively - which can lead to extra steps or a non-terminating calculation
* Solver currently is in Java - the port did not pan out - we can revisit this in the future
* No community, links to features, or internal routing on click events

#### Bug Fixes
* None

### Version 0.1.0

#### New Features
* Develop API to interact between MongoDB Database and server
* Revised file structure for client, server, and ROI alogrithm
* Code formatter and Linter
* Frontend Client dependencies installed and setup

#### Known issues
* None

#### Bug Fixes
* None
---



