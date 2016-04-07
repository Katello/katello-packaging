# vim: sw=4:ts=4:et
#
# Copyright (c) 2016 Red Hat, Inc.

# This program and entire repository is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#

Name:           katello-client-bootstrap
Version:        1.0.0
Release:        1%{?dist}
Summary:        Client bootstrap utility for Foreman and Katello

Group:          System Environment/Base
License:        LGPLv2
URL:            http://www.katello.org
Source0:        https://codeload.github.com/Katello/%{name}/tar.gz/%{version}

BuildArch:      noarch

%description
Client bootstrap utility for Foreman and Katello

%prep

%setup -q -n %{name}-%{version}

%build

%install

mkdir -p %{buildroot}/%{_var}/www/html/pub/
cp bootstrap.py %{buildroot}%{_var}/www/html/pub/bootstrap.py

%files
%defattr(-,apache,apache,-)
%{_var}/www/html/pub
%{_var}/www/html/pub/bootstrap.py

%changelog
