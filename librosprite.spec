#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	RISC OS sprite files loading library
Summary(pl.UTF-8):	Biblioteka do odczytu plików sprite z RISC OS
Name:		librosprite
Version:	0.1.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	e0812c37dec68e3242bfe97d7dc75c1d
URL:		http://www.netsurf-browser.org/projects/librosprite/
BuildRequires:	netsurf-buildsystem >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RISC OS sprite files loading library.

%description -l pl.UTF-8
Biblioteka do odczytu plików sprite z RISC OS.

%package devel
Summary:	librosprite library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki librosprite
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the include files and other resources you can
use to incorporate librosprite into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki librosprite w
swoich programach.

%package static
Summary:	librosprite static library
Summary(pl.UTF-8):	Statyczna biblioteka librosprite
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static librosprite library.

%description static -l pl.UTF-8
Statyczna biblioteka librosprite.

%prep
%setup -q

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/librosprite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librosprite.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librosprite.so
%{_includedir}/librosprite.h
%{_pkgconfigdir}/librosprite.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librosprite.a
%endif
