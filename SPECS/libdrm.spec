%global commit cc9a53f076d4e958e595e1daaff2c286ce1b7bb1
%global commitdate 20160418
%global checkout %{commitdate}git%{shortcommit}
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Direct Rendering Manager runtime library
Name: libdrm
Version: 2.4.67
Release: 7.%{checkout}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://dri.sourceforge.net

%if 0%{?commitdate}
Source0: %{name}-%{commitdate}.tar.bz2
%else
Source0: http://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.bz2
%endif
Source2: 91-drm-modeset.rules

BuildRequires: pkgconfig automake autoconf libtool
BuildRequires: kernel-headers
BuildRequires: libxcb-devel
%if 0%{?fedora} > 17 || 0%{?rhel} > 6
BuildRequires: systemd-devel
Requires: systemd
%else
BuildRequires: libudev-devel
Requires: udev
%endif
BuildRequires: libatomic_ops-devel
BuildRequires: libpciaccess-devel
BuildRequires: libxslt docbook-style-xsl
%ifnarch s390
BuildRequires: valgrind-devel
%endif
BuildRequires: xorg-x11-util-macros

# hardcode the 666 instead of 660 for device nodes
Patch3: libdrm-make-dri-perms-okay.patch
# remove backwards compat not needed on Fedora
Patch4: libdrm-2.4.0-no-bc.patch
# make rule to print the list of test programs
Patch5: libdrm-2.4.25-check-programs.patch

%description
Direct Rendering Manager runtime library

%package devel
Summary: Direct Rendering Manager development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers >= 2.6.27-0.144.rc0.git2.fc10
Requires: pkgconfig

%description devel
Direct Rendering Manager development package

%package -n drm-utils
Summary: Direct Rendering Manager utilities
Group: Development/Tools

%description -n drm-utils
Utility programs for the kernel DRM interface.  Will void your warranty.

%prep
%setup -q %{?commitdate:-n %{name}-%{commitdate}}
%patch3 -p1 -b .forceperms
%patch4 -p1 -b .no-bc
%patch5 -p1 -b .check

%build
autoreconf -v --install || exit 1
%configure \
%ifarch s390
    --disable-valgrind \
%endif
    --disable-vc4 \
%ifarch %{arm} aarch64
    --enable-exynos-experimental-api \
    --enable-tegra-experimental-api \
    --enable-vc4 \
%endif
%ifarch %{arm}
    --enable-omap-experimental-api \
%endif
    --enable-install-test-programs \
    --enable-udev

make %{?_smp_mflags} V=1
pushd tests
make %{?smp_mflags} `make check-programs` V=1
popd

%install
make install DESTDIR=%{buildroot}
pushd tests
mkdir -p %{buildroot}%{_bindir}
for foo in $(make check-programs) ; do
 libtool --mode=install install -m 0755 $foo %{buildroot}%{_bindir}
done
popd
# SUBDIRS=libdrm
mkdir -p %{buildroot}/lib/udev/rules.d/
install -m 0644 %{SOURCE2} %{buildroot}/lib/udev/rules.d/

# NOTE: We intentionally don't ship *.la files
find %{buildroot} -type f -name "*.la" -delete

for i in r300_reg.h via_3d_reg.h
do
rm -f %{buildroot}/usr/include/libdrm/$i
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.4.0
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so.1
%{_libdir}/libdrm_intel.so.1.0.0
%endif
%ifarch %{arm}
%{_libdir}/libdrm_omap.so.1
%{_libdir}/libdrm_omap.so.1.0.0
%endif
%ifarch %{arm} aarch64
%{_libdir}/libdrm_exynos.so.1
%{_libdir}/libdrm_exynos.so.1.0.0
%{_libdir}/libdrm_freedreno.so.1
%{_libdir}/libdrm_freedreno.so.1.0.0
%{_libdir}/libdrm_tegra.so.0
%{_libdir}/libdrm_tegra.so.0.0.0
%endif
%{_libdir}/libdrm_radeon.so.1
%{_libdir}/libdrm_radeon.so.1.0.1
%{_libdir}/libdrm_amdgpu.so.1
%{_libdir}/libdrm_amdgpu.so.1.0.0
%{_libdir}/libdrm_nouveau.so.2
%{_libdir}/libdrm_nouveau.so.2.0.0
%{_libdir}/libkms.so.1
%{_libdir}/libkms.so.1.0.0
/lib/udev/rules.d/91-drm-modeset.rules

%files -n drm-utils
%{_bindir}/dristat
%{_bindir}/drmstat
%{_bindir}/drmdevice
%{_bindir}/getclient
%{_bindir}/getstats
%{_bindir}/getversion
%{_bindir}/name_from_fd
%{_bindir}/openclose
%{_bindir}/setversion
%{_bindir}/updatedraw
%{_bindir}/modetest
%{_bindir}/modeprint
%{_bindir}/vbltest
%{_bindir}/kmstest
%{_bindir}/kms-steal-crtc
%{_bindir}/kms-universal-planes
%exclude %{_bindir}/exynos*
%exclude %{_bindir}/drmsl
%exclude %{_bindir}/hash
%exclude %{_bindir}/proptest
%exclude %{_bindir}/random

%files devel
# FIXME should be in drm/ too
%{_includedir}/xf86drm.h
%{_includedir}/xf86drmMode.h
%dir %{_includedir}/libdrm
%{_includedir}/libdrm/drm.h
%{_includedir}/libdrm/drm_fourcc.h
%{_includedir}/libdrm/drm_mode.h
%{_includedir}/libdrm/drm_sarea.h
%ifarch %{ix86} x86_64 ia64
%{_includedir}/libdrm/intel_aub.h
%{_includedir}/libdrm/intel_bufmgr.h
%{_includedir}/libdrm/intel_debug.h
%endif
%ifarch %{arm}
%{_includedir}/libdrm/omap_drmif.h
%{_includedir}/omap/
%endif
%ifarch %{arm} aarch64
%{_includedir}/exynos/
%{_includedir}/freedreno/
%{_includedir}/libdrm/exynos_drmif.h
%{_includedir}/libdrm/tegra.h
%{_includedir}/libdrm/vc4_packet.h
%{_includedir}/libdrm/vc4_qpu_defines.h
%endif
%{_includedir}/libdrm/amdgpu.h
%{_includedir}/libdrm/radeon_bo.h
%{_includedir}/libdrm/radeon_bo_gem.h
%{_includedir}/libdrm/radeon_bo_int.h
%{_includedir}/libdrm/radeon_cs.h
%{_includedir}/libdrm/radeon_cs_gem.h
%{_includedir}/libdrm/radeon_cs_int.h
%{_includedir}/libdrm/radeon_surface.h
%{_includedir}/libdrm/r600_pci_ids.h
%{_includedir}/libdrm/nouveau/
%{_includedir}/libdrm/*_drm.h
%{_includedir}/libkms
%{_libdir}/libdrm.so
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so
%endif
%ifarch %{arm}
%{_libdir}/libdrm_omap.so
%endif
%ifarch %{arm} aarch64
%{_libdir}/libdrm_exynos.so
%{_libdir}/libdrm_freedreno.so
%{_libdir}/libdrm_tegra.so
%endif
%{_libdir}/libdrm_radeon.so
%{_libdir}/libdrm_amdgpu.so
%{_libdir}/libdrm_nouveau.so
%{_libdir}/libkms.so
%{_libdir}/pkgconfig/libdrm.pc
%ifarch %{ix86} x86_64 ia64
%{_libdir}/pkgconfig/libdrm_intel.pc
%endif
%ifarch %{arm}
%{_libdir}/pkgconfig/libdrm_omap.pc
%endif
%ifarch %{arm} aarch64
%{_libdir}/pkgconfig/libdrm_exynos.pc
%{_libdir}/pkgconfig/libdrm_freedreno.pc
%{_libdir}/pkgconfig/libdrm_tegra.pc
%{_libdir}/pkgconfig/libdrm_vc4.pc
%endif
%{_libdir}/pkgconfig/libdrm_radeon.pc
%{_libdir}/pkgconfig/libdrm_amdgpu.pc
%{_libdir}/pkgconfig/libdrm_nouveau.pc
%{_libdir}/pkgconfig/libkms.pc
%{_mandir}/man3/drm*.3*
%{_mandir}/man7/drm*.7*

%changelog
