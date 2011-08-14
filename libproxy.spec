%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define gecko_version 1.9.2

Name:           libproxy
Version:        0.3.0
Release:        2%{?dist}
Summary:        A library handling all the details of proxy configuration

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/libproxy/
Source0:        http://libproxy.googlecode.com/files/libproxy-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
Requires: libproxy-python = %{version}-%{release}
Requires: libproxy-bin = %{version}-%{release}

# gnome
BuildRequires:  GConf2-devel
# mozjs
BuildRequires:  gecko-devel >= %{gecko_version}
# NetworkManager
BuildRequires:  NetworkManager-devel
BuildRequires:  dbus-devel
# webkit (gtk)
BuildRequires:  WebKit-gtk-devel
# kde
BuildRequires:  libXmu-devel
BuildRequires:  libX11-devel


%description
libproxy offers the following features:

    * extremely small core footprint (< 35K)
    * no external dependencies within libproxy core
      (libproxy plugins may have dependencies)
    * only 3 functions in the stable external API
    * dynamic adjustment to changing network topology
    * a standard way of dealing with proxy settings across all scenarios
    * a sublime sense of joy and accomplishment 


%package        bin
Summary:        Binary to test %{name}
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description    bin
The %{name}-bin package contains the proxy binary for %{name}

%package        python
Summary:        Binding for %{name} and python
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    python
The %{name}-python package contains the python binding for %{name}

%package        gnome
Summary:        Plugin for %{name} and gnome
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    gnome
The %{name}-gnome package contains the %{name} plugin for gnome.

%package        kde
Summary:        Plugin for %{name} and kde
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    kde
The %{name}-kde package contains the %{name} plugin for kde.

%package        mozjs
Summary:        Plugin for %{name} and mozjs
Group:          System Environment/Libraries
Requires:       %{name} = %{version}
#Tweak this according to the current gecko-libs version
Requires:       gecko-libs >= %{gecko_version}
Provides:       %{name}-pac = %{version}-%{release}

%description    mozjs
The %{name}-mozjs package contains the %{name} plugin for mozjs.

%package        webkit
Summary:        Plugin for %{name} and webkit
Group:          System Environment/Libraries
Requires:       %{name} = %{version}
Provides:       %{name}-pac = %{version}-%{release}

%description    webkit
The %{name}-webkit package contains the %{name} plugin for
webkit.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q



%build
%configure --includedir=%{_includedir}/libproxy --disable-static --with-python
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules
%{_libdir}/%{name}/%{version}/modules/config_direct.so
%{_libdir}/%{name}/%{version}/modules/config_envvar.so
%{_libdir}/%{name}/%{version}/modules/config_file.so
%{_libdir}/%{name}/%{version}/modules/config_wpad.so
%{_libdir}/%{name}/%{version}/modules/ignore_ip.so
%{_libdir}/%{name}/%{version}/modules/ignore_domain.so
%{_libdir}/%{name}/%{version}/modules/network_networkmanager.so
%{_libdir}/%{name}/%{version}/modules/wpad_dnsdevolution.so
%{_libdir}/%{name}/%{version}/modules/wpad_dns.so

%files bin
%defattr(-,root,root,-)
%{_bindir}/proxy

%files python
%defattr(-,root,root,-)
%{python_sitelib}/*

%files gnome
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_gnome.so

%files kde
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/config_kde.so

%files mozjs
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/pacrunner_mozjs.so

%files webkit
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/modules/pacrunner_webkit.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/libproxy/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libproxy-1.0.pc


%changelog
* Fri Aug 27 2010 Jan Horak <jhorak@redhat.com> - 0.3.0-2
- Rebuild against newer gecko

* Thu Sep 24 2009 kwizart < kwizart at gmail.com > - 0.3.0-1
- Update to 0.3.0

* Thu Sep 17 2009 kwizart < kwizart at gmail.com > - 0.2.3-12
- Remove Requirement of %%{name}-pac virtual provides 
  from the main package - #524043

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 kwizart < kwizart at gmail.com > - 0.2.3-10
- Rebuild for webkit
- Raise requirement for xulrunner to 1.9.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 kwizart < kwizart at gmail.com > - 0.2.3-8
- Merge NetworkManager module into the main libproxy package
- Main Requires the -python and -bin subpackage 
 (splitted for multilibs compliance).

* Fri Oct 24 2008 kwizart < kwizart at gmail.com > - 0.2.3-7
- Disable Gnome/KDE default support via builtin modules.
 (it needs to be integrated via Gconf2/neon instead).

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-6
- Disable Obsoletes.
- Requires ev instead of evr for optionnals sub-packages.

* Tue Oct 21 2008 kwizart < kwizart at gmail.com > - 0.2.3-5
- Use conditionals build.

* Mon Sep 15 2008 kwizart < kwizart at gmail.com > - 0.2.3-4
- Remove plugin- in the name of the packages

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-3
- Move proxy.h to libproxy/proxy.h
  This will prevent it to be included in the default include path
- Split main to libs and util and use libproxy to install all

* Mon Aug  4 2008 kwizart < kwizart at gmail.com > - 0.2.3-2
- Rename binding-python to python
- Add Requires: gecko-libs >= %%{gecko_version}
- Fix some descriptions
- Add plugin-webkit package
 
* Fri Jul 11 2008 kwizart < kwizart at gmail.com > - 0.2.3-1
- Convert to Fedora spec

* Fri Jun 6 2008 - dominique-rpm@leuenberger.net
- Updated to version 0.2.3
* Wed Jun 4 2008 - dominique-rpm@leuenberger.net
- Extended spec file to build all available plugins
* Tue Jun 3 2008 - dominique-rpm@leuenberger.net
- Initial spec file for Version 0.2.2

