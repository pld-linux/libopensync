#
# Conditional build:
%bcond_without	python	# don't build python binding

Summary:	Data synchronization framework
Summary(pl.UTF-8):	Szkielet do synchronizacji danych
Name:		libopensync
Version:	0.39
Release:	12
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://www.opensync.io/download/releases/0.39/%{name}-%{version}.tar.bz2
# Source0-md5:	733211e82b61e2aa575d149dda17d475
Patch0:		python-syntax.patch
Patch1:		python-noarch-plugins.patch
Patch2:		%{name}-glib.patch
Patch3:		%{name}-python.patch
Patch4:		notests.patch
URL:		https://www.opensync.io/
BuildRequires:	check
BuildRequires:	cmake >= 2.8.2-2
BuildRequires:	glib2-devel >= 1:2.12
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	libxslt-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	sqlite3-devel >= 3.3
%if %{with python}
BuildRequires:	python-devel >= 2
BuildRequires:	python-modules >= 2
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
Requires:	glib2 >= 1:2.12
# no such opensync plugins (yet?)
Obsoletes:	multisync-ldap
Obsoletes:	multisync-opie
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenSync is a synchronization framework that is platform and
distribution independent.

It consists of several plugins that can be used to connect to devices,
a powerful sync-engine and the framework itself.

The synchronization framework is kept very flexible and is capable of
synchronizing any type of data, including contacts, calendar, tasks,
notes and files.

%description -l pl.UTF-8
OpenSync to niezależny od platformy i dystrybucji szkielet do
synchronizacji danych.

Składa się z kilku wtyczek, których można używać do łączenia się z
urządzeniami, potężnego silnika synchronizującego i samego szkieletu.

Szkielet do synchronizacji jest utrzymywany jako bardzo elastyczny i
potrafiący synchronizować dowolny rodzaj danych, włącznie z
kontaktami, kalendarzem, zadaniami, notatkami i plikami.

%package devel
Summary:	Header files for opensync library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki opensync
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	glib2-devel >= 1:2.12
Obsoletes:	libopensync-static
Obsoletes:	multisync-devel
Conflicts:	libopensync02-devel

%description devel
Header files for opensync library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki opensync.

%package -n python-opensync
Summary:	Python bindings for opensync library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki opensync
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-opensync
Python bindings for opensync library.

%description -n python-opensync -l pl.UTF-8
Wiązania Pythona do biblioteki opensync.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

# broken, use fixed from cmake itself
%{__rm} cmake/modules/*Python*.cmake

%build
mkdir build
cd build
%cmake .. \
	-DPYTHON_VERSION=%{py_ver}

%{__make}

%py_lint

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

install -d $RPM_BUILD_ROOT%{_datadir}/libopensync1/defaults
install -d $RPM_BUILD_ROOT%{_libdir}/libopensync1/plugins
install -d $RPM_BUILD_ROOT%{_libdir}/libopensync1/formats

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/osyncbinary
%attr(755,root,root) %{_bindir}/osyncdump
%attr(755,root,root) %{_bindir}/osyncplugin
%attr(755,root,root) %{_libdir}/libopensync.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopensync.so.1
%dir %{_libdir}/libopensync1
%dir %{_libdir}/libopensync1/plugins
%dir %{_libdir}/libopensync1/formats
%attr(755,root,root) %{_libdir}/libopensync1/osplugin
%dir %{_datadir}/libopensync1
%{_datadir}/libopensync1/capabilities
%{_datadir}/libopensync1/defaults
%{_datadir}/libopensync1/descriptions
%{_datadir}/libopensync1/schemas

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopensync.so
%{_includedir}/libopensync1
%{_pkgconfigdir}/libopensync.pc
%dir %{_datadir}/libopensync1/cmake
%dir %{_datadir}/libopensync1/cmake/modules
%{_datadir}/libopensync1/cmake/modules/OpenSync*.cmake

%if %{with python}
%files -n python-opensync
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_opensync.so
%{py_sitedir}/opensync.py[co]
%endif
