[name]: Download
[title]: Download
[theme]: document.html

## Binary packages

Binaries are available for:

* [CentOS](#centos) 6, 7, 8

* [Debian](#debian) 8, 9, 10, 11

* [Fedora](#fedora) 28, 29, 30, 31, 32, 33, 34, 36, 37

* [RHEL](#rhel) 7, 8

* [Ubuntu](#ubuntu) 14.04, 16.04, 18.04, 18.10, 19.04, 19.10, 20.04, 20.10,
  21.04, 22.04

* [macOS](#macos)

### CentOS

1. To configure `lexbor` repository, create the following file named
   `/etc/yum.repos.d/lexbor.repo`:

 ```conf
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/centos/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install `lexbor` base package and additional packages you would like to use:

 ```sh
 yum install liblexbor
 yum install liblexbor-devel
 ```

### Debian

1. Download `lexbor` [signing key](https://lexbor.com/keys/lexbor_signing.key)
   used for our repositories and packages and add it to apt’s keyring:

 ```sh
 curl -O https://lexbor.com/keys/lexbor_signing.key
 apt-key add lexbor_signing.key
 ```

2. To configure `lexbor` repository, create the following file named
   `/etc/apt/sources.list.d/lexbor.list`.  For Debian 11:

 ```conf
 deb https://packages.lexbor.com/debian/ bullseye liblexbor
 deb-src https://packages.lexbor.com/debian/ bullseye liblexbor
 ```

 Other supported distro codenames are `buster`, `jessie`, and `stretch`.

3. Install `lexbor` base package and additional packages you would like to use:

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```

### Fedora

1. To configure `lexbor` repository, create the following file named
   `/etc/yum.repos.d/lexbor.repo`:

 ```conf
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/fedora/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install `lexbor` base package and additional packages you would like to use:

 ```sh
 yum install liblexbor
 yum install liblexbor-dev
 ```

### RHEL

1. To configure `lexbor` repository, create the following file named
   `/etc/yum.repos.d/lexbor.repo`:

 ```conf
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/rhel/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install `lexbor` base package and additional packages you would like to use:

 ```sh
 yum install liblexbor
 yum install liblexbor-dev
 ```

### Ubuntu

1. Download `lexbor` [signing key](https://lexbor.com/keys/lexbor_signing.key)
   used for our repositories and packages and add it to apt’s keyring:

 ```sh
 curl -O https://lexbor.com/keys/lexbor_signing.key
 apt-key add lexbor_signing.key
 ```

2. To configure `lexbor` repository, create the following file named
   `/etc/apt/sources.list.d/lexbor.list`.  For Ubuntu 22.04:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ jammy liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ jammy liblexbor
 ```

 Other supported distros are `bionic`, `cosmic`, `disco`, `eoan`,
 `focal`, `groovy`, `hirsute`, `trusty`,  and `xenial`.

3. Install `lexbor` base package and additional packages you would like to use:

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```

## macOS

### Homebrew

To install `lexbor` from Homebrew:

```sh
brew install lexbor
```

### MacPorts

To install `lexbor` from MacPorts:

```sh
sudo port install lexbor
```
