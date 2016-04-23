# Filter GLIBC_PRIVATE Requires, see wrappers/dlsym.cpp
%define __filter_GLIBC_PRIVATE 1

Name:           apitrace
Version:        7.1
Release:        1%{?dist}
Summary:        Tools for tracing OpenGL

License:        MIT
URL:            http://apitrace.github.io/
Source0:        https://github.com/apitrace/apitrace/archive/%{version}.tar.gz
Source1:        qapitrace.desktop
Source2:        qapitrace.appdata.xml

# Unbundle gtest
Patch0:         apitrace-7.1_gtest.patch

BuildRequires:  cmake
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  python2-devel
BuildRequires:  libpng-devel
BuildRequires:  snappy-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gtest-devel

Requires:       %{name}-libs%{_isa} = %{version}-%{release}
# scripts/snapdiff.py
Requires:       python-pillow

# See http://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_exceptions
Provides:       bundled(md5-plumb)
# See https://fedorahosted.org/fpc/ticket/429
Provides:       bundled(libbacktrace)


%description
apitrace consists of a set of tools to:
 * trace OpenGL and OpenGL ES  APIs calls to a file;
 * replay OpenGL and OpenGL ES calls from a file
 * inspect OpenGL state at any call while retracing
 * visualize and edit trace files


%package libs
Summary:        Libraries used by apitrace
Requires:       %{name} = %{version}-%{release}

%description libs
Libraries used by apitrace


%package gui
Summary:        Graphical frontend for apitrace
Requires:       %{name}%{_isa} = %{version}-%{release}

%description gui
This package contains qapitrace, the Graphical frontend for apitrace.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

# Remove bundled libraries, except khronos headers and libbacktrace
rm -rf `ls -1 thirdparty | grep -Ev "(khronos|md5|libbacktrace)"`

# Fix shebangs
find scripts -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'

# Fix spurious-executable-perm
chmod -x retrace/glretrace_main.cpp


%build
%cmake .
make %{?_smp_mflags}


%install
%make_install

# Install doc through %%doc
rm -rf %{buildroot}%{_docdir}/

# Install desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{SOURCE1}

# Install appdata file
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_datadir}/appdata/qapitrace.appdata.xml
%{_bindir}/appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/qapitrace.appdata.xml

# highlight.py is not a script
chmod 0644 %{buildroot}%{_libdir}/%{name}/scripts/highlight.py


%check
make check


%post gui
/usr/bin/update-desktop-database &> /dev/null || :


%postun gui
/usr/bin/update-desktop-database &> /dev/null || :


%files
%license LICENSE
%doc README.markdown docs/*
%{_bindir}/apitrace
%{_bindir}/eglretrace
%{_bindir}/glretrace

%files libs
%{_libdir}/%{name}/

%files gui
%{_bindir}/qapitrace
%{_datadir}/applications/qapitrace.desktop
%{_datadir}/appdata/qapitrace.appdata.xml



%changelog
* Wed Nov 25 2015 Sandro Mani <manisandro@gmail.com> - 7.1-1
- Update to 7.1

* Wed Sep 16 2015 Richard Hughes <rhughes@redhat.com> - 7.0-2
- Fix the AppData file to actually validate

* Thu Jul 23 2015 Sandro Mani <manisandro@gmail.com> - 7.0-1
- Update to 7.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.1-4
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 02 2015 Sandro Mani <manisandro@gmail.com> - 6.1-3
- Remove dlsym hack, use %%define __filter_GLIBC_PRIVATE 1

* Fri Jan 16 2015 Sandro Mani <manisandro@gmail.com> - 6.1-2
- Fix appdata file

* Fri Jan 16 2015 Sandro Mani <manisandro@gmail.com> - 6.1-1
- Update to 6.1

* Tue Jan 06 2015 Sandro Mani <manisandro@gmail.com> - 6.0-2
- Re-introduce dlsym hack

* Mon Jan 05 2015 Sandro Mani <manisandro@gmail.com> - 6.0-1
- Update to 6.0
- Ship appdata file

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Adam Jackson <ajax@redhat.com> 5.0-3
- Fix dlsym hack to work on arm (and probably others)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Sandro Mani <manisandro@gmail.com> - 5.0-1
- Update to 5.0

* Fri Mar 07 2014 Sandro Mani <manisandro@gmail.com> - 4.0-5
- Split off libs package
- Allow tracing 32bit binaries on 64bit

* Mon Nov 18 2013 Sandro Mani <manisandro@gmail.com> - 4.0-4
- chmod 0644 scripts/highlight.py
- Fix all python shebangs according to fedora guidelines
- Use BR: python2-devel
- Split off qapitrace into subpackage

* Sat Nov 16 2013 Sandro Mani <manisandro@gmail.com> - 4.0-3
- Fix desktop-file-install syntax

* Sat Nov 16 2013 Sandro Mani <manisandro@gmail.com> - 4.0-2
- Fix %%{_buildroot} -> %%{buildroot} typo
- Remove explicit BRs which are implicit

* Wed Nov 13 2013 Sandro Mani <manisandro@gmail.com> - 4.0-1
- Initial package
