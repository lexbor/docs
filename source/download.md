# Download

## Binary packages

The `lexbor` binaries are available for:

* [CentOS](#centos) 6, 7, 8

* [Debian](#debian) 8, 9, 10, 11

* [Fedora](#fedora) 28, 29, 30, 31, 32, 33, 34, 36, 37

* [RHEL](#rhel) 7, 8

* [Ubuntu](#ubuntu) 14.04, 16.04, 18.04, 18.10, 19.04, 19.10, 20.04, 20.10,
  21.04, 22.04

* [macOS](#macos)

### CentOS

1. To configure the `lexbor` repository, create the following file named
   `/etc/yum.repos.d/lexbor.repo`:

 ```ini
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/centos/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install the core `lexbor` package and extra packages you want to use:

 ```sh
 yum install liblexbor
 yum install liblexbor-devel
 ```

### Debian

1. Download the `lexbor` [signing
   key](https://lexbor.com/keys/lexbor_signing.key) used for our repositories
   and packages and add it to `apt`’s keyring:

 ```sh
 curl -O https://lexbor.com/keys/lexbor_signing.key
 apt-key add lexbor_signing.key
 ```

2. To configure the `lexbor` repository, create the following file named
   `/etc/apt/sources.list.d/lexbor.list`.  For Debian 11:

 ```ini
 deb https://packages.lexbor.com/debian/ bullseye liblexbor
 deb-src https://packages.lexbor.com/debian/ bullseye liblexbor
 ```

 Other supported distros are `buster` (10), `stretch` (9), and `jessie` (8).

3. Install the core `lexbor` package and extra packages you want to use:

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```

### Fedora

1. To configure the `lexbor` repository, create the following file named
   `/etc/yum.repos.d/lexbor.repo`:

 ```ini
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/fedora/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install the core `lexbor` package and extra packages you want to use:

 ```sh
 yum install liblexbor
 yum install liblexbor-dev
 ```

### RHEL

1. To configure the `lexbor` repository, create the following file named
   `/etc/yum.repos.d/lexbor.repo`:

 ```ini
 [lexbor]
 name=lexbor repo
 baseurl=https://packages.lexbor.com/rhel/$releasever/$basearch/
 gpgcheck=0
 enabled=1
 ```

2. Install the core `lexbor` package and extra packages you want to use:

 ```sh
 yum install liblexbor
 yum install liblexbor-dev
 ```

### Ubuntu

1. Download the `lexbor` [signing
   key](https://lexbor.com/keys/lexbor_signing.key) used for our repositories
   and packages and add it to `apt`’s keyring:

 ```sh
 curl -O https://lexbor.com/keys/lexbor_signing.key
 apt-key add lexbor_signing.key
 ```

2. To configure the `lexbor` repository, create the following file named
   `/etc/apt/sources.list.d/lexbor.list`.  For Ubuntu 22.04:

 ```ini
 deb https://packages.lexbor.com/ubuntu/ jammy liblexbor
 deb-src https://packages.lexbor.com/ubuntu/ jammy liblexbor
 ```

 Other supported distros are `hirsute` (21.04), `groovy` (20.10), `focal`
 (20.04), `eoan` (19.10), `disco` (19.04), `cosmic` (18.10), `bionic` (18.04),
 `xenial` (16.04), and `trusty` (14.04).

3. Install the core `lexbor` package and extra packages you want to use:

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```

## macOS

### Homebrew

To install `lexbor` from [Homebrew](https://brew.sh):

```sh
brew install lexbor
```

### MacPorts

To install `lexbor` from [MacPorts](https://www.macports.org):

```sh
sudo port install lexbor
```
