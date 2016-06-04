%global     capsname   GLXOSD

Name:     glxosd
Version:  3.2.0
Release:  1%{?dist}
Summary:  An OSD for OpenGL applications. Monitor your framerate in games.

License:  MIT
URL:      https://glxosd.nickguletskii.com/
Source0:  glxosd-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  mesa-libGLU-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  boost-devel
BuildRequires:  lm_sensors-devel

%description
GLXOSD is an on-screen display (OSD)/overlay for OpenGL applications running on Linux with X11. It
can show FPS, the temperature of your CPU, and if you have an NVIDIA graphics card (with
proprietary drivers), it will also show the temperature of the GPU. Also, it can log frame timings,
which is useful for benchmarking. This project aims to provide some of the functionality that
RivaTuner OSD (which is used by MSI Afterburner) provides under Windows.

%prep
%setup -q -n %{capsname}-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX=/usr \
      -DINSTALLATION_SUFFIX_64=lib64 \
      -DINSTALLATION_SUFFIX_32=lib \
      -G "Unix Makefiles"
make %{?_smp_mflags} all

%install
%make_install

%files
%attr(755, root, root) %{_bindir}/%{name}
%{_bindir}/%{name}
%{_libdir}/*
%{_datadir}/%{name}
%{_sysconfdir}/%{name}
%doc README.md
%doc AUTHORS
%license LICENSE

%changelog
* Sun Feb 21 2016 Kamil Páral <kparal@redhat.com> - 2.5.0-1.20160210git7f0886e
- initial release from 20160210 (git version)
