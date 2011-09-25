Summary:	Finger Lakes Instrumentation software development library
Summary(pl.UTF-8):	Biblioteka obsługująca urządzenia Finger Lakes Instrumentation
Name:		libfli
Version:	1.71
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.flicamera.com/downloads/fli-dist-%{version}.tgz
# Source0-md5:	2bcbf524544dd5d6e599a59c5b239ee9
Patch0:		%{name}-shared.patch
Patch1:		%{name}-nodebug.patch
Patch2:		%{name}-linux.patch
URL:		http://www.flicamera.com/software/index.html
BuildRequires:	cfitsio-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
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

%package tools
Summary:	Tools for Finger Lakes Instrumentation devices
Summary(pl.UTF-8):	Programy do urządzeń Finger Lakes Instrumentation
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description tools
Tools for Finger Lakes Instrumentation devices.

%description tools -l pl.UTF-8
Programy do urządzeń Finger Lakes Instrumentation.

%prep
%setup -q -n fli-dist-%{version}
%patch0 -p1
%undos libfli/libfli.c
%patch1 -p1
%patch2 -p1

%{__sed} -i -e 's,cfitsio/fitsio\.h,fitsio.h,' libfli/takepic/takepic.c

%build
%{__make} -C libfli \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
	CPPFLAGS="%{rpmcppflags} -I$(pwd)/libfli -I$(pwd)/libfli/unix" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir}

%{__make} -C libfli/flifilter \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -I.." \
	LOADLIBES="%{rpmldflags} -L../.libs"

%{__make} -C libfli/takepic \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -I.. -DUSEPNG -DUSEFITS" \
	LOADLIBES="%{rpmldflags} -L../.libs"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C libfli install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir}

install -D libfli/takepic/takepic $RPM_BUILD_ROOT%{_bindir}/flitakepic
install libfli/flifilter/flifilter $RPM_BUILD_ROOT%{_bindir}

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

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/flifilter
%attr(755,root,root) %{_bindir}/flitakepic
