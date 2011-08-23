Summary:	Finger Lakes Instrumentation software development library
Summary(pl.UTF-8):	Biblioteka obsługująca urządzenia Finger Lakes Instrumentation
Name:		libfli
Version:	1.71
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://www.flicamera.com/downloads/fli-dist-%{version}.tgz
# Source0-md5:	2bcbf524544dd5d6e599a59c5b239ee9
Patch0:		%{name}-shared.patch
URL:		http://www.flicamera.com/software/index.html
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel
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
%setup -q -n fli-dist-%{version}
%patch0 -p1

%build
%{__make} -C libfli \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
	CPPFLAGS="%{rpmcppflags} -I$(pwd)/libfli -I$(pwd)/libfli/unix" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C libfli install \
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
