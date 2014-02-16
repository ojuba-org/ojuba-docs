%global owner ojuba-org
%global commit #Write commit number here
%global fedora_version 20
%global ojuba_version 35
%global date %( date +%Y%m%d )

Name:		ojuba-docs
Version:	%{ojuba_version}.2.4
Release:	1.%{date}%{?dist}
BuildArch:	noarch
Summary:	Documentation from ojuba.org
URL:		http://ojuba.org
Group:		System Environment/Base
License:	WAQFv2
Source:		https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
BuildRequires:	bash
BuildRequires:	desktop-file-utils
Requires:	ojuba-docs-common = %{version}-%{release}
Requires:	xdg-utils


%description 
Arabic documentation provided by ojuba.org community.
It covers all aspects of computing from using to software development.

%package -n ojuba-linux-docs
Summary:	Ojuba Linux %{ojuba_version} Documentation
Group:		System Environment/Base
License:	Waqf
URL:		http://ojuba.org
BuildArch:	noarch
Requires:	ojuba-docs-common = %{version}-%{release}
Requires:	xdg-utils

%description -n ojuba-linux-docs
These are the official documentation for ojuba linux %{ojuba_version},

%package -n ojuba-release-notes
Summary:	Release Notes for ojuba linux %{ojuba_version}
Group:		System Environment/Base
License:	Waqf
URL:		http://ojuba.org
BuildArch:	noarch
Provides:	indexhtml = %{fedora_version}-%{release}
Provides:	fedora-release-notes = %{fedora_version}-%{release}
Obsoletes:	indexhtml < 9-3
Requires:	ojuba-docs-common = %{version}-%{release}
Requires:	xdg-utils

%description -n ojuba-release-notes
These are the official Release Notes for ojuba linux %{ojuba_version},

%package -n ojuba-docs-common
Summary:	common files needed by ojuba linux %{ojuba_version} documentation
Group:		System Environment/Base
License:	Waqf
URL:		http://ojuba.org
BuildArch:	noarch
Provides:	indexhtml = %{fedora_version}-%{release}
Provides:	fedora-release-notes = %{fedora_version}-%{release}
Obsoletes:	indexhtml < 9-3

%description -n ojuba-docs-common
Common files shared between all ojuba linux %{ojuba_version} documentations


%prep
%setup -q -n %{name}-%{commit}

%build
bash get-oj-docs-from-site.sh
bash get-oj-linux-docs-from-site.sh %{ojuba_version}

%install
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-docs/
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

cp -a release-notes/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/
cp -a homepage/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/
cp -a desktop/*.desktop $RPM_BUILD_ROOT%{_datadir}/applications/

install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/ojuba-documents

cp -a ojuba-docs/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-docs/
cp -a ojuba-linux-docs/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/

ln -s %{_defaultdocdir}/HTML/ojuba-docs/all.css $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/all.css
ln -s %{_defaultdocdir}/HTML/ojuba-docs/all.css $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/all.css
ln -s %{_defaultdocdir}/HTML/ojuba-docs/img $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/
ln -s %{_defaultdocdir}/HTML/ojuba-docs/img $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ojuba-documents
ln -s %{_defaultdocdir}/HTML/ojuba-docs/ "$RPM_BUILD_ROOT%{_datadir}/ojuba-documents/وثائق بوابة أعجوبة"
ln -s %{_defaultdocdir}/HTML/release-notes/RELEASE-NOTES-ar.html "$RPM_BUILD_ROOT%{_datadir}/ojuba-documents/ملحوظات الإصدار.html"
ln -s %{_defaultdocdir}/HTML/ojuba-linux-docs/ "$RPM_BUILD_ROOT%{_datadir}/ojuba-documents/وثائق أعجوبة لينكس"

find ojuba-docs -type f | grep -v 'ojuba-docs/img/' | grep -v '\.css$' |
  sed -e 's!^!%{_defaultdocdir}/HTML/!g;' > .ojuba-docs.ls

%post
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%postun
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%post -n ojuba-linux-docs
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%postun -n ojuba-linux-docs
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%post -n ojuba-release-notes
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi

%postun -n ojuba-release-notes
if [ -x /usr/bin/scrollkeeper-update ]; then scrollkeeper-update -q; fi
if [ -x /usr/bin/update-desktop-database ]; then update-desktop-database &> /dev/null; fi


%files -f .ojuba-docs.ls
%defattr(-,root,root,-)
%{_datadir}/applications/ojuba-docs.desktop

%files -n ojuba-docs-common
%defattr(-,root,root,-)
%{_defaultdocdir}/HTML/ojuba-docs/*.css
%{_defaultdocdir}/HTML/ojuba-docs/img/*.png

%files -n ojuba-release-notes
%defattr(-,root,root,-)
%{_defaultdocdir}/HTML/*.html
%{_defaultdocdir}/HTML/*.css
%{_defaultdocdir}/HTML/images/*
%{_defaultdocdir}/HTML/release-notes/
%{_datadir}/applications/ojuba-release-notes.desktop
%{_datadir}/ojuba-documents/

%files -n ojuba-linux-docs
%defattr(-,root,root,-)
%{_defaultdocdir}/HTML/ojuba-linux-docs/
%{_datadir}/applications/ojuba-linux-docs.desktop

%changelog
* Sun Feb 16 2014 Mosaab Alzoubi <moceap@hotmail.com> - 35.2.4-1.20140216
- General Revision.

* Wed Jul 28 2010 Muayyad Alsadi <alsadi@ojuba.org> - 4.0.2-1
- minor fix

* Wed Jun 23 2010 Muayyad Alsadi <alsadi@ojuba.org> - 4.0.0-7
- reworked to get data from the wiki
