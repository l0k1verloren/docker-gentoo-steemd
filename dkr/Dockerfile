FROM gentoo/stage3-amd64

RUN cd /usr ; wget -c http://distfiles.gentoo.org/snapshots/portage-latest.tar.xz;\
    tar xvf portage-latest.tar.xz; rm portage-latest.tar.xz

RUN emerge --sync

# Set compiler optimisation for minimising code size
RUN sed -i 's/CFLAGS=\"-O2 -pipe\"/CFLAGS=\"-Os -pipe\"/g' /etc/portage/make.conf

# Enable the elliptic curve functions in openssl
RUN sed -i 's/bindist/-bindist context python tools/g' /etc/portage/make.conf

RUN emerge --update world

RUN emerge -v openssl:0 openssh

RUN emerge dev-vcs/git 
RUN emerge autoconf 
RUN emerge cmake 
RUN emerge libtool 
RUN emerge make 
RUN emerge pkg-config 
RUN emerge app-arch/bzip2
RUN emerge doxygen 
RUN emerge ncurses 
RUN emerge readline 
RUN emerge perl 
RUN emerge python

# Build Boost from version 1.57.0 snapshot
RUN export CXXFLAGS='-Os -pipe'; cd /root; BOOST_ROOT=/usr/local; \
    URL='https://sourceforge.net/projects/boost/files/boost/1.60.0/boost_1_60_0.tar.bz2/download'; \
    wget -c "$URL" -O boost_1_60_0.tar.bz2; \
    tar xjf boost_1_60_0.tar.bz2; \
    cd boost_1_60_0; \
    ./bootstrap.sh "--prefix=$BOOST_ROOT"; \
    ./b2 -j$(nproc) install; \
    cd ..\
    rm -rf boost* \
    exit 0

RUN cd /root; git clone https://github.com/steemit/steem -b v0.19.0
RUN cd /root/steem; git submodule update --init --recursive
RUN cd /root/steem; mkdir build
RUN cd /root/steem/build; export CXXFLAGS='-Os -pipe'; cmake -DCMAKE_BUILD_TYPE=Release ..
RUN cd /root/steem/build; make -j$(nproc) steemd
RUN cd /root/steem/build; make -j$(nproc) cli_wallet
RUN cd /root/steem/build; make install

RUN emerge zsh

VOLUME /work
WORKDIR /work                  

#CMD tail -f /dev/null #
CMD steemd 1>>/work/steemd.log 2>>/work/steemd.log
