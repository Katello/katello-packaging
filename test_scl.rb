#!/usr/bin/env ruby

require 'open-uri'

SCL='tfm'

packages_to_build = [
  'rubygem-anemone',
  'rubygem-haml',
  'rubygem-haml-rails',
  'rubygem-hashr',
  'rubygem-hooks',
  'rubygem-tire',
  'rubygem-robotex',
  'rubygem-strong_parameters',
  'rubygem-qpid_messaging',
  'rubygem-runcible',
  'rubygem-hammer_cli_csv',
  'rubygem-hammer_cli_gutterball',
  'rubygem-hammer_cli_sam',
  'rubygem-hammer_cli_katello',
  'rubygem-hammer_cli_import',
  'rubygem-katello',
  'rubygem-foreman_gutterball',
  'katello',
  'katello-utils'
]

def install_dependency(package_name)
  `rpm -q #{package_name}`
  `sudo yum -y install #{package_name}` unless $? == 0
end

def make_local_scl_repo
  puts "Generating local ruby193 SCL repository at /tmp/local_ruby193_scl_repo"
  Dir.mkdir('/tmp/local_ruby193_scl_repo') unless File.exist?('/tmp/local_ruby193_scl_repo')

  scl_index = open('https://www.softwarecollections.org/repos/rhscl/ruby193/epel-7-x86_64/', &:read)
  hrefs = scl_index.scan(/href=".*.rpm"/).collect { |link| link.split('href="')[1].split('">')[0] }

  Dir.chdir('/tmp/local_ruby193_scl_repo') do
    hrefs.each do |href|
      unless File.exist?(href)
        `wget https://www.softwarecollections.org/repos/rhscl/ruby193/epel-7-x86_64/#{href}`
      end
    end
  end
  `createrepo /tmp/local_ruby193_scl_repo`
end

def make_tmp_repository
  puts "Generating local repository at /tmp/test_scl_repo"
  Dir.mkdir('/tmp/test_scl_repo') unless File.exist?('/tmp/test_scl_repo')
  `createrepo /tmp/test_scl_repo`
end

def remove_package(package, tfm = true)
  `rm -f /tmp/test_scl_repo/#{tfm ? 'tfm-' : ''}#{package}*`
  `rm -f mock/result/#{tfm ? 'tfm-' : ''}#{package}*`
end

def build_srpm(package)
  output = Dir.chdir(package) do
    `tito build --srpm --test --dist=.el7 --scl=#{SCL}`
  end
  output.split('Wrote: ').last
end

def mock_build(srpm_path)
  puts "mock -r ./mock/foreman-scl.cfg #{srpm_path}"
  if srpm_path.include?('qpid') || srpm_path.include?('katello')
    `mock --no-clean -r ./mock/foreman-scl.cfg --install http://koji.katello.org/packages/qpid-cpp/0.30/7.proton.0.9.el7/x86_64/qpid-cpp-client-devel-0.30-7.proton.0.9.el7.x86_64.rpm --install http://koji.katello.org/packages/qpid-cpp/0.30/7.proton.0.9.el7/x86_64/qpid-cpp-client-0.30-7.proton.0.9.el7.x86_64.rpm`
  end
  `mock --no-clean --resultdir=mock/result -r ./mock/foreman-scl.cfg #{srpm_path}`
end

def mock_clean
  `mock -r ./mock/foreman-scl.cfg --clean`
  `rm -rf mock/result/*`
end

def rebuild_local_repo(package)
  `cp -f mock/result/*#{package}*.rpm /tmp/test_scl_repo`
  `createrepo /tmp/test_scl_repo`
end

%w(mock tito git-annex createrepo scl-utils scl-utils-build).each do |package|
  install_dependency(package)
end

#make_local_scl_repo
make_tmp_repository

packages_to_build.each do |package|
  if ARGV[0] == package || !Dir.entries('/tmp/test_scl_repo').any? { |entry| entry.include?("tfm-#{package}") || entry.include?(package) }
    `./setup_sources.sh #{package}`
    remove_package(package)
    srpm_path = build_srpm(package)
    mock_build(srpm_path)
    rebuild_local_repo(package)
  end
  #mock_clean
end
