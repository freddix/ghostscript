%bcond_with	bootstrap

Summary:	PostScript & PDF interpreter and renderer
Name:		ghostscript
Version:	9.06
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	http://downloads.sourceforge.net/ghostscript/%{name}-%{version}.tar.bz2
# Source0-md5:	46f9ebe40dc52755287b30704270db11
URL:		http://www.ghostscript.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	docbook-style-dsssl
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	xorg-libX11-devel
%if ! %{with bootstrap}
BuildRequires:	glib-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	%{_prefix}/lib

%description
Ghostscript is a PostScript interpreter. It can render both PostScript
and PDF compliant files to devices which include an X window, many
printer formats (including support for color printers), and popular
graphics file formats.

%package devel
Summary:	libgs header files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libgs - ghostscript shared library.

%package ijs-devel
Summary:	IJS development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description ijs-devel
IJS development files.

%package cups
Summary:	Ghostscript CUPS files
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description cups
Ghostscript CUPS files.

%package gtk
Summary:	Ghostscript with GTK+ console
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description gtk
Ghostscript with GTK+ console.

%package x11
Summary:	X Window System drivers for Ghostscript
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description x11
X Window System output drivers for Ghostscript: x11, x11alpha.

%prep
%setup -q

rm -rf jpeg libpng zlib jasper expat tiff lcms freetype

%build
%{__aclocal}
%{__autoconf}
%configure \
	--disable-compile-inits	\
	--enable-dynamic	\
	--enable-fontconfig	\
	--enable-freetype	\
	--with-drivers=ALL	\
	--with-fontpath="%{_datadir}/fonts:%{_datadir}/fonts/Type1"	\
	--with-ijs		\
	--with-install-cups	\
	--with-jbig2dec		\
	--with-omni		\
	--with-system-libtiff 	\
	--with-x		\
	--without-luratech

cd ijs
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--enable-shared
cd ..

%{__make} -j1 so \
	docdir=%{_docdir}/%{name}-%{version}

%{__make} -j1 \
	docdir=%{_docdir}/%{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/ghostscript/lib,%{_libdir},%{_includedir}/{ghostscript,ps}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_docdir}/%{name}-%{version}

%{__make} soinstall \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_docdir}/%{name}-%{version}

%{__make} -C ijs install \
	DESTDIR=$RPM_BUILD_ROOT

# Headers
install psi/{iapi,ierrors}.h $RPM_BUILD_ROOT%{_includedir}/ghostscript
install base/gdevdsp.h $RPM_BUILD_ROOT%{_includedir}/ghostscript

rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/doc \
	$RPM_BUILD_ROOT%{_bindir}/*.sh \
	$RPM_BUILD_ROOT%{_mandir}/man1/{ps2pdf1{2,3},gsbj,gsdj,gsdj500,gslj,eps2eps}.1 \
	$RPM_BUILD_ROOT%{_mandir}/de/man1/{ps2pdf1{2,3},eps2eps}.1

echo ".so gs.1"     > $RPM_BUILD_ROOT%{_mandir}/man1/ghostscript.1
echo ".so ps2pdf.1" > $RPM_BUILD_ROOT%{_mandir}/man1/ps2pdf12.1
echo ".so ps2pdf.1" > $RPM_BUILD_ROOT%{_mandir}/man1/ps2pdf13.1
echo ".so ps2ps.1"  > $RPM_BUILD_ROOT%{_mandir}/man1/eps2eps.1
echo ".so gslp.1"   > $RPM_BUILD_ROOT%{_mandir}/man1/gsbj.1
echo ".so gslp.1"   > $RPM_BUILD_ROOT%{_mandir}/man1/gsdj.1
echo ".so gslp.1"   > $RPM_BUILD_ROOT%{_mandir}/man1/gsdj500.1
echo ".so gslp.1"   > $RPM_BUILD_ROOT%{_mandir}/man1/gslj.1

echo ".so ps2ps.1"  > $RPM_BUILD_ROOT%{_mandir}/de/man1/eps2eps.1
echo ".so ps2pdf.1" > $RPM_BUILD_ROOT%{_mandir}/de/man1/ps2pdf12.1
echo ".so ps2pdf.1" > $RPM_BUILD_ROOT%{_mandir}/de/man1/ps2pdf13.1

ln -sf gs $RPM_BUILD_ROOT%{_bindir}/gsc
ln -sf gs $RPM_BUILD_ROOT%{_bindir}/ghostscript
ln -sf gstoraster $RPM_BUILD_ROOT%{_ulibdir}/cups/filter/pdftoraster
ln -sf gstoraster $RPM_BUILD_ROOT%{_ulibdir}/cups/filter/pstoraster

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}

%dir %{_datadir}/ghostscript
%dir %{_datadir}/ghostscript/%{version}
%dir %{_datadir}/ghostscript/%{version}/lib

%attr(755,root,root) %{_bindir}/dvipdf
%attr(755,root,root) %{_bindir}/eps2eps
%attr(755,root,root) %{_bindir}/font2c
%attr(755,root,root) %{_bindir}/ghostscript
%attr(755,root,root) %{_bindir}/gs
%attr(755,root,root) %{_bindir}/gsbj
%attr(755,root,root) %{_bindir}/gsc
%attr(755,root,root) %{_bindir}/gsdj
%attr(755,root,root) %{_bindir}/gsdj500
%attr(755,root,root) %{_bindir}/gslj
%attr(755,root,root) %{_bindir}/gslp
%attr(755,root,root) %{_bindir}/gsnd
%attr(755,root,root) %{_bindir}/ijs_client_example
%attr(755,root,root) %{_bindir}/ijs_server_example
%attr(755,root,root) %{_bindir}/pdf2dsc
%attr(755,root,root) %{_bindir}/pdf2ps
%attr(755,root,root) %{_bindir}/pdfopt
%attr(755,root,root) %{_bindir}/pf2afm
%attr(755,root,root) %{_bindir}/pfbtopfa
%attr(755,root,root) %{_bindir}/printafm
%attr(755,root,root) %{_bindir}/ps2ascii
%attr(755,root,root) %{_bindir}/ps2epsi
%attr(755,root,root) %{_bindir}/ps2pdf
%attr(755,root,root) %{_bindir}/ps2pdf12
%attr(755,root,root) %{_bindir}/ps2pdf13
%attr(755,root,root) %{_bindir}/ps2pdf14
%attr(755,root,root) %{_bindir}/ps2pdfwr
%attr(755,root,root) %{_bindir}/ps2ps
%attr(755,root,root) %{_bindir}/ps2ps2
%attr(755,root,root) %{_bindir}/pphs
%attr(755,root,root) %{_bindir}/wftopfa

%attr(755,root,root) %ghost %{_libdir}/libgs.so.?
%attr(755,root,root) %{_libdir}/libgs.so.*.*
%attr(755,root,root) %{_libdir}/libijs-*.so

%{_datadir}/ghostscript/%{version}/Resource
%{_datadir}/ghostscript/%{version}/examples
%{_datadir}/ghostscript/%{version}/iccprofiles
%{_datadir}/ghostscript/%{version}/lib/*.*

%{_mandir}/man*/*
%lang(de) %{_mandir}/de/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgs.so
%{_includedir}/ghostscript
%{_includedir}/ps

%files ijs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ijs-config
%attr(755,root,root) %{_libdir}/libijs.so
%{_includedir}/ijs
%{_libdir}/libijs.la
%{_pkgconfigdir}/*.pc

%files cups
%defattr(644,root,root,755)
%attr(755,root,root) %{_ulibdir}/cups/filter/gstopxl
%attr(755,root,root) %{_ulibdir}/cups/filter/gstoraster
%attr(755,root,root) %{_ulibdir}/cups/filter/pdftoraster
%attr(755,root,root) %{_ulibdir}/cups/filter/pstoraster
%{_datadir}/cups/model/pxlcolor.ppd
%{_datadir}/cups/model/pxlmono.ppd
/etc/cups/gstoraster.convs

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gsx

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ghostscript/%{version}/X11.so

