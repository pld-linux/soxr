#
# Conditional build:
%bcond_without	gomp	# OpenMP support
#
Summary:	SoX Resampler library
Summary(pl.UTF-8):	Biblioteka resamplera SoX
Name:		soxr
Version:	0.1.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/soxr/%{name}-%{version}-Source.tar.xz
# Source0-md5:	0866fc4320e26f47152798ac000de1c0
URL:		http://soxr.sourceforge.net/
BuildRequires:	cmake >= 2.8
%{?with_gomp:BuildRequires:	gcc >= 6:4.2}
%{?with_gomp:BuildRequires:	libgomp-devel}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SoX Resampler library `libsoxr' performs one-dimensional
sample-rate conversion - it may be used, for example, to resample
PCM-encoded audio.

%description -l pl.UTF-8
Biblioteka SoX Resampler (libsoxr) wykonuje jednowymiarową konwersję
częstotliwości próbkowania - może być używana na przykład do
resamplowania dźwięku kodowanego PCM. 

%package devel
Summary:	Header files for SoX Resampler library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SoX Resampler
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SoX Resampler library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SoX Resampler.

%prep
%setup -q -n %{name}-%{version}-Source

%build
%cmake . \
	%{!?with_gomp:-DWITH_OPENMP=OFF}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# move examples to standard place
install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libsoxr/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# remaining files packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libsoxr

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENCE NEWS README TODO
%attr(755,root,root) %{_libdir}/libsoxr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsoxr.so.0
%attr(755,root,root) %{_libdir}/libsoxr-lsr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsoxr-lsr.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsoxr.so
%attr(755,root,root) %{_libdir}/libsoxr-lsr.so
%{_includedir}/soxr.h
%{_includedir}/soxr-lsr.h
%{_pkgconfigdir}/soxr.pc
%{_pkgconfigdir}/soxr-lsr.pc
%{_examplesdir}/%{name}-%{version}
