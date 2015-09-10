https://travis-ci.org/jeff1evesque/machine-learning.svg

Machine Learning
================

###Definition

Machine learning is a [subfield](http://en.wikipedia.org/wiki/Academic_disciplines) of [computer science](http://en.wikipedia.org/wiki/Computer_science) (CS) and [artificial intelligence](http://en.wikipedia.org/wiki/Artificial_intelligence) (AI) that deals with the construction and study of systems that can [learn](http://en.wikipedia.org/wiki/Learning) from data, rather than follow only explicitly programmed instructions.

- http://en.wikipedia.org/wiki/Machine_learning

Applications for machine learning include:

- [Object recognition](http://en.wikipedia.org/wiki/Object_recognition)
- [Natural language processing](http://en.wikipedia.org/wiki/Natural_language_processing)
- [Search engines](http://en.wikipedia.org/wiki/Search_engines)
- [Bioinformatics](http://en.wikipedia.org/wiki/Bioinformatics)
- [Stock market](http://en.wikipedia.org/wiki/Stock_market) analysis
- [Speech](http://en.wikipedia.org/wiki/Speech_recognition) and [handwriting recognition](http://en.wikipedia.org/wiki/Speech_recognition)
- [Sentiment analysis](http://en.wikipedia.org/wiki/Sentiment_analysis)
- [Recommender systems](http://en.wikipedia.org/wiki/Recommender_system)
- [Sequence mining](http://en.wikipedia.org/wiki/Sequence_mining), commonly referred as *data mining*
- [Computational advertising](http://en.wikipedia.org/wiki/Computational_advertising), and [Computational finance](http://en.wikipedia.org/wiki/Computational_finance)

In [machine learning](http://en.wikipedia.org/wiki/Machine_learning), support vector machines (SVMs) are [supervised learning](http://en.wikipedia.org/wiki/Supervised_learning) models with associated learning [algorithms](http://en.wikipedia.org/wiki/Algorithm) that analyze data and recognize patterns, used for [classification](http://en.wikipedia.org/wiki/Statistical_classification) and [regression analysis](http://en.wikipedia.org/wiki/Regression_analysis). 

- http://en.wikipedia.org/wiki/Support_vector_machine

###Overview

## Preconfiguration

This project implements puppets [r10k](https://github.com/puppetlabs/r10k) module via vagrants [plugin](https://github.com/jantman/vagrant-r10k). A requirement of this implementation includes a `Puppetfile` (already defined), which includes the following syntax:

```
#!/usr/bin/env ruby
## Install Module: stdlib (apt dependency)
mod 'stdlib',
  :git => "git@github.com:puppetlabs/puppetlabs-stdlib.git",
  :ref => "4.6.0"

## Install Module: apt (from master)
mod 'apt',
  :git => "git@github.com:puppetlabs/puppetlabs-apt.git"
...
```

Specifically, this implements the ssh syntax `git@github.com:account/repo.git`, unlike the following alternatives:

- `https://github.com/account/repot.git`
- `git://github.com/account/repot.git`

This allows r10k to clone the corresponding puppet module(s), without a deterrence of [DDoS](https://en.wikipedia.org/wiki/Denial-of-service_attack).  However, to implement the above syntax, ssh keys need to be generated, and properly assigned locally, as well as on the github account.

The following steps through how to implement the ssh keys with respect to github:

```bash
$ cd ~/.ssh/
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
Enter file in which to save the key (/Users/you/.ssh/id_rsa): [Press enter]
Enter passphrase (empty for no passphrase): [Type a passphrase]
Enter same passphrase again: [Type passphrase again]
$ ssh-agent -s
Agent pid 59566
$ ssh-add ~/.ssh/id_rsa
$ pbcopy < ~/.ssh/id_rsa.pub
```

**Note:** it is recommended to simply press enter, to keep default values when asked *Enter file in which to save the key*.  Also, if `ssh-agent -s` alternative for git bash doesn't work, then `eval $(ssh-agent -s)` for other terminal prompts should work.

Then, at the top of any github page (after login), click `Settings > SSH keys > Add SSH Keys`, then paste the above copied key into the `Key` field, and click *Add key*.  Finally, to test the ssh connection, enter the following within the same terminal window used for the above commands:

```bash
$ ssh -T git@github.com
The authenticity of host 'github.com (207.97.227.239)' can't be established.
RSA key fingerprint is 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'github.com,192.30.252.130' (RSA) to the list of known hosts.
Hi jeff1evesque! You've successfully authenticated, but GitHub does not provide shell access.
```

## Configuration

Fork this project in your GitHub account, then clone your repository:

```
cd /[PROJECT-DIRECTORY]
sudo git clone https://[YOUR-USERNAME]@github.com/[YOUR-USERNAME]/machine-learning.git
```

**Note:** change `[PROJECT-DIRECTORY]` to a desired directory path, and `[YOUR-USERNAME]` to your corresponding git username.

Then, add the *Remote Upstream*, this way we can pull any merged pull-requests:

```
cd /[PROJECT-DIRECTORY]
git remote add upstream https://github.com/[YOUR-USERNAME]/machine-learning.git
```

##Installation

In order to proceed with the installation for this project, two dependencies need to be installed:

- [Vagrant](https://www.vagrantup.com/)
- [Virtualbox](https://www.virtualbox.org/)

**Note:** more information can be found within the associated vagrant [wiki page](https://github.com/jeff1evesque/machine-learning/wiki/Vagrant).

Once the necessary dependencies have been installed, execute the following command to build the virtual environment:

```bash
cd /path/to/machine-learning/
vagrant up
```

Depending on the network speed, the build can take between 10-15 minutes.  So, grab a cup of coffee, and perhaps enjoy a danish while the virtual machine builds.  Remember, the application is intended to run on localhost, where the [`Vagrantfile`](https://github.com/jeff1evesque/machine-learning/blob/master/Vagrantfile) defines the exact port-forward on the host machine.

The following lines, indicate the application is accessible via `localhost:8080`, on the host machine:

```bash
...
  ## Create a forwarded port mapping which allows access to a specific port
  #  within the machine from a port on the host machine. In the example below,
  #  accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 5000, host: 8080
  config.vm.network "forwarded_port", guest: 443, host: 8585
...
```

Otherwise, if ssl is configured, then the application is accessible via `https://localhost:8585`, on the host machine.

**Note:** general convention implements port `443` for ssl.

##Testing / Execution

###Web Interface

This project provides a [web-interface](https://github.com/jeff1evesque/machine-learning/tree/master/templates/index.html), consisting of an HTML5 form, where users supply necessary training, or analysis information. During the training session, users provide csv, xml, or json file(s) representing the dataset(s). Upon form submission, user supplied form data is validated on the client-side (i.e. javascript), converted to a json object (python), validated on the server-side (python), stored into corresponding [EAV](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model) database tables (python, mariadb), then cached into nosql (redis) when appropriate.

When using the web-interface, it is important to ensure the csv, xml, or json file(s) are properly formatted. Dataset(s) poorly formatted will fail to create respective json dataset representation(s). Subsequently, the dataset(s) will not succeed being stored into corresponding database tables; therefore, no model, or prediction can be made.

The following are acceptable syntax:

- [CSV sample datasets](https://github.com/jeff1evesque/machine-learning/tree/master/html/machine-learning/data/csv/)
- [XML sample datasets](https://github.com/jeff1evesque/machine-learning/tree/master/html/machine-learning/data/xml/)
- [JSON sample datasets](https://github.com/jeff1evesque/machine-learning/tree/master/html/machine-learning/data/json/)

**Note:** each dependent variable value (for JSON datasets), is an array (square brackets), since each dependent variable may have multiple observations.

As mentioned earlier, the web application can be accessed after subsequent `vagrant up` command, followed by using a browser referencing localhost:8080 (or https://locoalhost:5050, with ssl), on the host machine.

###Programmatic Interface

Unavailable until milestone [0.2](https://github.com/jeff1evesque/machine-learning/milestones/0.2).

###Test Scripts

Unavailable until milestone [0.2](https://github.com/jeff1evesque/machine-learning/milestones/0.2).
