# Help us test more laptops and desktops!

The Laptop and Support Usability project is committed to ensure that FreeBSD works on [these supported configurations](https://github.com/FreeBSDFoundation/proj-laptop/tree/main/supported). However, we want FreeBSD to run smoothly on the systems that you use! We would appreciate any help to test and validate your desired configurations as well.

This guide provides regarding how to test your laptop or desktop with FreeBSD, collecting hardware data using hw-probe, and steps to convert your hw-probe dump into a user-friendly list of devices that are working, which will improve our database of supported platforms.

## Getting started

You will need `hw-probe`, which is in the FreeBSD ports tree as [sysutils/hw-probe](https://www.freshports.org/sysutils/hw-probe/). Once installed, run `hw-probe -all` to create a raw dump of your system's devices. This dump will be converted into a human-readable format using TODO, which provides a more user-friendly insight into which devices are currently supported on FreeBSD on your system.

## What contributions we need

TODO

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

- Update CONTRIBUTING.md to have information on what the guide provides and how to use hw-probe
- Provide information on contributions needed to the repo
