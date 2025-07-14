Summary:	Finger Lakes Instrumentation software development library
Summary(pl.UTF-8):	Biblioteka obsługująca urządzenia Finger Lakes Instrumentation
Name:		libfli
Version:	1.104
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.flicamera.com/downloads/sdk/%{name}-%{version}.zip
# Source0-md5:	f1a44f770f327ef0a2aeeb4dc3f8df60
Patch0:		%{name}-shared.patch
Patch1:		%{name}-linux.patch
URL:		http://www.flicamera.com/software/index.html
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
Obsoletes:	libfli-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Finger Lakes Instrumentation software development library brings Linux
support for FLI CCD cameras, filter wheels and focusers.

%description -l pl.UTF-8
Biblioteka Finger Lakes Instrumentation SDK zapewnia obsługę pod
Linuksem urządzeń firmy FLI, takich jak kamery CCD, koła filtrujące
czy układy ogniskujące.

%package devel
Summary:	Header files for FLI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FLI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for FLI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FLI.

%package static
Summary:	Static FLI library
Summary(pl.UTF-8):	Statyczna biblioteka FLI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FLI library.

%description static -l pl.UTF-8
Statyczna biblioteka FLI.

%prep
%setup -q
%patch -P0 -p2
%undos libfli.c
%patch -P1 -p2

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
	CPPFLAGS="%{rpmcppflags} -I$(pwd) -I$(pwd)/unix" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfli.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfli.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfli.so
%{_libdir}/libfli.la
%{_includedir}/libfli.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libfli.a
