# Help us test more laptops and desktops!

The Laptop and Support Usability project is committed to ensure that FreeBSD works on [these supported configurations](https://github.com/FreeBSDFoundation/proj-laptop/tree/main/supported). However, we want FreeBSD to run smoothly on the systems that you use! We would appreciate any help to test and validate your desired configurations as well.

## Getting started

1. First, `git clone` this repo. then run `pkg install python hw-probe` and type `make`. Supply your root password when prompted and a new file will be generated inside the `test_results` directory.

2. Enter the `test_results` directory and view the file. The file will contain sections pertaining to devices on your system that are working and not working, along with more verbose output at the bottom.

3. Create a new pull request with the file attatched. 
 
## What contributions we need

Any recent laptop hardware would be very helpful for our testing project. The more platforms we can gather test data for, the better we can make the FreeBSD experience on laptops be. Since Wi-Fi is a core focus of the FreeBSD Laptop Project, a wide variety of network card vendors would be very helpful for developers.  

### Issues

For the Laptop Integration Testing Project specifically, we use Github Issues solely to triage and track open tasks that are assigned to our testers on the [project board](https://github.com/users/svmhdvn/projects/2). For this reason, issue creation in this repository is locked to Foundation staff only.

Instead, we keep Github Discussions open for you to:
* Report bugs
* Request more testing coverage
* Ask about a particular scenario
* Ask for help to get started with testing on a particular system
* Talk about anything relevant to general laptop and desktop testing

If you have anything to say, please don't hesitate to post in a Discussion! If any actionable items arise from the discussion, our staff will file an Issue for it.

### Pull Requests

