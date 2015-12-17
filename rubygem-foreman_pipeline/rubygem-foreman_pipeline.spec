# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation
# /1/html/Software_Collections_Guide/index.html

%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_pipeline
%global foreman_dir /usr/share/foreman
%global scl_rake /usr/bin/%{?scl:%{scl_prefix}}rake

%define rubyabi 1.9.1

Summary:    A Foreman plugin that cooperates with Jenkins
Name:       %{?scl_prefix}rubygem-%{gem_name}
Version:    0.0.8
Release:    1%{?foremandist}%{?dist}
Group:      Applications/System
License:    GPLv3
URL:        http://github.com/theforeman/foreman_pipeline
Source0:    http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Requires:   %{?scl_prefix}rubygem(jenkins_api_client) < 2.0.0
Requires:   %{?scl_prefix}rubygem(foreman_deployments) < 1.0.0
Requires:   %{?scl_prefix}rubygem(net-ssh) >= 2.9
Requires:   %{?scl_prefix}rubygem(net-ssh) < 3.0
Requires:   %{?scl_prefix}rubygem(net-scp) >= 1.1
Requires:   %{?scl_prefix}rubygem(net-scp) < 2.0
Requires:   %{?scl_prefix}rubygem-katello >= 2.4.0
Requires:   %{?scl_prefix}rubygem-katello < 3.0.0
Requires:   %{?scl_prefix}rubygem(bastion) >= 2.0.0
Requires:   %{?scl_prefix}rubygem(bastion) < 3.0.0

BuildRequires: foreman-plugin >= 1.8.0
BuildRequires: %{?scl_prefix}rubygem(jenkins_api_client) < 2.0.0
BuildRequires: %{?scl_prefix}rubygem(foreman_deployments) < 1.0.0
BuildRequires: %{?scl_prefix}rubygem(net-ssh) >= 2.9
BuildRequires: %{?scl_prefix}rubygem(net-ssh) < 3.0
BuildRequires: %{?scl_prefix}rubygem(net-scp) >= 1.1
BuildRequires: %{?scl_prefix}rubygem(net-scp) < 2.0
BuildRequires: %{?scl_prefix}rubygem-katello >= 2.4.0
BuildRequires: %{?scl_prefix}rubygem-katello < 3.0.0
BuildRequires: %{?scl_prefix}rubygem(bastion) >= 2.0.0
BuildRequires: %{?scl_prefix}rubygem(bastion) < 3.0.0

%if 0%{?fedora} > 18
Requires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
%else
Requires: %{?scl_prefix_ruby}ruby(abi) >= %{rubyabi}
BuildRequires: %{?scl_prefix_ruby}ruby(abi) >= %{rubyabi}
%endif

Requires: %{?scl_prefix_ruby}rubygems
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygems
BuildRequires: foreman-assets

BuildArch: noarch

Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-plugin-pipeline

%description
This plugin allows Jenkins to deploy artifacts onto newly 
provisioned host by Foreman.

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

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
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p ./usr/share
cp -r %{foreman_dir} ./usr/share || echo 0

mkdir -p ./%{_localstatedir}/lib/foreman
cp -r /var/lib/foreman/db ./%{_localstatedir}/lib/foreman || echo 0
unlink ./usr/share/foreman/db
ln -sv `pwd`/%{_localstatedir}/lib/foreman/db ./usr/share/foreman/db

cp -r /var/lib/foreman/public ./%{_localstatedir}/lib/foreman || echo 0
unlink ./usr/share/foreman/public
ln -sv `pwd`/%{_localstatedir}/lib/foreman/public ./usr/share/foreman/public

unlink ./usr/share/foreman/config/database.yml
unlink ./usr/share/foreman/config/settings.yaml
unlink ./usr/share/foreman/config/initializers/encryption_key.rb

cp /etc/foreman/settings.yaml ./usr/share/foreman/config

cat <<DB >> ./usr/share/foreman/config/database.yml
production:
  adapter: sqlite3
  database: db/production.sqlite3
  pool: 5
  timeout: 5000

development:
  adapter: sqlite3
  database: db/development.sqlite3
  pool: 5
  timeout: 5000
DB

pushd ./usr/share/foreman
sed -i 's/:locations_enabled: false/:locations_enabled: true/' config/settings.yaml
sed -i 's/:organizations_enabled: false/:organizations_enabled: true/' config/settings.yaml
export GEM_PATH=%{buildroot}%{gem_dir}:${GEM_PATH:+${GEM_PATH}}${GEM_PATH:-`scl enable %{scl_ruby} -- ruby -e "print Gem.path.join(':')"`}

cat <<GEMFILE >> ./bundler.d/%{gem_name}.rb
gem '%{gem_name}'
GEMFILE

unlink tmp

export BUNDLER_EXT_NOSTRICT=1
#export BUNDLER_EXT_GROUPS="default assets"

%{scl_rake} security:generate_encryption_key --trace
%{scl_rake} plugin:assets:precompile['%{gem_name}'] RAILS_ENV=production --trace
%{scl_rake} db:migrate RAILS_ENV=development --trace
%{scl_rake} plugin:apipie:cache['%{gem_name}'] RAILS_ENV=development cache_part=resources OUT=%{buildroot}%{gem_instdir}/public/apipie-cache/plugin/%{gem_name} --trace

popd
rm -rf ./usr

mkdir -p %{buildroot}%{foreman_bundlerd_dir}
cat <<GEMFILE > %{buildroot}%{foreman_bundlerd_dir}/%{gem_name}.rb
gem '%{gem_name}'
GEMFILE

mkdir -p %{buildroot}%{foreman_dir}/public/assets
mkdir -p %{buildroot}%{foreman_dir}/public/apipie-cache/plugin
ln -s %{gem_instdir}/public/assets/%{gem_name} %{buildroot}%{foreman_dir}/public/assets/%{gem_name}
ln -s %{gem_instdir}/public/apipie-cache/plugin/%{gem_name} %{buildroot}%{foreman_dir}/public/apipie-cache/plugin/%{gem_name}

%post
cp -r %{foreman_dir}/public/apipie-cache/plugin/%{gem_name}/* %{foreman_dir}/public/apipie-cache/
chown -R foreman.foreman %{foreman_dir}/public/apipie-cache

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_instdir}/db
%{gem_instdir}/script
%{gem_spec}
%{foreman_bundlerd_plugin}
%{foreman_apipie_cache_foreman}
%{foreman_assets_plugin}
%{foreman_dir}/public/apipie-cache/plugin/%{gem_name}
%{foreman_dir}/public/assets/%{gem_name}
%doc %{gem_instdir}/LICENSE

%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/public
%exclude %{gem_cache}

%files doc
%doc %{gem_instdir}/README.md

%posttrans
# We need to run the db:migrate after the install transaction

%foreman_db_migrate
%foreman_db_seed
%foreman_apipie_cache
%foreman_restart
exit 0

%changelog
* Thu Nov 12 2015 Ondrej Prazak <oprazak@redhat.com> 0.0.8-1
- initial build
