%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%define gem_name haml-rails

Summary: let your Gemfile do the configuring
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.4
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://github.com/indirect/haml-rails
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{?scl_prefix_ruby}ruby(abi) = 1.9.1
Requires: %{?scl_prefix_ruby}rubygems
Requires: %{?scl_prefix}rubygem(haml) >= 3.0
Requires: %{?scl_prefix_ruby}rubygem(activesupport) >= 3.0
Requires: %{?scl_prefix_ruby}rubygem(actionpack) >= 3.0
Requires: %{?scl_prefix_ruby}rubygem(railties) >= 3.0
Requires: %{?scl_prefix_ruby}rubygem(rails) >= 3.0
Requires: %{?scl_prefix_ruby}rubygem(bundler) >= 1.0.0
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
%{?scl:Obsoletes: ruby193-rubygem-%{gem_name}}

%description
Haml-rails provides Haml generators for Rails 3. It also enables Haml as the
templating engine for you, so you don't have to screw around in your own
application.rb when your Gemfile already clearly indicated what templating
engine you have installed. Hurrah.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir %{buildroot}%{gem_dir} \
            --force --rdoc %{SOURCE0}
%{?scl:"}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gem_dir}/gems/%{gem_name}-%{version}/
%doc %{gem_dir}/doc/%{gem_name}-%{version}
%{gem_dir}/cache/%{gem_name}-%{version}.gem
%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec

%changelog
* Mon Dec 01 2014 Justin Sherrill <jsherril@redhat.com> 0.4-1
- downgrading haml-rails to 0.4 (jsherril@redhat.com)

* Mon Dec 01 2014 Justin Sherrill <jsherril@redhat.com> 0.3.4-6
- remove empty tito.props and definition which are duplicate with default from
  rel-eng/tito.props (msuchy@redhat.com)
- with recent tito you do not need SCL meta package (msuchy@redhat.com)

* Fri Mar 01 2013 Miroslav Suchý <msuchy@redhat.com> 0.3.4-5
- fix requires on ruby abi (msuchy@redhat.com)

* Tue Feb 26 2013 Miroslav Suchý <msuchy@redhat.com> 0.3.4-4
- new package built with tito

* Wed Jan 19 2011 Jason E. Rist <jrist@redhat.com> 0.3.4-3
- Added ruby 1.8. require.

* Wed Jan 19 2011 Jason E. Rist <jrist@redhat.com> 0.3.4-2
- new package built with tito

* Wed Jan 19 2011 Jason E. Rist <jrist@jrist> - 0.3.4-1
- Initial package
