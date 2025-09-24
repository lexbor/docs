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

2. Install the core `lexbor` package and any additional packages you need:

 ```sh
 yum install liblexbor
 yum install liblexbor-devel
 ```


### Debian

1. Download the `lexbor` [signing
   key](https://lexbor.com/keys/lexbor_signing.key) used for our repositories
   and add it to `apt`’s keyring:

 ```sh
sudo mkdir -p /etc/apt/keyrings
curl https://lexbor.com/keys/lexbor_signing.key | \
    sudo gpg --dearmor --output /etc/apt/keyrings/lexbor.gpg
 ```

2. To configure the `lexbor` repository, create the following file named
   `/etc/apt/sources.list.d/lexbor.list`. For Debian 11:

 ```ini
deb-src [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/debian/ bullseye liblexbor
deb [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/debian/ bullseye liblexbor
 ```

 Supported distros also include `buster` (10), `stretch` (9), and `jessie` (8).

3. Install the core `lexbor` package and any additional packages you need:

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

2. Install the core `lexbor` package and any additional packages you need:

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

2. Install the core `lexbor` package and any additional packages you need:

 ```sh
 yum install liblexbor
 yum install liblexbor-dev
 ```


### Ubuntu

1. Download the `lexbor` [signing
   key](https://lexbor.com/keys/lexbor_signing.key) used for our repositories
   and add it to `apt`’s keyring:

 ```sh
sudo mkdir -p /etc/apt/keyrings
curl https://lexbor.com/keys/lexbor_signing.key | \
    sudo gpg --dearmor --output /etc/apt/keyrings/lexbor.gpg
 ```

2. To configure the `lexbor` repository, create the following file named
   `/etc/apt/sources.list.d/lexbor.list`. For Ubuntu 20.04:

 ```ini
deb-src [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/ubuntu/ focal liblexbor
deb [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/ubuntu/ focal liblexbor
 ```

 Supported distros also include `hirsute` (21.04), `groovy` (20.10), `focal`
 (20.04), `eoan` (19.10), `disco` (19.04), `cosmic` (18.10), `bionic` (18.04),
 `xenial` (16.04), and `trusty` (14.04).

3. Install the core `lexbor` package and any additional packages you need:

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```


## macOS

### Homebrew

To install `lexbor` using [Homebrew](https://brew.sh):

```sh
brew install lexbor
```


### MacPorts

To install `lexbor` using [MacPorts](https://www.macports.org):

```sh
sudo port install lexbor
```
