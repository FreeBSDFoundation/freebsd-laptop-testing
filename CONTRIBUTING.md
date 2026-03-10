# Help us test more laptops and desktops!

The [Laptop and Support Usability project](https://github.com/FreeBSDFoundation/proj-laptop) is committed to ensuring that FreeBSD works on [these test targets](https://github.com/FreeBSDFoundation/proj-laptop/tree/main/supported). However, we want FreeBSD to run smoothly on the laptops and desktops that you use! We would appreciate any help to test and validate your desired configurations as well.

## Getting started

```sh
pkg install python hw-probe
git clone https://github.com/FreeBSDFoundation/freebsd-laptop-testing
cd freebsd-laptop-testing
make
```

**NOTE:** Your root password will be needed to enumerate your system's hardware with [linuxhw/hw-probe](https://github.com/linuxhw/hw-probe).

After these steps, a new directory corresponding to your system will be generated inside `test_results/`. This will contain sections pertaining to devices on your system that are working and not working, along with more verbose output at the bottom.

To contribute these test results, create a new pull request containing the new directory and answer the "User Stories" questionnaire in the PR's description.
 
## What contributions we need

Any recent laptop hardware would be very helpful for our testing project. The more platforms we can gather test data for, the better we can make the FreeBSD experience on laptops be. Since Wi-Fi is a core focus of the FreeBSD Laptop Project, a wide variety of network card vendors would be very helpful for developers.  

### Need help?

For the Laptop Integration Testing Project specifically, we use Github Issues solely to triage and track open tasks that are assigned to The FreeBSD Foundation's staff. For this reason, issue creation in this repository is locked to Foundation staff only.

We also keep Github Discussions open for you to:
* Report bugs
* Request more testing coverage
* Ask about a particular scenario
* Ask for help to get started with testing on a particular system
* Talk about anything relevant to general laptop and desktop testing

If you have anything to say, please don't hesitate to post in a Discussion! Our staff will file Issues for any actionable items arise from the discussion.
