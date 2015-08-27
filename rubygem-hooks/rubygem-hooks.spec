%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name hooks

%define rubyabi 1.9.1

%if 0%{?fedora}
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
%endif

Name:           %{?scl_prefix}rubygem-%{gem_name}
Summary:        Generic hooks with callbacks for Ruby.
Group:          Applications/System
License:        MIT
Version:        0.2.2
Release:        7%{?dist}
URL:            http://nicksda.apotomo.de/tag/hooks
Source0: 	http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} > 18
Requires:       %{?scl_prefix_ruby}ruby(release)
%else
Requires:       %{?scl_prefix_ruby}ruby(abi) = %{rubyabi}
%endif
Requires:       %{?scl_prefix_ruby}ruby(rubygems) 

BuildRequires:  %{?scl_prefix_ruby}rubygems
BuildRequires:  %{?scl_prefix_ruby}rubygems-devel 

BuildArch:      noarch
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}}

%description
Declaratively define hooks, add callbacks and run them with the options you like.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}
%{?scl:"}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%{gem_instdir}/CHANGES.textile
%{gem_instdir}/Gemfile
%{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/hooks.gemspec
%exclude %{gem_instdir}/test
%exclude %{gem_cache}
%{gem_spec}


%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}

%files doc
%doc %{gem_docdir}

%changelog
* Thu Aug 27 2015 Eric D. Helms <ericdhelms@gmail.com> 0.2.2-7
- new package built with tito

