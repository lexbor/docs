# Download

## Binary packages

The `lexbor` binaries are available for:

* [CentOS](#centos) 7

* [Debian](#debian) 11, 12

* [Fedora](#fedora) 39, 40, 41

* [RHEL](#rhel) 8, 9

* [Ubuntu](#ubuntu) 20.04, 22.04, 24.04

* [macOS](#macos)

**Note:** Older distribution versions that have reached end-of-life are no longer listed. If you need packages for an older version, check the repository at `packages.lexbor.com` directly.


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
   `/etc/apt/sources.list.d/lexbor.list`. For Debian 12:

 ```ini
deb-src [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/debian/ bookworm liblexbor
deb [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/debian/ bookworm liblexbor
 ```

 Supported distros also include `bullseye` (11).

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
 dnf install liblexbor
 dnf install liblexbor-devel
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
 yum install liblexbor-devel
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
   `/etc/apt/sources.list.d/lexbor.list`. For Ubuntu 22.04:

 ```ini
deb-src [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/ubuntu/ jammy liblexbor
deb [signed-by=/etc/apt/keyrings/lexbor.gpg] https://packages.lexbor.com/ubuntu/ jammy liblexbor
 ```

 Supported distros also include `noble` (24.04) and `focal` (20.04).

3. Install the core `lexbor` package and any additional packages you need:

 ```sh
 apt update
 apt install liblexbor
 apt install liblexbor-dev
 ```


### macOS

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
