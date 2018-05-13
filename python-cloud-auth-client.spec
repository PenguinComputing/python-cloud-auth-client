%define build_number %([ -e /build/.scyld-build-number ] && cat /build/.scyld-build-number || echo `date +"%y%m%d.%H.%M"`)
%define debug_package %{nil}

%define name 			python-cloud-auth-client
%define version 		0.1.1
%define _podtoolsenv     /opt/scyld/podtools/env

Summary: Scyld Cloud Authorization Client
Name: %{name}
Version: %{version}
Release: %{build_number}
Vendor: Penguin Computing, Inc.
Packager: Penguin Computing Inc. <http://www.penguincomputing.com>
License: (c) 2002-2018 Penguin Computing, Inc.
Group: Development/Tools
URL: http://www.penguincomputing.com
Distribution: Scyld ClusterWare
Requires: python-scyld-utils >= 1.4.2
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Source0: %{name}-%{version}.tar.gz

%description
Client library for Scyld Cloud Auth API

%prep
%setup -q -n %{name} -c

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/opt/scyld/podtools
source %{_podtoolsenv}/bin/activate
python setup.py install --single-version-externally-managed --root ${RPM_BUILD_ROOT}
pip install -r ${RPM_BUILD_ROOT}/%{_podtoolsenv}/lib/python*/site-packages/python_cloud_auth_client-%{version}-*.egg-info/requires.txt --root ${RPM_BUILD_ROOT}
# HACK to fix RECORD file.
sed -i '/BUILDROOT/d' ${RPM_BUILD_ROOT}/%{_podtoolsenv}/lib/python*/site-packages/*-info/RECORD || true
rm -f ${RPM_BUILD_ROOT}/%{_podtoolsenv}/lib/python*/site-packages/tests/__init__*
deactivate

%clean
%__rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-, root, root, -)
%{_podtoolsenv}/bin/*
%{_podtoolsenv}/lib*/python*/site-packages/*

%post

%changelog
* Fri May 11 2018 Limin Gu <lgu@penguincomputing.com>
- Move installation to podtools virtual environment.

* Mon Oct 17 2016 Limin Gu <lgu@penguincomputing.com>
- Packaging from github source
