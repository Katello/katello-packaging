%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name qpid_messaging
%global qpid_version 0.30

Summary:       Ruby bindings for the Qpid messaging framework
Name:          %{?scl_prefix}rubygem-%{gem_name}
Version:       %{qpid_version}.0
Release:       1%{?dist}
License:       ASL 2.0

URL:           http://qpid.apache.org
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} > 18
Requires:       %{?scl_prefix_ruby}ruby(release)
%else
Requires: %{?scl_prefix_ruby}ruby(abi) = 1.9.1
%endif

Requires:      %{?scl_prefix_ruby}ruby(rubygems)

%if 0%{?fedora} > 18
BuildRequires:       %{?scl_prefix_ruby}ruby(release)
%else
BuildRequires: %{?scl_prefix_ruby}ruby(abi) = 1.9.1
%endif
BuildRequires: %{?scl_prefix_ruby}rubygems

BuildRequires: %{?scl_prefix_ruby}ruby-devel
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: qpid-cpp-client-devel = %{qpid_version}

Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}}

%description
Qpid is an enterprise messaging framework. This package provides Ruby
language bindings based on that framework.

%package doc
Summary:   Documentation for %{?scl_prefix}%{name}
Requires:  %{?scl_prefix}%{name} = %{version}-%{release}
BuildArch: noarch
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}-doc}

%description doc
%{Summary}.

%files doc
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/ChangeLog
%{gem_instdir}/examples
%doc %{gem_instdir}/TODO

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0} --no-rdoc --no-ri
%{?scl:"}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/lib

rm -rf %{buildroot}%{gem_instdir}/ext

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%changelog
* Wed Jan 21 2015 Jason Montleon <jmontleo@redhat.com> 0.30.0-1
- update rubygem-qpid_messaging to MRG 3.1 (jmontleo@redhat.com)

* Fri Dec 05 2014 Jason Montleon <jmontleo@redhat.com> 0.22.0-1.1
- add correct source (jmontleo@redhat.com)

* Fri Dec 05 2014 Jason Montleon <jmontleo@redhat.com> 0.22.0-1
- new package built with tito

* Thu Aug 07 2014 Jason Montleon <jmontleo@redhat.com> 0.26.1-4
- don't package non-existent doc dir (jmontleo@redhat.com)

* Thu Aug 07 2014 Jason Montleon <jmontleo@redhat.com> 0.26.1-3
- packaging change (jmontleo@redhat.com)

* Thu Aug 07 2014 Jason Montleon <jmontleo@redhat.com> 0.26.1-2
- new package built with tito

* Tue Jul 15 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26.1-1
- Rebased on qpid_messaging 0.26.1.

* Fri Feb 21 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26.0-1
- Rebased on qpid_messaging 0.26.0.

* Fri Oct 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.2-1
- Rebased on qpid_messaging 0.24.2.
- Fixed ordering of caught exceptions from C++.

* Fri Oct 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.1-2
- Removed the ARM exclusion.

* Fri Oct 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.1-1
- Rebased on qpid_messaging 0.24.1.

* Tue Sep 24 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24.0-1
- Rebased on qpid_messaging 0.24.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-2
- Updated build to fix dependency issues on qpid-cpp.

* Tue Jun 18 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-1
- Rebased on qpid_messaging 0.22.

* Fri Mar  8 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20.2-1
- Rebased on qpid_messaging 0.20.2.
- Updated to use the newer rubygems-devel macros.

* Thu Feb  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-2
- bump qpid_version to 0.20 to match release

* Mon Jan 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20.0-1
- Rebased on qpid_messaging 0.20.0.

* Mon Jan  7 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.18.1-1.2
- Now installs the repackaged gem.

* Wed Dec 26 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18.1-1.1
- Removed Group field from the doc subpackage.
- Updated the specfile to match current Ruby packaging guidelines.

* Mon Sep 24 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18.1-1
- Rebased on qpid_messaging 0.18.1.
- Added the ChangeLog to the files in the -doc package.

* Mon Aug 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16.0-1.2
- Moved the gem install statement to the install section.

* Wed Aug  1 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16.0-1.1
- Added BR for ruby-devel.

* Thu Jul 19 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16.0-1
- Initial repackaging.
