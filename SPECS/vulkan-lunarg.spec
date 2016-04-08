%global        _so_version     1.0.5

Name:            VulkanTools-sdk
Epoch:           1
Version:         %{_so_version}.0
Release:         1%{?dist}
Summary:         NVIDIA's proprietary display driver for NVIDIA graphic cards

Group:           User Interface/X Hardware Support
License:         Redistributable, no modification permitted
URL:             http://www.nvidia.com/
Source0:         https://github.com/LunarG/VulkanTools/archive/sdk-%{version}.zip

ExclusiveArch: i686 x86_64

BuildRequires:   libpciaccess-devel bison libxcb-devel ImageMagick-devel git cmake mesa-libGL-devel

Requires:        libpciaccess libxcb ImageMagick

%description
This package provides the LunarG Vulkan SDK from https://github.com/LunarG

%prep
%setup -q -a 0

%build
# Nothing to build
./update_external_sources.sh
cmake -H. -Bdbuild -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=/usr
cd dbuild
make %{?_smp_mflags}


%install
sed -i 's/\.\///g' icd/intel/intel_icd.json
sed -i 's/\.\///g' icd/nulldrv/nulldrv_icd.json

install -m 0755 -d $RPM_BUILD_ROOT%{_bindir}
install -m 0755 -d $RPM_BUILD_ROOT%{_libdir}
install -m 0755 -d $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/
install -m 0755 -d $RPM_BUILD_ROOT%{_datadir}/vulkan-demos

install -p -m 0755 dbuild/vktrace/vk* $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 dbuild/vktrace/lib*.so $RPM_BUILD_ROOT%{_libdir}

install -p -m 0755 dbuild/tests/vkbase $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 dbuild/tests/vk_*_tests $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 dbuild/tests/gtest-1.7.0/lib*.so $RPM_BUILD_ROOT%{_libdir}

install -p -m 0755 dbuild/loader/libvulkan.so.%{_so_version} $RPM_BUILD_ROOT%{_libdir}
for lib in $( find $RPM_BUILD_ROOT%{_libdir} -name libvulkan.so.%{_so_version} ) ; do
  ln -s ${lib##*/} ${lib%.%{_so_version}}
  ln -s ${lib##*/} ${lib%.%{_so_version}}.1
done

install -p -m 0755 dbuild/libs/vkjson/lib*.a $RPM_BUILD_ROOT%{_libdir}
install -p -m 0755 dbuild/libs/vkjson/vkjson_* $RPM_BUILD_ROOT%{_bindir}

install -p -m 0755 dbuild/layers/lib*.so $RPM_BUILD_ROOT%{_libdir}

install -p -m 0755 dbuild/icd/intel/compiler/standalone_compiler $RPM_BUILD_ROOT%{_bindir}/vk_standalone_compiler
install -p -m 0755 dbuild/icd/intel/compiler/lib*.a $RPM_BUILD_ROOT%{_libdir}
install -p -m 0755 dbuild/icd/intel/kmd/lib*.a $RPM_BUILD_ROOT%{_libdir}
install -p -m 0755 dbuild/icd/common/lib*.a $RPM_BUILD_ROOT%{_libdir}

install -p -m 0755 dbuild/icd/intel/lib*.so $RPM_BUILD_ROOT%{_libdir}
install -p -m 0755 dbuild/icd/nulldrv/lib*.so $RPM_BUILD_ROOT%{_libdir}

install -p -m 0644 icd/intel/intel_icd.json $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/
install -p -m 0644 icd/nulldrv/nulldrv_icd.json $RPM_BUILD_ROOT%{_sysconfdir}/vulkan/icd.d/

install -m 0755 -d $RPM_BUILD_ROOT%{_includedir}/vulkan/
install -p -m 0644 include/vulkan/*.h $RPM_BUILD_ROOT%{_includedir}/vulkan/

install -p -m 0755 dbuild/demos/vulkaninfo $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 dbuild/demos/tri $RPM_BUILD_ROOT%{_datadir}/vulkan-demos
install -p -m 0755 dbuild/demos/cube $RPM_BUILD_ROOT%{_datadir}/vulkan-demos
install -p -m 0755 dbuild/demos/smoke/smoke $RPM_BUILD_ROOT%{_datadir}/vulkan-demos
install -p -m 0755 dbuild/demos/*.spv $RPM_BUILD_ROOT%{_datadir}/vulkan-demos
install -p -m 0644 dbuild/demos/lunarg.ppm $RPM_BUILD_ROOT%{_datadir}/vulkan-demos


%pre

%post

%files
%defattr(-,root,root,-)
%{_includedir}/vulkan/

%{_bindir}/vkreplay
%{_bindir}/vktrace

%{_libdir}/libVkLayer_vktrace_layer.so

%{_bindir}/vkbase
%{_bindir}/vk_blit_tests
%{_bindir}/vk_image_tests
%{_bindir}/vk_layer_validation_tests
%{_bindir}/vk_render_tests
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so

%{_libdir}/libvulkan.so
%{_libdir}/libvulkan.so.1
%{_libdir}/libvulkan.so.%{_so_version}

%{_libdir}/libvkjson.a
%{_bindir}/vkjson_info
%{_bindir}/vkjson_unittest

%{_libdir}/liblayer_utils.so
%{_libdir}/libVkLayer_api_dump.so
%{_libdir}/libVkLayer_basic.so
%{_libdir}/libVkLayer_device_limits.so
%{_libdir}/libVkLayer_draw_state.so
%{_libdir}/libVkLayer_generic.so
%{_libdir}/libVkLayer_image.so
%{_libdir}/libVkLayer_mem_tracker.so
%{_libdir}/libVkLayer_multi.so
%{_libdir}/libVkLayer_object_tracker.so
%{_libdir}/libVkLayer_param_checker.so
%{_libdir}/libVkLayer_screenshot.so
%{_libdir}/libVkLayer_swapchain.so
%{_libdir}/libVkLayer_threading.so
%{_libdir}/libVkLayer_unique_objects.so

%{_bindir}/vk_standalone_compiler
%{_libdir}/libintelcompiler.a
%{_libdir}/libintelcompiler-os.a
%{_libdir}/libintelkmd.a
%{_libdir}/libicd.a

%{_libdir}/libVK_i965.so
%{_libdir}/libVK_nulldrv.so
%{_sysconfdir}/vulkan/icd.d/intel_icd.json
%{_sysconfdir}/vulkan/icd.d/nulldrv_icd.json

%{_bindir}/vulkaninfo
%{_datadir}/vulkan-demos/


%changelog
* Tue Mar 29 2016 Tiziano Carotti
- Initial version

