# explicitly define, as we build on top of an scl, not inside with scl_package
%{?scl:%global scl_prefix %{scl}-}
%global scl_ruby_bin /usr/bin/%{?scl:%{scl_prefix}}ruby
%global scl_rake /usr/bin/%{?scl:%{scl_prefix}}rake

Name:           katello-utils
Version:        2.4.0
Release:        3%{?dist}
Summary:        Additional tools for Katello

Group:          Applications/Internet
License:        GPLv2
URL:            http://www.katello.org
Source0:        https://codeload.github.com/Katello/%{name}/tar.gz/%{version}

BuildArch: noarch

Requires:       coreutils
Requires:       unzip
%if 0%{?fedora} > 18
Requires: %{?scl_prefix_ruby}ruby(release)
%else
Requires: %{?scl_prefix_ruby}ruby(abi) = 1.9.1
%endif
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(katello)
Requires: %{?scl_prefix_ruby}rubygem(json)
Requires: %{?scl_prefix_ruby}rubygem(activesupport)
Requires: %{?scl_prefix}rubygem(oauth)
Requires: %{?scl_prefix}rubygem(rest-client)
Requires: %{?scl_prefix}rubygem(runcible)
Requires: %{?scl_prefix}rubygem(fast_gettext)

BuildRequires:  /usr/bin/pod2man
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  gettext translate-toolkit
BuildRequires:  %{?scl_prefix_ruby}rubygems-devel
BuildRequires:  %{?scl_prefix_ruby}rubygems
BuildRequires:  tfm

%description
Provides katello-disconnected script along with few other tools for Katello
cloud lifecycle management application.

%prep
%setup -q

%build
# replace shebangs for SCL
%if "%{scl}"
    sed -i '1s|/usr/bin/ruby|%{scl_ruby_bin}|' bin/*
%endif

%if "%{scl}"
# check syntax of main configure script and libs
    %{scl_ruby_bin} -c bin/katello-disconnected
%endif

# pack gettext i18n PO files into MO files
make -C po check all-mo %{?_smp_mflags}

# build katello-configure man page
pushd man
    sed -e 's/THE_VERSION/%{version}/g' katello-disconnected.pod |\
    /usr/bin/pod2man --name=katello-disconnected -c "Katello Reference" --section=1 --release=%{version} - katello-disconnected.man1
popd


%install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 bin/katello-disconnected %{buildroot}%{_bindir}
install -m 0755 bin/katello-cat-manifest %{buildroot}%{_bindir}

install -d -m 0755 %{buildroot}%{_datadir}/katello-disconnected/lib
install -m 0644 lib/* %{buildroot}%{_datadir}/katello-disconnected/lib

install -d -m 0755 %{buildroot}%{_datadir}/katello-disconnected/locale
pushd po
for MOFILE in $(find . -name "*.mo"); do
    DIR=$(dirname "$MOFILE")
    install -d -m 0755 %{buildroot}%{_datadir}/katello-disconnected/locale/$DIR/LC_MESSAGES
    install -m 0644 $DIR/*.mo %{buildroot}%{_datadir}/katello-disconnected/locale/$DIR/LC_MESSAGES
done
popd

install -d -m 0755 %{buildroot}%{_mandir}/man1
install -m 0644 man/katello-disconnected.man1 %{buildroot}%{_mandir}/man1/katello-disconnected.1


%files
%{_bindir}/katello-disconnected
%{_bindir}/katello-cat-manifest
%{_datadir}/katello-disconnected/lib
%{_datadir}/katello-disconnected/locale
%{_mandir}/man1/katello-disconnected.1*


%changelog
* Tue Sep 01 2015 Eric D. Helms <ericdhelms@gmail.com> 2.4.0-3
- Fixing erroneous requires within katello-utils (ericdhelms@gmail.com)

* Fri Aug 28 2015 Eric D. Helms <ericdhelms@gmail.com> 2.4.0-2
- Update katello-utils to the tfm SCL (ericdhelms@gmail.com)

* Wed Jul 29 2015 Eric D. Helms <ericdhelms@gmail.com> 2.4.0-1
- new package built with tito

* Tue Jul 07 2015 Stephen Benjamin <stbenjam@redhat.com> 2.4.0-1
- Bump to 2.4.0

* Tue Jul 07 2015 Stephen Benjamin <stbenjam@redhat.com> 2.3.0-1
- Update for Katello 2.3.0
- Fixes #10706: Fix data range export (ericdhelms@gmail.com)

* Fri Dec 19 2014 David Davis <daviddavis@redhat.com> 2.2.0-1
- 

* Fri Sep 12 2014 Justin Sherrill <jsherril@redhat.com> 2.1.0-1
- bumping version to 2.1 (jsherril@redhat.com)

* Fri Sep 12 2014 Justin Sherrill <jsherril@redhat.com> 2.0.0-1
- fixes #7252, BZ1040112 - adding support for a proxy (mmccune@redhat.com)
- fixes #6921,BZ102410 - ensure only root can execute (mmccune@redhat.com)
- fixes #6265 - better error handing for missing listing files on the CDN
  (mmccune@redhat.com)
- fixes 5629 - adding proper BuildRequires (mmccune@redhat.com)
- fixes 5624 - adding a publish command (mmccune@redhat.com)

* Wed Apr 09 2014 Mike McCune <mmccune@redhat.com> 1.5.2-1
- Merge pull request #28 from ehelms/fixes-5067 (ericdhelms@gmail.com)
- Fixes #5067: Updates paths to Katello gem BZ1083201 (ericdhelms@gmail.com)
- fix katello-utils rpm dependencies (jmontleo@redhat.com)
- Merge pull request #18 from mccun934/man-reader-path-fix (mmccune@gmail.com)
- 1013755 - filter out the endless loop of Packages/Packages/Packages
  (mmccune@redhat.com)
- 1013755 - make sure we actually export and remove unused var
  (mmccune@redhat.com)
- fixing path to manifest_reader.rb to loc from katello-utils
  (mmccune@redhat.com)

* Fri Oct 11 2013 Partha Aji <paji@redhat.com> 1.5.1-1
- Bumping package versions for 1.5 (paji@redhat.com)

* Fri Oct 11 2013 Partha Aji <paji@redhat.com> 1.4.4-1
- minor syntax cleanup with some review from daviddavis (mmccune@redhat.com)
- fixing style (mmccune@redhat.com)
- go back to original interp (mmccune@redhat.com)
- switch to http only and properly archive up the puppet-forge
  (mmccune@redhat.com)
- remove ISO distributor that we don't need (mmccune@redhat.com)
- adding start/end date support for exports (mmccune@redhat.com)
- go back to original shell (mmccune@redhat.com)
- puppet support for katello-disconnected and better syncing status
  (mmccune@redhat.com)
- switch to feed vs feed_url (mmccune@redhat.com)
- update katello-disconnected to use runcible 1.0 style objects
  (mmccune@redhat.com)
- update katello-disconnected to use runcible 1.0 style objects
  (mmccune@redhat.com)

* Wed Jul 31 2013 Partha Aji <paji@redhat.com> 1.4.3-1
- fix swapped variables so we properly send the key and secret
  (mmccune@redhat.com)
- 2699 - handle error conditions better so disconnected can continue
  (mmccune@redhat.com)
- adding method parens to follow coding convention (mmccune@redhat.com)
- first stab at exporting pulp content to a directory (mmccune@redhat.com)

* Sat Apr 27 2013 Justin Sherrill <jsherril@redhat.com> 1.4.2-1
- Build with new repo structure  (jsherril@redhat.com)

* Fri Apr 12 2013 Justin Sherrill <jsherril@redhat.com> 1.4.1-1
- version bump to 1.4 (jsherril@redhat.com)

* Fri Apr 12 2013 Justin Sherrill <jsherril@redhat.com> 1.3.2-1
- i18n - fixing missing build require (lzap+git@redhat.com)
- i18n - enabling katello domain and improving check (lzap+git@redhat.com)
- removing resource_permissions require and minor fix (lzap+git@redhat.com)
- disconnected - adding support for ruby scl (lzap+git@redhat.com)
- disconnected - adding i18n and refactoring (lzap+git@redhat.com)
- diconnected - pulp v2 initial support (lzap+git@redhat.com)

* Tue Jan 08 2013 Lukas Zapletal <lzap+git@redhat.com> 1.3.1-1
- use dependecies according the code in ./bin/katello-disconnected
- Bumping package versions for 1.3.

* Tue Oct 23 2012 Lukas Zapletal <lzap+git@redhat.com> 1.2.1-1
- Bumping package versions for 1.1.

* Thu Sep 27 2012 Lukas Zapletal <lzap+git@redhat.com> 1.1.2-1
- katello-utils - correcting build requires
- adding two requires and comps for katello-utils

* Wed Sep 26 2012 Lukas Zapletal <lzap+git@redhat.com> 1.1.1-1
- new package built with tito

* Wed Sep 26 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.1.0-1
- Initial version
