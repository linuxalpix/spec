Name:    glibc
Version: 2.24
Release: 1
Group: Base/System
Summary: C library
URL:     http://www.gnu.org/software/libc
License: GPL
Packager: Xeneloid <xeneloid@yandex.ru>
Vendor: ProtonOS

BuildArch: x86_64
BuildRequires: gcc

Requires: linux-api-headers
Requires: tzdata

Source0: http://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
Source1: https://raw.githubusercontent.com/linuxalpix/sources/master/glibc/ld.so.conf
Source2: https://raw.githubusercontent.com/linuxalpix/sources/master/glibc/nsswitch.conf

%description
This library provides the basic routines for allocating memory,
searching directories, opening and closing files, reading and
writing files, string handling, pattern matching, arithmetic,
and so on.

%prep
%setup -q
mkdir -v %{_builddir}/build

%build
cd       %{_builddir}/build
../%{name}-%{version}/configure \
			 --prefix=/usr          \
             --libdir=/usr/lib \
             --libexecdir=/usr/lib \
             --with-headers=/usr/include \
             --enable-kernel=2.6.32 \
             --enable-obsolete-rpc \
             --disable-silent-rules \
             --enable-add-ons \
             --enable-static-nss \
             --disable-profile \
             --disable-werror \
             --without-gd \
             --enable-obsolete-rpc \
             --enable-stackguard-randomization \
             --enable-lock-elision \
             --enable-bind-now
make

%install
install -dm755 %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/ld.so.conf
make root_install=%{buildroot} install
rm %{buildroot}%{_sysconfdir}/ld.so.conf
cp -v ../%{name}-%{version}/nscd/nscd.conf %{buildroot}%{_sysconfdir}/nscd.conf
mkdir -pv %{buildroot}%{_localstatedir}/cache/nscd
install -v -Dm644 ../%{name}-%{version}/nscd/nscd.tmpfiles %{buildroot}%{_libdir}/tmpfiles.d/nscd.conf
install -v -Dm644 ../%{name}-%{version}/nscd/nscd.service %{buildroot}%{_lib}/systemd/system/nscd.service
install -m 0644 %{_sourcedir}/{nsswitch.conf,ld.so.conf} %{buildroot}%{_sysconfdir}
mkdir -pv %{buildroot}%{_sysconfdir}/ld.so.conf.d
mkdir -pv %{buildroot}%{_libdir}/locale
make root_install=%{buildroot} localedata/install-locales

%files
%defattr(-,root,root)
%{buildroot}/*

%changelog
*   Sun Jan 1 2017 Egor Mikhailov <xeneloid@yandex.ru> 2.24-1
-   Initial package
