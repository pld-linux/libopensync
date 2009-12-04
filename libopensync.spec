# Conditional build:
%bcond_without	python		# don't build python binding
#
Summary:	Data synchronization framework
Summary(pl.UTF-8):	Szkielet do synchronizacji danych
Name:		libopensync
Version:	0.37
Release:	7
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opensync.org/download/releases/0.37/%{name}-%{version}.tar.bz2
# Source0-md5:	5b99caaf15d878719f9135713f63ebc5
Patch0:		%{name}-python_wrapper_update.patch
URL:		http://www.opensync.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	check
BuildRequires:	cmake
BuildRequires:	glib2-devel >= 1:2.10
BuildRequires:	libint-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	libxslt-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.385
BuildRequires:	sqlite3-devel >= 3.3
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
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
Requires:	glib2-devel >= 1:2.10
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
%patch0 -p1

%build
rm cmake/modules/*Python*.cmake
mkdir build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPYTHON_VERSION=%{py_ver} \
%if "%{_lib}" != "lib"
	-DLIB_SUFFIX=64 \
%endif
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/libopensync1/defaults
install -d $RPM_BUILD_ROOT%{_libdir}/libopensync1/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libopensync.so.*
%dir %{_libdir}/libopensync1
%dir %{_libdir}/libopensync1/formats
%dir %{_libdir}/libopensync1/plugins
%dir %{_datadir}/libopensync1
%attr(755,root,root) %{_libdir}/libopensync1/osplugin
%{_datadir}/libopensync1/capabilities
%{_datadir}/libopensync1/defaults
%{_datadir}/libopensync1/descriptions
%{_datadir}/libopensync1/schemas
%attr(755,root,root) %{_libdir}/libopensync1/formats/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopensync.so
%{_includedir}/libopensync1
%{_pkgconfigdir}/libopensync.pc

%dir %{_datadir}/libopensync1/cmake
%dir %{_datadir}/libopensync1/cmake/modules
%{_datadir}/libopensync1/cmake/modules/*.cmake

%if %{with python}
%files -n python-opensync
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_opensync.so
%{py_sitedir}/opensync.py
%endif
