Name:           gongxincoin
Version:        0.5.0
Release:        1%{dist}
Summary:        Gongxincoin Wallet
Group:          Applications/Internet
Vendor:         Gongxincoin
License:        GPLv3
URL:            http://www.gongxincoin.com
Source0:        %{name}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  autoconf automake libtool gcc-c++ openssl-devel >= 1:1.0.2d libdb4-devel libdb4-cxx-devel miniupnpc-devel boost-devel boost-static
Requires:       pwgen openssl >= 1:1.0.2d libdb4 libdb4-cxx miniupnpc logrotate

%description
Gongxincoin Wallet

%prep
%setup -q -n gongxincoin

%build
./autogen.sh
./configure
make

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT/etc/gongxincoin $RPM_BUILD_ROOT/etc/ssl/gxc $RPM_BUILD_ROOT/var/lib/gxc/.gongxincoin $RPM_BUILD_ROOT/usr/lib/systemd/system $RPM_BUILD_ROOT/etc/logrotate.d
%{__install} -m 755 bin/* $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 755 src/gongxincoind $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 755 src/gongxincoin-cli $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 600 contrib/build.el7/gongxincoin.conf $RPM_BUILD_ROOT/var/lib/gxc/.gongxincoin
%{__install} -m 644 contrib/build.el7/gongxincoind.service $RPM_BUILD_ROOT/usr/lib/systemd/system
%{__install} -m 644 contrib/build.el7/gongxincoind.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/gongxincoind

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pretrans
getent passwd gxc >/dev/null && { [ -f /usr/bin/gongxincoind ] || { echo "Looks like user 'gxc' already exists and have to be deleted before continue."; exit 1; }; } || useradd -r -M -d /var/lib/gxc -s /bin/false gxc

%post
[ $1 == 1 ] && {
  sed -i -e "s/\(^rpcpassword\)\(.*\)/rpcpassword=$(pwgen 64 1)/" /var/lib/gxc/.gongxincoin/gongxincoin.conf
  openssl req -nodes -x509 -newkey rsa:4096 -keyout /etc/ssl/gxc/gongxincoin.key -out /etc/ssl/gxc/gongxincoin.crt -days 3560 -subj /C=US/ST=Oregon/L=Portland/O=IT/CN=gongxincoin.gxc
  ln -sf /var/lib/gxc/.gongxincoin/gongxincoin.conf /etc/gongxincoin/gongxincoin.conf
  ln -sf /etc/ssl/gxc /etc/gongxincoin/certs
  chown gxc.gxc /etc/ssl/gxc/gongxincoin.key /etc/ssl/gxc/gongxincoin.crt
  chmod 600 /etc/ssl/gxc/gongxincoin.key
} || exit 0

%posttrans
[ -f /var/lib/gxc/.gongxincoin/addr.dat ] && { cd /var/lib/gxc/.gongxincoin && rm -rf database addr.dat nameindex* blk* *.log .lock; }
sed -i -e 's|rpcallowip=\*|rpcallowip=0.0.0.0/0|' /var/lib/gxc/.gongxincoin/gongxincoin.conf
systemctl daemon-reload
systemctl status gongxincoind >/dev/null && systemctl restart gongxincoind || exit 0

%preun
[ $1 == 0 ] && {
  systemctl is-enabled gongxincoind >/dev/null && systemctl disable gongxincoind >/dev/null || true
  systemctl status gongxincoind >/dev/null && systemctl stop gongxincoind >/dev/null || true
  pkill -9 -u gxc > /dev/null 2>&1
  getent passwd gxc >/dev/null && userdel gxc >/dev/null 2>&1 || true
  rm -f /etc/ssl/gxc/gongxincoin.key /etc/ssl/gxc/gongxincoin.crt /etc/gongxincoin/gongxincoin.conf /etc/gongxincoin/certs
} || exit 0

%files
%doc COPYING
%attr(750,gxc,gxc) %dir /etc/gongxincoin
%attr(750,gxc,gxc) %dir /etc/ssl/gxc
%attr(700,gxc,gxc) %dir /var/lib/gxc
%attr(700,gxc,gxc) %dir /var/lib/gxc/.gongxincoin
%attr(600,gxc,gxc) %config(noreplace) /var/lib/gxc/.gongxincoin/gongxincoin.conf
%defattr(-,root,root)
%config(noreplace) /etc/logrotate.d/gongxincoind
%{_bindir}/*
/usr/lib/systemd/system/gongxincoind.service

%changelog
* Sun Aug 21 2016 Sergii Vakula <sv@gongxincoin.com> 0.5.0
- Rebase to the v0.5.0

* Tue Jun 21 2016 Sergii Vakula <sv@gongxincoin.com> 0.3.7
- Initial release
