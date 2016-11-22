Summary:            Script & GNOME Tools for switch between Nvidia and Intel GPU on Optimus Laptop
Name:               nvidia-optimus
Version:            1.0.2
Release:            1%{?dist}
License:            GPLv3
Group:              System Environment/Kernel
Source:             %{name}-%{version}.tar.gz
URL:                https://github.com/ivendor
BuildArch: 	  noarch
Requires:          akmod-nvidia,xorg-x11-drv-nvidia-libs,xorg-x11-drv-nvidia,mesa-libGL,mesa-libglapi,mesa-dri-drivers,gnome-shell, gdm, kernel-devel

%description
Script & GNOME Tools for switch between Nvidia and Intel GPU on Optimus Laptop

%prep
%autosetup -n %{name}

%build

%install
mkdir -p %{buildroot}/%{_sysconfdir}/X11/xorg.conf.d/
mkdir -p %{buildroot}/%{_sysconfdir}/X11/xinit/xinitrc.d
mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/modprobe.d
mkdir -p %{buildroot}/%{_sysconfdir}/prelink.conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/default
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/usr/lib/systemd/scripts
mkdir -p %{buildroot}/var/lib/gdm/.config/autostart/
mkdir -p %{buildroot}/%{_datadir}/gnome-shell/extensions/gpu-chooser@ivendor/icons

install -m 755 10-modesetting.sh %{buildroot}/%{_sysconfdir}/X11/xinit/xinitrc.d/
install -m 644 20-*.conf.disabled %{buildroot}/%{_sysconfdir}/X11/xorg.conf.d/
install -m 644 nvidia-modeset.conf.disabled %{buildroot}/%{_sysconfdir}/modprobe.d/
install -m 644 nvidia.conf.disabled %{buildroot}/%{_sysconfdir}/ld.so.conf.d/
install -m 644 prenvidia.conf.disabled %{buildroot}/%{_sysconfdir}/prelink.conf.d/nvidia.conf.disabled
install -m 755 gpuswitchcleaner %{buildroot}/usr/lib/systemd/scripts/
install -m 644 gpuswitchcleaner.service %{buildroot}/usr/lib/systemd/system/
install -m 755 gpu-choice.sh %{buildroot}/%{_sbindir}
install -m 755 modesetting.sh %{buildroot}/%{_sbindir}
install -m 644 optimus %{buildroot}/%{_sysconfdir}/default/
install -m 644 org.gnome.Shell.desktop %{buildroot}/var/lib/gdm/.config/autostart/
install -m 644 gpu-chooser@ivendor/*.js* %{buildroot}/%{_datadir}/gnome-shell/extensions/gpu-chooser@ivendor/
install -m 644 gpu-chooser@ivendor/icons/*.svg %{buildroot}/%{_datadir}/gnome-shell/extensions/gpu-chooser@ivendor/icons/

ln -s 20-intel.conf.disabled %{buildroot}/%{_sysconfdir}/X11/xorg.conf.d/20-gpu.conf

%files
%defattr(-,root,root,-)
%{_sysconfdir}/X11/xinit/xinitrc.d/10-modesetting.sh
%{_sysconfdir}/X11/xorg.conf.d/20-*.conf.disabled
%{_sysconfdir}/X11/xorg.conf.d/20-gpu.conf
%{_sysconfdir}/modprobe.d/nvidia-modeset.conf.disabled
%{_sysconfdir}/ld.so.conf.d/nvidia.conf.disabled
%{_sysconfdir}/prelink.conf.d/nvidia.conf.disabled
/usr/lib/systemd/scripts/gpuswitchcleaner
/usr/lib/systemd/system/gpuswitchcleaner.service
%{_sbindir}/gpu-choice.sh
%{_sbindir}/modesetting.sh
%{_sysconfdir}/default/optimus
%{_datadir}/gnome-shell/extensions/gpu-chooser@ivendor/*.js*
%{_datadir}/gnome-shell/extensions/gpu-chooser@ivendor/icons/*.svg
%defattr(-,gdm,gdm,-)
%attr(-,gdm,gdm) /var/lib/gdm/.config
%attr(-,gdm,gdm) /var/lib/gdm/.config/autostart
/var/lib/gdm/.config/autostart/org.gnome.Shell.desktop

%post
/usr/bin/systemctl daemon-reload
/usr/bin/systemctl enable gpuswitchcleaner
/usr/bin/systemctl enable akmods
sed -i s/BUSXXX/`lspci|grep NVIDIA|grep 3D|cut -d " " -f 1|sed  's/\./:/g'`/ /etc/X11/xorg.conf.d/20-nvidia-optimus.conf.disabled
echo "You should blacklist nouveau from kernel command line using rdblacklist=nouveau"
echo "You should enable X11 for gdm in /etc/gdm/custom.conf using WaylandEnable=False"
%preun
if [ $1 -eq 0 ] ; then
/usr/bin/systemctl disable gpuswitchcleaner
fi

%changelog
* Tue Nov 22 2016 Tiziano Carotti <t.carotti@quanticresearch.com> - 1.0.2-1
- Nvidia KMS Modeset enabler

* Sat Nov 5 2016 Tiziano Carotti <t.carotti@quanticresearch.com> - 1.0.1-1
- Support for libglvnd nvidia driver

* Thu Dec 10 2015 Tiziano Carotti <t.carotti@quanticresearch.com> - 1.0.0-1
- First Release

