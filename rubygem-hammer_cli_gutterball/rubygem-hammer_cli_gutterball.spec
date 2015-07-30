%global gem_name hammer_cli_gutterball
%global confdir hammer

%if 0%{?rhel} < 7
%global gem_dir /usr/lib/ruby/gems/1.8
%endif

Summary: Gutterball commands for Hammer
Name: rubygem-%{gem_name}
Version: 1.0.1
Release: 2%{?dist}
Group: Development/Languages
License: GPLv3
URL: http://github.com/Katello/hammer-cli-gutterball
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?rhel} == 6
Requires: ruby(abi)
%else
Requires: ruby(release)
%endif

Requires: ruby(rubygems)
Requires: rubygem(hammer_cli) >= 0.1.1
BuildRequires: ruby(rubygems)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Hammer-CLI-Gutterball is a Hammer module which provides additional functionality for use with the foreman_gutterball plugin.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0}

%install
mkdir -p %{buildroot}%{_sysconfdir}/%{confdir}/cli.modules.d
install -m 755 .%{gem_instdir}/config/gutterball.yml %{buildroot}%{_sysconfdir}/%{confdir}/cli.modules.d/gutterball.yml

mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_instdir}/
%exclude %{gem_dir}/cache/%{gem_name}-%{version}.gem
%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%config(noreplace) %{_sysconfdir}/%{confdir}/cli.modules.d/gutterball.yml

%files doc
%doc %{gem_dir}/doc/%{gem_name}-%{version}
%doc %{gem_instdir}/config

%changelog
* Wed Jul 29 2015 Eric D. Helms <ericdhelms@gmail.com> 1.0.1-2
- new package built with tito

* Tue Mar 03 2015 Adam Price <komidore64@gmail.com> 1.0.0-1
- new package built with tito

