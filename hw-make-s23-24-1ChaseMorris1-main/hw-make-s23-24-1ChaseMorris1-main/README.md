[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=13585830)
<h2 align="center">
CS3560 Homework Assignment 2: Makefile (100 Points)<br/>
Due date: Please check the entry on Blackboard
</h2>

The purpose of this assignment is to help you get comfortable with a build system (GNU Make) and shell commands. Be ready to solve any error that occur! You are expected to read and try to understand program's output and error messages.

## 1 - Reading Assignments

Please read the following articles/book.

- [Dealing with Multiple (C++) Files](http://csundergrad.science.uoit.ca/courses/cpp-notes/notes/dealing-with-multiple-files.html) by Faisal Qureshi.
- At least Chapter 1, 2 and 3 of a book "Managing Projects with GNU Make" (2004) [http://www.oreilly.com/openbook/make3/book/](http://www.oreilly.com/openbook/make3/book/)
- [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- [About authentication with SAML single sign-on](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/about-authentication-with-saml-single-sign-on)
- [Authorizing a personal access token for use with SAML single sign-on](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on)

If you are planning on using SSH key, please read

- [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/enterprise-cloud@latest/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Authorizing an SSH key for use with SAML single sign-on](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-an-ssh-key-for-use-with-saml-single-sign-on)

## 2 - Installation of the Required Software

This can be skipped if you already have the required software. If you are on Windows, we highly recommend that
you [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install), and then install these softwares inside WSL.

- C++ Compiler: the GNU Compiler Collection (GCC) OR Clang
- GDB (if you install GCC)
- LLDB (if you install Clang)
- GNU Make
- Git (if it is not yet installed)
- tar (if it is not yet installed)

Use keyword like "how to install X on Y" in your preferred search engine if you need to know how to install
these softwares on your system.

## 3 - Solve the problems

Solve all of the following puzzles.

- `sandstorm`
- `odd-or-even-makefile`
- `broken-shell`
- `simple-project`

Please read the `README.md` file in each puzzle folder for the instructions.

## 5 - Commit and push to GitHub

We will be using your repository in GitHub Classroom to grade, so make sure to make a commit (or commits) of your solution
and push it out to GitHub.

If you need a refresher on how to push, please read [this article](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository).

## Submission

Submit the link to your Github Classroom repository to Blackboard.

## Appendix A - Running the grading scripts locally

You will need at least Python version 3.12 and the pacakges listed in `requirements.txt`.

## Appendix B - Common Errors

### SAML SSO Error

From [Authorizing a personal access token for use with SAML single sign-on](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on),

> To use a personal access token (classic) with an organization that uses SAML single sign-on (SSO), you must first authorize the token.

As the quote suggest, the token need to be authorized before it can be used with an organization that uses SAML SSO. Our OU-CS3560 is using
this SAML SSO, so you need to authorize your token. Please read the article above for how to authorize your token.

### Unable to access / The requested URL returned error: 403

This is when you get the following message

```console
$ git clone https://github.com/OU-CS3560/awesome-respository.git
Cloning into 'awesome-respository'...
Username for 'https://github.com': krerkkiat
Password for 'https://krerkkiat@github.com':
remote: The `OU-CS3560' organization has enabled or enforced SAML SSO. To access
remote: this repository, visit https://github.com/enterprises/ohiouniversity/sso?authorization_request=CjJ7Eqm5UiLaptX-IhbOpij5S7JaqSU8Tkbek-r09yTnvBn3WSg6eR4_VTfOmFvwu9OVEa3z7mVLAccRhlOD5CuFrQRsjctrX8gpmkHq0ipxP_5HbZxFR5VF
remote: and try your request again.
fatal: unable to access 'https://github.com/OU-CS3560/awesome-respository.git/': The requested URL returned error: 403
```

From the error message, you can visit the link to quickly authorize your token. See the "SAML SSO Error" section in "Appendix B - Common Errors" for more detail.

### Authentication failed with git clone when using password

If you get the following message

```console
$ git clone https://github.com/OU-CS3560/awesome-respository.git
Cloning into 'awesome-respository'...
Username for 'https://github.com': krerkkiat
Password for 'https://krerkkiat@github.com':
remote: Support for password authentication was removed on August 13, 2021.
remote: Please see https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls for information on currently recommended modes of authentication.
fatal: Authentication failed for 'https://github.com/OU-CS3560/examples.git/'
```

Please read the message in the error message. You will notice that GitHub does not allow password to be used and a personal access token
is used instead.

Since our OU-CS3560 organization is using SAML SSO, you will also need to authorize the token. Please read the following three items
in the reading assignment

- About authentication with SAML single sign-on
- Authorizing a personal access token for use with SAML single sign-on
- Authorizing an SSH key for use with SAML single sign-on

### Git does not ask for a password anymore, so I cannot enter my token

This problem usually occur when password was used instead of a personal access token, but now Git remember the password and
does not ask for it again, so you cannot tell git to use your token instead.

Solution to this is to make git forget your password. The detail of this depends on your operating system

- For Windows, Search for "Credential Manager" in the startup menu. Go to Windows Credentials. Find entry for github.com and edit or remove them (see [here](https://web.archive.org/web/20210803204901/https://cmatskas.com/how-to-update-your-git-credentials-on-windows/) for more detail instructions)
- For MacOS, open "Keychain Access" by searching for it in Spotlight. Then search for github.com entry. Edit or remove the entry (see [here](https://docs.github.com/en/github/using-git/updating-credentials-from-the-macos-keychain) for more detail). You may have to reboot your Mac to be able to edit or remove the entry.

### "Command not found" Error

You want to familarize yourself with the error message from the shell when the command does not exist

For example, in a Bash shell, you will get the following message

```console
$ git
bash: git: command not found
```

PowerShell will produce a longer message

```console
PS C:\Users\kchusap> git
whee: The term 'git' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
```

Most of the time, the solution is to install the program. If you just perform the installation, make sure
it was completed successfully.

### Permission denied when running my program

You may be trying to run a file that is not an [executable file](https://en.wikipedia.org/wiki/Executable).

For example, the following output is when you are trying to run `README.md` file.

```console
$ ./README.md
bash: ./README.md: Permission denied
```

In this case, the `README.md` is a text file. It is not a program that can be run. `file` command is a useful
command to check what type of the content of file is. Running `file` on `README.md` will give the following
output

```console
$ file README.md
README.md: ASCII text, with very long lines
```

For program created by the compiler, you will get output like the following

```console
$ file awesome-program
awesome-program: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=0154720979a5199273e00fc56b4ac309a9175fc6, for GNU/Linux 3.2.0, not stripped
```

The key information is the `ELF` which is a [file format](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) in Linux for
executable/program. This is the similar to the `.exe` on Windows.

### "g++ \*.cpp" does not work

This assignment is designed so that `g++ *.cpp` will not work. Instead, please use commands that compile
each file individually then later link object files together to create an executable file.
If you need an example, please read an article by Faisal Qureshi in the reading assignment.

## Appendix C - Rubric

Total: 100 points

### Problem - sandstorm (25 points)

### Problem - odd-or-even-makefile (25 points)

### Problem - limited-resources (25 points)

### Problem - simple-project (25 points)
