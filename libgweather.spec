#
# Conditional build:
%bcond_without	vala		# do not build Vala API
#
Summary:	Library to access weather information from online services for numerous locations
Summary(pl.UTF-8):	Biblioteka dostępu do informacji pogodowych z serwisów internetowych dla różnych miejsc
Name:		libgweather
Version:	3.10.0
Release:	1
License:	GPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgweather/3.10/%{name}-%{version}.tar.xz
# Source0-md5:	fe37c6b8f58fd678a7bcfdbdfe4bd1bf
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-devel >= 0.18
BuildRequires:	glib2-devel >= 1:2.35.1
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	intltool >= 0.50.0
BuildRequires:	libsoup-devel >= 2.34.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.18.0}
BuildRequires:	xz
Requires(post,postun):	gnome-icon-theme
Requires(post,postun):	gnome-icon-theme-symbolic
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	glib2 >= 1:2.35.1
Requires:	glib2 >= 1:2.35.1
Requires:	libsoup >= 2.34.0
Requires:	libxml2 >= 1:2.6.30
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgweather is a library to access weather information from online
services for numerous locations.

%description -l pl.UTF-8
libgweather to biblioteka pozwalająca na dostęp do informacji
pogodowych z serwisów internetowych dla różnych miejsc.

%package devel
Summary:	Header files for libgweather
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgweather
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+3-devel >= 3.0.0
Requires:	libsoup-devel >= 2.34.0
Requires:	libxml2-devel >= 1:2.6.30
Obsoletes:	gnome-applets-devel <= 2.21.4

%description devel
Header files for libgweather.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgweather.

%package static
Summary:	Static libgweather library
Summary(pl.UTF-8):	Statyczna biblioteka libgweather
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libgweather library.

%description static -l pl.UTF-8
Statyczna biblioteka libgweather.

%package apidocs
Summary:	libgweather API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libgweather
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libgweather API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libgweather.

%package -n vala-libgweather
Summary:        libgweather API for Vala language
Summary(pl.UTF-8):      API biblioteki libgweather dla języka Vala
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       vala >= 2:0.18.0

%description -n vala-libgweather
libgweather API for Vala language.

%description -n vala-libgweather -l pl.UTF-8
API biblioteki libgweather dla języka Vala.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable vala vala} \
	--with-zoneinfo-dir=%{_datadir}/zoneinfo \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--disable-silent-rules \
	--enable-static

%{__make} -j1 -C data
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/es_ES
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang libgweather-3.0 --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas
%update_icon_cache gnome

%postun
/sbin/ldconfig
%glib_compile_schemas
%update_icon_cache gnome

%files -f libgweather-3.0.lang
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_libdir}/libgweather-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgweather-3.so.6
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.gschema.xml
%dir %{_datadir}/libgweather
%{_datadir}/libgweather/Locations.xml
%{_datadir}/libgweather/locations.dtd
%{_iconsdir}/gnome/*/status/*.png
%{_iconsdir}/gnome/scalable/status/*.svg
%{_libdir}/girepository-1.0/GWeather-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgweather-3.so
%{_includedir}/libgweather-3.0
%{_pkgconfigdir}/gweather-3.0.pc
%{_datadir}/gir-1.0/GWeather-3.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libgweather-3.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libgweather-3.0

%if %{with vala}
%files -n vala-libgweather
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gweather-3.0.vapi
%endif
