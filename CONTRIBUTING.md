# Help us test more laptops and desktops!

The Laptop and Support Usability project is committed to ensure that FreeBSD works on [these supported configurations](https://github.com/FreeBSDFoundation/proj-laptop/tree/main/supported). However, we want FreeBSD to run smoothly on the systems that you use! We would appreciate any help to test and validate your desired configurations as well.

This guide provides information on how to test your laptop or desktop with FreeBSD. We are gathering hardware data using hw-probe into a user-friendly list of devices that are working, which will improve our database of supported platforms.

## Getting started

1. You will need `hw-probe`, which can be downloaded from `pkg` or found in the ports tree at [/sysutils/hw-probe](https://www.freshports.org/sysutils/hw-probe/).

2. Run `hw-probe -all` as root. The tool will tell you where it stored its raw data, the `devices` file inside the hw.info folder is what we are interested in.

3. Create a PR with your devices file and a file will be generated that contains a more readable version of your hardware status.
 
## What contributions we need


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

