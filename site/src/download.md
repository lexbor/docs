[name]: Download
[title]: Download
[theme]: document.html

## Binary packages

Binaries are available for:

* CentOS 6, 7, 8
* Debian 8, 9, 10
* Fedora 28, 29, 30, 31, 32, 33, 34
* RHEL 6, 7
* Ubuntu 14.04, 16.04, 18.04, 18.10, 19.04, 19.10, 20.04, 20.10, 21.04

### CentOS

1. To configure Lexbor repository, create the following file named `/etc/yum.repos.d/lexbor.repo`:

 ```conf
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/centos/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install Lexbor base package and additional packages you would like to use.

 ```sh
 yum install liblexbor
 yum install liblexbor-devel
 ```

### Debian

1. Download Lexbor [signing key](https://lexbor.com/keys/lexbor_signing.key) used for our repositories and packages and add it to apt’s keyring:

 ```sh
 curl -O https://lexbor.com/keys/lexbor_signing.key
 apt-key add lexbor_signing.key
 ```

2. To configure Lexbor repository, create the following file named `/etc/apt/sources.list.d/lexbor.list`:

 Debian 8:

 ```conf
 deb https://packages.lexbor.com/debian/ jessie liblexbor
 deb-src https://packages.lexbor.com/debian/ jessie liblexbor
 ```

 Debian 9:

 ```conf
 deb https://packages.lexbor.com/debian/ stretch liblexbor
 deb-src https://packages.lexbor.com/debian/ stretch liblexbor
 ```
 
 Debian 10:
 
 ```conf
 deb https://packages.lexbor.com/debian/ buster liblexbor
 deb-src https://packages.lexbor.com/debian/ buster liblexbor
 ```

3. Install Lexbor base package and additional packages you would like to use.

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```

### Fedora

1. To configure Lexbor repository, create the following file named `/etc/yum.repos.d/lexbor.repo`:

 ```conf
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/fedora/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install Lexbor base package and additional packages you would like to use.

 ```sh
 yum install liblexbor
 yum install liblexbor-dev
 ```

### RHEL

1. To configure Lexbor repository, create the following file named `/etc/yum.repos.d/lexbor.repo`:

 ```conf
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/rhel/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install Lexbor base package and additional packages you would like to use.

 ```sh
 yum install liblexbor
 yum install liblexbor-dev
 ```

### Ubuntu

1. Download Lexbor [signing key](https://lexbor.com/keys/lexbor_signing.key) used for our repositories and packages and add it to apt’s keyring:

 ```sh
 curl -O https://lexbor.com/keys/lexbor_signing.key
 apt-key add lexbor_signing.key
 ```

2. To configure Lexbor repository, create the following file named `/etc/apt/sources.list.d/lexbor.list`:

 Ubuntu 14.04:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ trusty liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ trusty liblexbor
 ```

 Ubuntu 16.04:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ xenial liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ xenial liblexbor
 ```

 Ubuntu 18.04:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ bionic liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ bionic liblexbor
 ```

 Ubuntu 18.10:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ cosmic liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ cosmic liblexbor
 ```

 Ubuntu 19.04:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ disco liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ disco liblexbor
 ```

 Ubuntu 19.10:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ eoan liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ eoan liblexbor
 ```

 Ubuntu 20.04:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ focal liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ focal liblexbor
 ```

 Ubuntu 20.10:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ groovy liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ groovy liblexbor
 ```

 Ubuntu 21.04:

 ```conf
 deb https://packages.lexbor.com/ubuntu/ hirsute liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ hirsute liblexbor
 ```

3. Install Lexbor base package and additional packages you would like to use.

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```

## macOS

### Homebrew

To install `lexbor` on macOS from Homebrew:

```sh
brew install lexbor
```

### MacPorts

To install `lexbor` on macOS from MacPorts:

```sh
sudo port install lexbor
```
