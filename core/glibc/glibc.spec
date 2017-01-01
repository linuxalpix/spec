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
Source3: https://raw.githubusercontent.com/linuxalpix/sources/master/glibc/locale-gen
Source4: https://raw.githubusercontent.com/linuxalpix/sources/master/glibc/locale.gen.txt

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
             --prefix=%{_prefix}          \
             --libdir=%{_libdir} \
             --libexecdir=%{_libdir} \
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
strip $STRIP_BINARIES %{buildroot}/sbin/{ldconfig,sln} \
                      %{buildroot}%{_bindir}/{gencat,getconf,getent,iconv,locale} \
                      %{buildroot}%{_bindir}/{localedef,pcprofiledump,rpcgen,sprof} \
                      %{buildroot}%{_libdir}/getconf/* \
                      %{buildroot}%{_prefix}/{iconvconfig,nscd}
strip $STRIP_STATIC %{buildroot}%{_libdir}/*.a 
strip $STRIP_SHARED %{buildroot}%{_lib}/{libanl,libBrokenLocale,libcidn,libcrypt}-*.so \
                    %{buildroot}%{_lib}/libnss_{compat,dns,files,hesiod,nis,nisplus}-*.so \
                    %{buildroot}%{_lib}/{libdl,libm,libnsl,libresolv,librt,libutil}-*.so \
                    %{buildroot}%{_lib}/{libmemusage,libpcprofile,libSegFault}.so \
                    %{buildroot}%{_libdir}/{audit,gconv}/*.so \
                    %{buildroot}%{_lib}/libmvec-*.so

install -m644 %{_sourcedir}/locale.gen.txt  %{buildroot}%{_sysconfdir}/locale.gen
sed -e '1,3d' -e 's|/| |g' -e 's|\\| |g' -e 's|^|#|g' \
%{_sourcedir}/%{name}-%{version}/localedata/SUPPORTED >>  %{buildroot}%{_sysconfdir}/locale.gen

install -m755 %{_sourcedir}/locale-gen %{buildroot}%{_prefix}/bin

%files
%defattr(-,root,root)
%{buildroot}/*

%changelog
*   Sun Jan 1 2017 Egor Mikhailov <xeneloid@yandex.ru> 2.24-1
-   Strip binaries and libs + add locale gen

*   Sun Jan 1 2017 Egor Mikhailov <xeneloid@yandex.ru> 2.24-1
-   Initial package
