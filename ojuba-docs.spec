%define fedora_version 15.0.0
%define ojuba_version 5
Name:		ojuba-docs
Version:	%{ojuba_version}.0.3
Release:	1
Summary:	Documentation from ojuba.org
URL:		http://docs.ojuba.org
Group:		System Environment/Base
License:	Waqf
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	desktop-file-utils, bash
Requires:	ojuba-docs-common = %{version}-%{release}
Requires:	xdg-utils


%description 
Arabic documentation provided by ojuba.org community.
It covers all aspects of computing from using to software development.

%package -n ojuba-linux-docs
Summary:	Ojuba Linux %{ojuba_version} Documentation
Group:		System Environment/Base
License:	Waqf
URL:		http://linux.ojuba.org
BuildArch:	noarch
Requires:	ojuba-docs-common = %{version}-%{release}
Requires:	xdg-utils
%description -n ojuba-linux-docs
These are the official documentation for ojuba linux %{ojuba_version},

%package -n ojuba-release-notes
Summary:	Release Notes for ojuba linux %{ojuba_version}
Group:		System Environment/Base
License:	Waqf
URL:		http://linux.ojuba.org
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
URL:		http://linux.ojuba.org
BuildArch:	noarch
Provides:	indexhtml = %{fedora_version}-%{release}
Provides:	fedora-release-notes = %{fedora_version}-%{release}
Obsoletes:	indexhtml < 9-3

%description -n ojuba-docs-common
Common files shared between all ojuba linux %{ojuba_version} documentations


%prep
%setup -q

%build
bash get-oj-docs-from-site.sh
bash get-oj-linux-docs-from-site.sh

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-docs/
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/img
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

cp -a release-notes/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/
cp -a homepage/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/
cp -a desktop/*.desktop $RPM_BUILD_ROOT%{_datadir}/applications/


install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/ojuba-documents

cp -a ojuba-docs/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-docs/
cp -a ojuba-linux-docs/* $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/

ln -s %{_defaultdocdir}/HTML/ojuba-docs/all.css $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/all.css
ln -s %{_defaultdocdir}/HTML/ojuba-docs/all.css $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/all.css

ln -s %{_defaultdocdir}/HTML/ojuba-docs/img $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/release-notes/img

ln -s %{_defaultdocdir}/HTML/ojuba-docs/img $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/ojuba-linux-docs/img

mkdir -p $RPM_BUILD_ROOT%{_datadir}/ojuba-documents
ln -s %{_defaultdocdir}/HTML/ojuba-docs/ "$RPM_BUILD_ROOT%{_datadir}/ojuba-documents/وثائق بوابة أعجوبة"
ln -s %{_defaultdocdir}/HTML/release-notes/RELEASE-NOTES-ar.html "$RPM_BUILD_ROOT%{_datadir}/ojuba-documents/ملحوظات الإصدار.html"
ln -s %{_defaultdocdir}/HTML/ojuba-linux-docs/ "$RPM_BUILD_ROOT%{_datadir}/ojuba-documents/وثائق أعجوبة لينكس"

find ojuba-docs -type f | grep -v '\.png$' | grep -v '\.css$' |
  sed -e 's!^!%{_defaultdocdir}/HTML/'!g;' > .ojuba-docs.ls

%clean
rm -rf $RPM_BUILD_ROOT

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
* Wed Jul 28 2010 Muayyad Alsadi <alsadi@ojuba.org> - 4.0.2-1
- minor fix

* Wed Jun 23 2010 Muayyad Alsadi <alsadi@ojuba.org> - 4.0.0-7
- reworked to get data from the wiki

