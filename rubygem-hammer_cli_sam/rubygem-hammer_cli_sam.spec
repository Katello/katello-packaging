%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%{!?_root_sysconfdir:%global _root_sysconfdir %{_sysconfdir}}

%global gem_name hammer_cli_sam
%global confdir hammer

Summary: SAM commands for Hammer
Name:    %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.1
Release: 1%{?dist}
Group:   Development/Languages
License: GPLv3
URL:     http://github.com/Katello/hammer-cli-sam
Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
%if 0%{?scl:1}
Obsoletes: rubygem-%{gem_name} < 1.0.1-2
%endif

Requires: %{?scl_prefix}ruby(abi)
Requires: %{?scl_prefix}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(hammer_cli_katello)

BuildRequires: %{?scl_prefix}ruby(rubygems)
BuildRequires: %{?scl_prefix}rubygems-devel

%description
Hammer-CLI-SAM is a Hammer module which provides connectivity to a SAM server.


%package doc
Summary:   Documentation for %{pkg_name}
Group:     Documentation
Requires:  %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T -n %{pkg_name}-%{version}
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} - << \EOF}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0}
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{_root_sysconfdir}/%{confdir}/cli.modules.d
install -m 755 .%{gem_instdir}/config/sam.yml %{buildroot}%{_root_sysconfdir}/%{confdir}/cli.modules.d/sam.yml
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%doc %{gem_instdir}/LICENSE
%config(noreplace) %{_root_sysconfdir}/%{confdir}/cli.modules.d/sam.yml
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/config
%doc %{gem_instdir}/README.md

%changelog
* Mon Aug 03 2015 Adam Price <komidore64@gmail.com> 1.0.1-1
- Move config file into config directory and deploy via gem.
  (ericdhelms@gmail.com)

* Wed Mar 04 2015 Adam Price <komidore64@gmail.com> 1.0.0-1
- new package built with tito

* Wed Dec 03 2014 Mike McCune - 0.0.1-1
- Initial package
