%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%{!?_root_sysconfdir:%global _root_sysconfdir %{_sysconfdir}}

%global gem_name hammer_cli_gutterball
%global confdir hammer

Summary: Gutterball commands for Hammer
Name:    %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.1
Release: 5%{?dist}
Group:   Development/Languages
License: GPLv3
URL:     http://github.com/Katello/hammer-cli-gutterball
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
%if 0%{?scl:1}
Obsoletes: rubygem-%{gem_name} < 1.0.1-3
%endif
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}}

Requires:  %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(hammer_cli) >= 0.1.1

BuildRequires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel

%description
Hammer-CLI-Gutterball is a Hammer module which provides additional functionality for use with the foreman_gutterball plugin.

%package doc
Summary:   Documentation for %{pkg_name}
Group:     Documentation
Requires:  %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}-doc}

%description doc
Documentation for %{pkg_name}

%prep
%setup -q -c -T -n %{pkg_name}-%{version}
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} - << \EOF}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0}
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{_root_sysconfdir}/%{confdir}/cli.modules.d
install -m 755 .%{gem_instdir}/config/gutterball.yml %{buildroot}%{_root_sysconfdir}/%{confdir}/cli.modules.d/gutterball.yml

mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%doc %{gem_instdir}/LICENSE
%config(noreplace) %{_root_sysconfdir}/%{confdir}/cli.modules.d/gutterball.yml
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/config
%doc %{gem_instdir}/README.md

%changelog
* Wed Jan 06 2016 Eric D. Helms <ericdhelms@gmail.com> 1.0.1-5
- Build rubygem-hammer_cli_gutterball for RH22 SCL (ericdhelms@gmail.com)

* Fri Aug 28 2015 Eric D. Helms <ericdhelms@gmail.com> 1.0.1-4
- Update rubygem-hammer_cli_gutterball to tfm SCL (ericdhelms@gmail.com)

* Fri Jul 31 2015 Eric D. Helms <ericdhelms@gmail.com> 1.0.1-3
- Fixes #11259: Move hammer packages to SCL (ericdhelms@gmail.com)

* Wed Jul 29 2015 Eric D. Helms <ericdhelms@gmail.com> 1.0.1-2
- new package built with tito

* Tue Mar 03 2015 Adam Price <komidore64@gmail.com> 1.0.0-1
- new package built with tito

