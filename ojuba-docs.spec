%global owner ojuba-org
%global commit #Write commit number here
%global fedora_version 22
%global ojuba_version 36
%global date %( date +%Y%m%d )

Name: ojuba-docs
Version: %{ojuba_version}
Release: 1.%{date}%{?dist}
BuildArch: noarch
Summary: Documentation from Ojuba.org
Summary(ar): وثائق أعجوبة
URL: http://ojuba.org
License: WAQFv2
Source: https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
BuildRequires: bash
BuildRequires: desktop-file-utils
Requires: ojuba-docs-common = %{version}-%{release}
Requires: xdg-utils


%description 
Arabic documentation provided by ojuba.org community.
It covers all aspects of computing from using to
software development.

%description -l ar
وثائق أعجوبة المزّودة من قبل بوّابة أعجوبة الإلكترونية.
تُغطي الوثائق ما يتعلق بالحوسبة من الاستخدام و حتّى التّطوير.

%package -n ojuba-os-docs
Summary: Ojuba %{ojuba_version} Documentation
Sumary(ar): وثائق نظام أعجوبة %{ojuba_version}
License: WAQFv2
URL: http://ojuba.org
BuildArch: noarch
Requires: ojuba-docs-common = %{version}-%{release}
Requires: xdg-utils

%description -n ojuba-os-docs
These are the official documentation for Ojuba OS %{ojuba_version},

%description -n ojuba-os-docs -l ar
الوثائق الرّسمية لنظام أعجوبة %{ojuba_version}.

%package -n ojuba-release-notes
Summary: Release Notes for Ojuba OS %{ojuba_version}
Sumary(ar): ملحوظات إصدار أعجوبة %{ojuba_version}
License: WAQFv2
URL: http://ojuba.org
BuildArch: noarch
Provides: indexhtml = %{fedora_version}-%{release}
Provides: fedora-release-notes = %{fedora_version}-%{release}
Obsoletes: indexhtml
Requires: ojuba-docs-common = %{version}-%{release}
Requires: xdg-utils

%description -n ojuba-release-notes
These are the official Release Notes for Ojuba OS %{ojuba_version}.

%description -n ojuba-release-notes -l ar
ملحوظات إصدار نظام أعجوبة %{ojuba_version}.

%package -n ojuba-docs-common
Summary: Common files of ojuba-docs
Summary(ar): الملفات المشتركة للوثائق
License: WAQFv2
URL: http://ojuba.org
BuildArch: noarch
Requires: rarian-compat

%description -n ojuba-docs-common
Common files shared between all Ojuba OS %{ojuba_version} documentations.

%description -n ojuba-docs-common -l ar
الملفات المشتركة لكل توثيقات نظام أعجوبة %{ojuba_version}.

%prep
%setup -q -n %{name}-%{commit}

%build
bash get-oj-docs-from-site.sh
bash get-oj-os-docs-from-site.sh %{ojuba_version}

%install
mkdir -p %{buildroot}%{_defaultdocdir}/HTML/ojuba-docs/
mkdir -p %{buildroot}%{_defaultdocdir}/HTML/ojuba-os-docs/
mkdir -p %{buildroot}%{_defaultdocdir}/HTML/release-notes/
mkdir -p %{buildroot}%{_datadir}/applications

cp -a release-notes/* %{buildroot}%{_defaultdocdir}/HTML/release-notes/
cp -a homepage/* %{buildroot}%{_defaultdocdir}/HTML/
cp -a desktop/*.desktop %{buildroot}%{_datadir}/applications/

install -m 755 -d %{buildroot}%{_datadir}/ojuba-documents

cp -a ojuba-docs/* %{buildroot}%{_defaultdocdir}/HTML/ojuba-docs/
cp -a ojuba-os-docs/* %{buildroot}%{_defaultdocdir}/HTML/ojuba-os-docs/

ln -s %{_defaultdocdir}/HTML/ojuba-docs/all.css %{buildroot}%{_defaultdocdir}/HTML/release-notes/all.css
ln -s %{_defaultdocdir}/HTML/ojuba-docs/all.css %{buildroot}%{_defaultdocdir}/HTML/ojuba-os-docs/all.css
ln -s %{_defaultdocdir}/HTML/ojuba-docs/img %{buildroot}%{_defaultdocdir}/HTML/release-notes/
ln -s %{_defaultdocdir}/HTML/ojuba-docs/img %{buildroot}%{_defaultdocdir}/HTML/ojuba-os-docs/
mkdir -p %{buildroot}%{_datadir}/ojuba-documents
ln -s %{_defaultdocdir}/HTML/ojuba-docs/ "%{buildroot}%{_datadir}/ojuba-documents/وثائق بوابة أعجوبة"
ln -s %{_defaultdocdir}/HTML/release-notes/RELEASE-NOTES-ar.html "%{buildroot}%{_datadir}/ojuba-documents/ملحوظات الإصدار.html"
ln -s %{_defaultdocdir}/HTML/ojuba-os-docs/ "%{buildroot}%{_datadir}/ojuba-documents/وثائق أعجوبة لينكس"

find ojuba-docs -type f | grep -v 'ojuba-docs/img/' | grep -v '\.css$' |
  sed -e 's!^!%{_defaultdocdir}/HTML/!g;' > .ojuba-docs.ls

%post
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%postun
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%post -n ojuba-os-docs
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%postun -n ojuba-os-docs
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%post -n ojuba-release-notes
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%postun -n ojuba-release-notes
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi


%files -f .ojuba-docs.ls
%{_datadir}/applications/ojuba-docs.desktop

%files -n ojuba-docs-common
%{_defaultdocdir}/HTML/ojuba-docs/*.css
%{_defaultdocdir}/HTML/ojuba-docs/img/*.png

%files -n ojuba-release-notes
%{_defaultdocdir}/HTML/*.html
%{_defaultdocdir}/HTML/*.css
%{_defaultdocdir}/HTML/images/*
%{_defaultdocdir}/HTML/release-notes/
%{_datadir}/applications/ojuba-release-notes.desktop
%{_datadir}/ojuba-documents/

%files -n ojuba-os-docs
%{_defaultdocdir}/HTML/ojuba-os-docs/
%{_datadir}/applications/ojuba-os-docs.desktop

%changelog
* Sun Feb 16 2014 Mosaab Alzoubi <moceap@hotmail.com> - 36-1.20150721
- General Revision
- Update to ver 36
- Add Arabic Summary and Descriptions
- Remove Group tag
- Remove repeated provides
- New name for some packages
- Remove old ATTR way

* Sun Feb 16 2014 Mosaab Alzoubi <moceap@hotmail.com> - 35.2.4-1.20140216
- General Revision.

* Wed Jul 28 2010 Muayyad Alsadi <alsadi@ojuba.org> - 4.0.2-1
- minor fix

* Wed Jun 23 2010 Muayyad Alsadi <alsadi@ojuba.org> - 4.0.0-7
- reworked to get data from the wiki
