Title: Dokku on Debian: Tips &amp; Tricks
Date: 2014-05-29
Tags: devops
Slug: dokku_debian
Author: Martin Putniorz
Summary: How to get your Debian based Heroku up and running

As you might know, [Dokku](https://github.com/progrium/dokku) officialy supports Ubuntu (14.04 x64 or 12.04 x64). But Ubuntu (at least on server) is just Debian, so there's no reason, why it should not work, right? Wrong - but I'm gonna show you problems and possible solution, that I've used.

## Dokku installation

First problem you encounter during execution of bootstrap script. It uses ```add-apt-repository``` helper, which is custom Ubuntu command. Workaround is pretty easy, but a little bit messy - you just get your own helper script:

    :::shell-session
    # wget http://blog.anantshri.info/content/uploads/2010/09/add-apt-repository.sh.txt
    # cp add-apt-repository.sh.txt /usr/sbin/add-apt-repository
    # chmod o+x /usr/sbin/add-apt-repository

Now just execute bootstrap again and all should be fine. Right?

## sshcommand 

Dokku is using [sshcommand](https://github.com/progrium/sshcommand) to propagate itself through ```ssh```. This is really neat, because during bootstrap *dokku* user is created to execute commands remotely. There's only a tiny little problem. This user is passwordless and works only on key basis. Which is cool if you are on Ubuntu, because such user is fully operational. Debian on the other hand just **locks it**. Without password you are screwed even if you disable password auth through *secure shell*. Solution? Just add some random password to *dokku* user (I've generated it using [pass](http://www.passwordstore.org/)):

    (local) $ pass generate citra/dokku 20
    (remote) # usermod -p '<new_password>' dokku
    (remote) # passwd -u dokku

## acl-add 

Adding you public key to *dokku* control keys is also kinda tricky. Standard command from project README:

    $ cat ~/.ssh/id_rsa.pub | ssh progriumapp.com "sudo sshcommand acl-add dokku <alias>"

does not work, because (at least in my case), sudo considered parts of my key my passwords (if you are a badass with passwordless sudo, you are going to be fine). So I just executed it on the server:

    # sshcommand acl-add dokku <alias>
    (paste key)^D

## Deploy

Now you should be able to just deploy and use dokku@your_server shell according to README. I'm considering writing a follow-up about some [plugins](https://github.com/progrium/dokku/wiki/Plugins) and how to get them working without Ubuntu underneath. Have you encountered any other issues with Dokku on Debian? Please, share it in comments.  